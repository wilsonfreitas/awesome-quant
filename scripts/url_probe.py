"""Safe, retrying HTTP URL classification for README audit tooling."""

from __future__ import annotations

import http.client
import ipaddress
import socket
import ssl
from dataclasses import dataclass
from enum import StrEnum
from time import sleep
from typing import Callable
from urllib.parse import SplitResult, urljoin, urlsplit, urlunsplit


USER_AGENT = "awesome-quant-url-audit/1.0"
RETRYABLE_STATUSES = {408, 425, 500, 502, 503, 504}
REDIRECT_STATUSES = {300, 301, 302, 303, 307, 308}
PERMANENT_REDIRECT_STATUSES = {301, 308}
TRANSPORT_ERRORS = (OSError, ssl.SSLError, socket.gaierror, TimeoutError)


class Outcome(StrEnum):
    OK = "ok"
    DEAD = "dead"
    RESTRICTED = "restricted"
    TRANSIENT = "transient"
    HTTP_ERROR = "http_error"
    PERMANENT_REDIRECT = "permanent_redirect"


@dataclass(frozen=True)
class RawResponse:
    status: int
    location: str | None


@dataclass(frozen=True)
class UrlObservation:
    requested_url: str
    final_url: str
    status: int | None
    outcome: Outcome
    attempts: int
    redirect_chain: tuple[str, ...] = ()
    error: str = ""


