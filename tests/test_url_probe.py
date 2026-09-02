import socket
import unittest
from unittest.mock import patch

from scripts.url_probe import (
    Outcome,
    RawResponse,
    UnsafeUrlError,
    probe_url,
    request_once,
    validate_public_url,
)


PUBLIC_URL = "https://example.test/start"


def public_validation(url: str):
    return "example.test", 443, "8.8.8.8"


class SequenceRequester:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.urls = []

    def __call__(self, url, timeout):
        self.urls.append((url, timeout))
        result = next(self.responses)
        if isinstance(result, BaseException):
            raise result
        return result


class UrlProbeTests(unittest.TestCase):
    def test_changed_301_canonical_target_is_a_permanent_redirect(self):
        requester = SequenceRequester(
            [
                RawResponse(301, "https://www.example.test/guide/"),
                RawResponse(200, None),
            ]
        )

        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            observation = probe_url(PUBLIC_URL, requester=requester, sleeper=lambda _: None)

        self.assertEqual(observation.outcome, Outcome.PERMANENT_REDIRECT)
        self.assertEqual(observation.final_url, "https://www.example.test/guide/")
        self.assertEqual(observation.status, 200)
        self.assertEqual(observation.attempts, 1)

    def test_retryable_http_status_uses_all_three_attempts(self):
        requester = SequenceRequester([RawResponse(503, None)] * 3)
        delays = []

        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            observation = probe_url(
                PUBLIC_URL, requester=requester, sleeper=delays.append
            )

        self.assertEqual(observation.outcome, Outcome.TRANSIENT)
        self.assertEqual(observation.status, 503)
        self.assertEqual(observation.attempts, 3)
        self.assertEqual(delays, [0, 1, 2])

    def test_terminal_statuses_are_classified_without_retry(self):
        cases = [
            (404, Outcome.DEAD),
            (410, Outcome.DEAD),
            (401, Outcome.RESTRICTED),
            (403, Outcome.RESTRICTED),
            (407, Outcome.RESTRICTED),
            (429, Outcome.RESTRICTED),
            (451, Outcome.RESTRICTED),
            (418, Outcome.HTTP_ERROR),
        ]

        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            for status, expected in cases:
                with self.subTest(status=status):
                    observation = probe_url(
                        PUBLIC_URL,
                        requester=SequenceRequester([RawResponse(status, None)]),
                        sleeper=lambda _: None,
                    )
                    self.assertEqual(observation.outcome, expected)
                    self.assertEqual(observation.attempts, 1)

    def test_temporary_redirect_to_success_is_ok(self):
        requester = SequenceRequester(
            [RawResponse(302, "/next"), RawResponse(200, None)]
        )

        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            observation = probe_url(PUBLIC_URL, requester=requester, sleeper=lambda _: None)

        self.assertEqual(observation.outcome, Outcome.OK)
        self.assertEqual(observation.final_url, "https://example.test/next")

    def test_private_dns_answer_is_rejected(self):
        answers = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))]

        with patch("scripts.url_probe.socket.getaddrinfo", return_value=answers):
            with self.assertRaisesRegex(
                UnsafeUrlError, "resolved address is not globally routable"
            ):
                validate_public_url(PUBLIC_URL)

    def test_dns_resolution_failures_are_retried_as_transient(self):
        delays = []

        with patch(
            "scripts.url_probe.socket.getaddrinfo",
            side_effect=socket.gaierror("no dns"),
        ) as getaddrinfo:
            observation = probe_url(PUBLIC_URL, sleeper=delays.append)

        self.assertEqual(observation.outcome, Outcome.TRANSIENT)
        self.assertEqual(observation.attempts, 3)
        self.assertEqual(observation.error, "transport error: gaierror")
        self.assertEqual(delays, [0, 1, 2])
        self.assertEqual(getaddrinfo.call_count, 3)

    def test_default_requester_revalidation_failure_is_an_http_error(self):
        public_answer = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))
        ]
        private_answer = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))
        ]

        with patch(
            "scripts.url_probe.socket.getaddrinfo",
            side_effect=[public_answer, private_answer],
        ) as getaddrinfo:
            observation = probe_url(PUBLIC_URL, sleeper=lambda _: None)

        self.assertEqual(observation.outcome, Outcome.HTTP_ERROR)
        self.assertEqual(observation.attempts, 1)
        self.assertEqual(
            observation.error,
            "unsafe URL: resolved address is not globally routable",
        )
        self.assertEqual(getaddrinfo.call_count, 2)

    def test_missing_redirect_location_is_an_http_error(self):
        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            observation = probe_url(
                PUBLIC_URL,
                requester=SequenceRequester([RawResponse(302, None)]),
                sleeper=lambda _: None,
            )

        self.assertEqual(observation.outcome, Outcome.HTTP_ERROR)
        self.assertEqual(observation.error, "missing redirect location")

    def test_redirect_loop_and_limit_are_http_errors(self):
        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            loop = probe_url(
                PUBLIC_URL,
                requester=SequenceRequester([RawResponse(302, "/start")]),
                sleeper=lambda _: None,
            )
            overflow = probe_url(
                PUBLIC_URL,
                requester=SequenceRequester([RawResponse(302, f"/hop-{index}") for index in range(6)]),
                sleeper=lambda _: None,
            )

        self.assertEqual(loop.outcome, Outcome.HTTP_ERROR)
        self.assertEqual(loop.error, "redirect loop")
        self.assertEqual(overflow.outcome, Outcome.HTTP_ERROR)
        self.assertEqual(overflow.error, "redirect limit exceeded")

    def test_transport_failures_use_all_three_attempts(self):
        requester = SequenceRequester(
            [socket.gaierror("no dns"), OSError("reset"), TimeoutError("late")]
        )
        delays = []

        with patch("scripts.url_probe.validate_public_url", side_effect=public_validation):
            observation = probe_url(
                PUBLIC_URL, requester=requester, sleeper=delays.append
            )

        self.assertEqual(observation.outcome, Outcome.TRANSIENT)
        self.assertEqual(observation.attempts, 3)
        self.assertEqual(delays, [0, 1, 2])
        self.assertEqual(observation.error, "transport error: TimeoutError")

    def test_request_once_falls_back_to_get_for_unsupported_head(self):
        calls = []

        class Response:
            def __init__(self, status):
                self.status = status

            def getheader(self, name):
                return "/redirect" if name == "Location" else None

            def close(self):
                calls.append("response-close")

        class Connection:
            def __init__(self, *args, **kwargs):
                calls.append(("connect", args, kwargs))

            def request(self, method, target, headers):
                calls.append((method, target, headers))

            def getresponse(self):
                return Response(405 if len([call for call in calls if isinstance(call, tuple) and call[0] in {"HEAD", "GET"}]) == 1 else 200)

            def close(self):
                calls.append("connection-close")

        with (
            patch("scripts.url_probe.validate_public_url", return_value=("example.test", 443, "8.8.8.8")),
            patch("scripts.url_probe._PinnedHTTPSConnection", Connection),
        ):
            response = request_once("https://example.test/path?x=1", timeout=7)

        self.assertEqual(response, RawResponse(200, "/redirect"))
        self.assertEqual([call[0] for call in calls if isinstance(call, tuple) and call[0] in {"HEAD", "GET"}], ["HEAD", "GET"])
        request = next(call for call in calls if isinstance(call, tuple) and call[0] == "GET")
        self.assertEqual(request[1], "/path?x=1")
        self.assertEqual(request[2]["Host"], "example.test")
        self.assertEqual(request[2]["User-Agent"], "awesome-quant-url-audit/1.0")

    def test_public_redirect_to_private_target_is_an_http_error(self):
        def validate(url):
            if url == "https://example.test/private":
                raise UnsafeUrlError("resolved address is not globally routable")
            return public_validation(url)

        with patch("scripts.url_probe.validate_public_url", side_effect=validate):
            observation = probe_url(
                PUBLIC_URL,
                requester=SequenceRequester([RawResponse(302, "/private")]),
                sleeper=lambda _: None,
            )

        self.assertEqual(observation.outcome, Outcome.HTTP_ERROR)
        self.assertEqual(
            observation.error,
            "unsafe redirect target: resolved address is not globally routable",
        )


if __name__ == "__main__":
    unittest.main()