class UnsafeUrlError(ValueError):
    """Raised before connecting to a URL that is not publicly routable."""


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection whose TCP peer is pinned while SNI remains the hostname."""

    def __init__(self, host: str, port: int, server_hostname: str, timeout: float):
        super().__init__(host, port, timeout=timeout, context=ssl.create_default_context())
        self._server_hostname = server_hostname

    def connect(self) -> None:
        self.sock = self._create_connection(
            (self.host, self.port), self.timeout, self.source_address
        )
        if self._tunnel_host:
            self._tunnel()
        self.sock = self._context.wrap_socket(self.sock, server_hostname=self._server_hostname)


class _PinnedHTTPConnection(http.client.HTTPConnection):
    """HTTP connection using an already-validated address as its TCP peer."""


def validate_public_url(url: str) -> tuple[str, int, str]:
    """Validate an HTTP(S) URL and return hostname, effective port, and pinned IP."""
    try:
        parsed = urlsplit(url)
    except ValueError as error:
        raise UnsafeUrlError("invalid URL") from error

    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"}:
        raise UnsafeUrlError("unsupported URL scheme")
    if parsed.username is not None or parsed.password is not None:
        raise UnsafeUrlError("URL credentials are not allowed")

    try:
        hostname = parsed.hostname
        explicit_port = parsed.port
    except ValueError as error:
        raise UnsafeUrlError("invalid port") from error
    if not hostname:
        raise UnsafeUrlError("missing hostname")
    if explicit_port == 0:
        raise UnsafeUrlError("port zero is not allowed")

    port = explicit_port or (443 if scheme == "https" else 80)
    results = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)

    addresses: list[str] = []
    for _family, _socktype, _protocol, _canonname, sockaddr in results:
        try:
            address = ipaddress.ip_address(sockaddr[0])
        except (IndexError, ValueError) as error:
            raise UnsafeUrlError("invalid resolved address") from error
        if not address.is_global:
            raise UnsafeUrlError("resolved address is not globally routable")
        addresses.append(str(address))
    if not addresses:
        raise UnsafeUrlError("hostname did not resolve")

    return hostname, port, min(addresses)


def _host_header(hostname: str, port: int, scheme: str) -> str:
    bracketed_host = f"[{hostname}]" if ":" in hostname else hostname
    default_port = 443 if scheme == "https" else 80
    return bracketed_host if port == default_port else f"{bracketed_host}:{port}"


def _request_target(parsed: SplitResult) -> str:
    target = parsed.path or "/"
    return f"{target}?{parsed.query}" if parsed.query else target


def _single_request(
    method: str,
    parsed: SplitResult,
    hostname: str,
    port: int,
    address: str,
    timeout: float,
) -> RawResponse:
    if parsed.scheme.lower() == "https":
        connection = _PinnedHTTPSConnection(address, port, hostname, timeout)
    else:
        connection = _PinnedHTTPConnection(address, port, timeout=timeout)

    response = None
    try:
        connection.request(
            method,
            _request_target(parsed),
            headers={
                "Host": _host_header(hostname, port, parsed.scheme.lower()),
                "User-Agent": USER_AGENT,
            },
        )
        response = connection.getresponse()
        return RawResponse(response.status, response.getheader("Location"))
    finally:
        if response is not None:
            response.close()
        connection.close()


def request_once(url: str, timeout: float = 10) -> RawResponse:
    """Perform a pinned HEAD request, falling back to GET when HEAD is unsupported."""
    hostname, port, address = validate_public_url(url)
    parsed = urlsplit(url)
    response = _single_request("HEAD", parsed, hostname, port, address, timeout)
    if response.status in {405, 501}:
        response = _single_request("GET", parsed, hostname, port, address, timeout)
    return response


def _canonical_url(url: str) -> str:
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()
    port = parsed.port
    default_port = 443 if scheme == "https" else 80
    host = f"[{hostname}]" if ":" in hostname else hostname
    netloc = host if port in {None, default_port} else f"{host}:{port}"
    path = parsed.path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parsed.query, ""))


def _http_error(
    requested_url: str,
    final_url: str,
    status: int | None,
    attempts: int,
    redirects: list[str],
    error: str,
) -> UrlObservation:
    return UrlObservation(
        requested_url,
        final_url,
        status,
        Outcome.HTTP_ERROR,
        attempts,
        tuple(redirects),
        error,
    )


def _classify_terminal(
    requested_url: str,
    final_url: str,
    response: RawResponse,
    attempts: int,
    redirects: list[str],
    saw_meaningful_permanent_redirect: bool,
) -> UrlObservation:
    if response.status in {404, 410}:
        outcome = Outcome.DEAD
        error = ""
    elif response.status in {401, 403, 407, 429, 451}:
        outcome = Outcome.RESTRICTED
        error = ""
    elif 200 <= response.status <= 399:
        outcome = (
            Outcome.PERMANENT_REDIRECT
            if saw_meaningful_permanent_redirect
            else Outcome.OK
        )
        error = ""
    else:
        outcome = Outcome.HTTP_ERROR
        error = f"HTTP status {response.status}"
    return UrlObservation(
        requested_url,
        final_url,
        response.status,
        outcome,
        attempts,
        tuple(redirects),
        error,
    )


def probe_url(
    requested_url: str,
    *,
    requester: Callable[[str, float], RawResponse] = request_once,
    sleeper: Callable[[float], None] = sleep,
    timeout: float = 10,
) -> UrlObservation:
    """Classify a public HTTP(S) URL without allowing DNS rebinding requests."""
    last_transport_error = ""
    for attempt, delay in enumerate((0, 1, 2), start=1):
        sleeper(delay)
        current_url = requested_url
        redirects: list[str] = []
        seen: set[str] = set()
        saw_meaningful_permanent_redirect = False
        try:
            while True:
                try:
                    validate_public_url(current_url)
                except UnsafeUrlError as error:
                    prefix = "unsafe URL" if current_url == requested_url else "unsafe redirect target"
                    return _http_error(
                        requested_url,
                        current_url,
                        None,
                        attempt,
                        redirects,
                        f"{prefix}: {error}",
                    )

                current_canonical = _canonical_url(current_url)
                seen.add(current_canonical)

                response = requester(current_url, timeout)
                if response.status not in REDIRECT_STATUSES:
                    if response.status in RETRYABLE_STATUSES:
                        if attempt == 3:
                            return UrlObservation(
                                requested_url,
                                current_url,
                                response.status,
                                Outcome.TRANSIENT,
                                attempt,
                                tuple(redirects),
                                f"retry limit exceeded: HTTP {response.status}",
                            )
                        break
                    return _classify_terminal(
                        requested_url,
                        current_url,
                        response,
                        attempt,
                        redirects,
                        saw_meaningful_permanent_redirect,
                    )

                if not response.location:
                    return _http_error(
                        requested_url,
                        current_url,
                        response.status,
                        attempt,
                        redirects,
                        "missing redirect location",
                    )
                if len(redirects) >= 5:
                    return _http_error(
                        requested_url,
                        current_url,
                        response.status,
                        attempt,
                        redirects,
                        "redirect limit exceeded",
                    )

                target_url = urljoin(current_url, response.location)
                try:
                    validate_public_url(target_url)
                except UnsafeUrlError as error:
                    return _http_error(
                        requested_url,
                        current_url,
                        response.status,
                        attempt,
                        redirects,
                        f"unsafe redirect target: {error}",
                    )
                target_canonical = _canonical_url(target_url)
                if target_canonical in seen:
                    return _http_error(
                        requested_url,
                        current_url,
                        response.status,
                        attempt,
                        redirects,
                        "redirect loop",
                    )
                if (
                    response.status in PERMANENT_REDIRECT_STATUSES
                    and target_canonical != current_canonical
                ):
                    saw_meaningful_permanent_redirect = True
                redirects.append(target_url)
                seen.add(target_canonical)
                current_url = target_url
        except TRANSPORT_ERRORS as error:
            last_transport_error = type(error).__name__
            if attempt == 3:
                return UrlObservation(
                    requested_url,
                    requested_url,
                    None,
                    Outcome.TRANSIENT,
                    attempt,
                    (),
                    f"transport error: {last_transport_error}",
                )
        except UnsafeUrlError as error:
            prefix = "unsafe URL" if current_url == requested_url else "unsafe redirect target"
            return _http_error(
                requested_url,
                current_url,
                None,
                attempt,
                redirects,
                f"{prefix}: {error}",
            )

    raise AssertionError("retry loop exhausted unexpectedly")
