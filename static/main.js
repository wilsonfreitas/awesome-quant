/* awesome-quant – search, filter, sort, expand */
(function () {
  "use strict";

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  const searchInput = $("#search");
  const filterBar = $("#filter-bar");
  const filterValue = $("#filter-value");
  const filterClear = $("#filter-clear");
  const noResults = $("#no-results");
  const resultsCount = $("#results-count");
  const tableBody = $("tbody", $("#project-table"));
  const sortHeaders = $$("th[data-sort]");

  let activeFilter = { type: "", value: "" };
  let currentSort = { key: "", dir: "" };

  // ===== Theme =====
  const themeToggle = $(".theme-toggle");

  function getPreferredTheme() {
    const stored = localStorage.getItem("theme");
    if (stored) return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }

  applyTheme(getPreferredTheme());

  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
  });

  // ===== Helpers =====
  function getRows() {
    return $$(".row", tableBody);
  }

  function getExpandRow(row) {
    return row.nextElementSibling;
  }

  function collapseAll() {
    for (const row of getRows()) {
      row.classList.remove("expanded");
      const expand = getExpandRow(row);
      if (expand) expand.hidden = true;
    }
  }

  // ===== Search & Filter =====
  let searchTimeout;

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    let visible = 0;

    collapseAll();

    for (const row of getRows()) {
      const expand = getExpandRow(row);
      const text = (
        row.textContent +
        " " +
        (expand ? expand.textContent : "")
      ).toLowerCase();
      const language = row.dataset.language || "";
      const category = row.dataset.category || "";
      const sources = row.dataset.sources || "";

      let show = true;

      // Search
      if (query && !text.includes(query)) show = false;

      // Tag filter
      if (show && activeFilter.value) {
        const ft = activeFilter.type;
        const fv = activeFilter.value;
        if (ft === "language" && language !== fv) show = false;
        if (ft === "category" && category !== fv) show = false;
        if (ft === "source" && !sources.split(" ").includes(fv)) show = false;
      }

      row.hidden = !show;
      if (expand) expand.hidden = true;

      if (show) {
        visible++;
        const numCell = $(".col-num", row);
        if (numCell) numCell.textContent = visible;
      }
    }

    noResults.hidden = visible > 0;
    resultsCount.textContent =
      query || activeFilter.value
        ? `Showing ${visible} project${visible !== 1 ? "s" : ""}`
        : "";

    // Sync filter bar
    if (activeFilter.value) {
      filterValue.textContent = activeFilter.value;
      filterBar.style.display = "flex";
    } else {
      filterBar.style.display = "none";
    }

    syncURL();
  }

  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(applyFilters, 120);
  });

  filterClear.addEventListener("click", () => {
    activeFilter = { type: "", value: "" };
    applyFilters();
  });

  // ===== Tag Click =====
  tableBody.addEventListener("click", (e) => {
    const tag = e.target.closest(".tag");
    if (tag) {
      e.stopPropagation();
      const type = tag.dataset.filterType;
      const value = tag.dataset.filterValue;

      // Toggle off if same filter
      if (activeFilter.type === type && activeFilter.value === value) {
        activeFilter = { type: "", value: "" };
      } else {
        activeFilter = { type, value };
      }
      applyFilters();
      return;
    }
  });

  // ===== Row Expand =====
  tableBody.addEventListener("click", (e) => {
    if (e.target.closest(".tag") || e.target.closest("a")) return;
    const row = e.target.closest(".row");
    if (!row) return;

    const expand = getExpandRow(row);
    if (!expand) return;

    const isExpanded = row.classList.contains("expanded");

    for (const r of getRows()) {
      if (r !== row) {
        r.classList.remove("expanded");
        const ex = getExpandRow(r);
        if (ex) ex.hidden = true;
      }
    }

    if (isExpanded) {
      row.classList.remove("expanded");
      expand.hidden = true;
    } else {
      row.classList.add("expanded");
      expand.hidden = false;
    }
  });

  tableBody.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      const row = e.target.closest(".row");
      if (row) {
        e.preventDefault();
        row.click();
      }
    }
  });

  // ===== Sort =====
  function getSortValue(row, key) {
    if (key === "name") {
      return ($(".col-name a", row)?.textContent || "").toLowerCase();
    }
    if (key === "stars") {
      return parseInt(row.dataset.stars || "0", 10);
    }
    if (key === "update") {
      return ($(".last-update", row)?.textContent || "").trim();
    }
    return "";
  }

  function doSort(key, dir) {
    const rows = getRows();
    const pairs = rows.map((r) => [r, getExpandRow(r)]);

    if (!dir) {
      pairs.sort((a, b) => {
        const ai = parseInt(a[0].dataset.originalIndex || "0");
        const bi = parseInt(b[0].dataset.originalIndex || "0");
        return ai - bi;
      });
    } else {
      pairs.sort((a, b) => {
        const va = getSortValue(a[0], key);
        const vb = getSortValue(b[0], key);
        let cmp;
        if (typeof va === "number" && typeof vb === "number") {
          cmp = va - vb;
        } else {
          cmp = String(va).localeCompare(String(vb));
        }
        return dir === "asc" ? cmp : -cmp;
      });
    }

    for (const [row, expand] of pairs) {
      tableBody.appendChild(row);
      if (expand) tableBody.appendChild(expand);
    }

    applyFilters();
  }

  for (const th of sortHeaders) {
    th.addEventListener("click", () => {
      const key = th.dataset.sort;

      let nextDir;
      if (currentSort.key !== key) {
        nextDir = key === "name" ? "asc" : "desc";
      } else if (currentSort.dir === "asc") {
        nextDir = "desc";
      } else if (currentSort.dir === "desc") {
        nextDir = key === "name" ? "" : "asc";
      } else {
        nextDir = key === "name" ? "asc" : "desc";
      }

      for (const h of sortHeaders) {
        h.classList.remove("asc", "desc");
      }

      if (nextDir) {
        th.classList.add(nextDir);
      }

      currentSort = { key: nextDir ? key : "", dir: nextDir };
      doSort(key, nextDir);
    });
  }

  // Store original indices
  getRows().forEach((r, i) => (r.dataset.originalIndex = i));

  // ===== Keyboard Shortcuts =====
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !e.ctrlKey && !e.metaKey) {
      const active = document.activeElement;
      if (
        active &&
        (active.tagName === "INPUT" ||
          active.tagName === "SELECT" ||
          active.tagName === "TEXTAREA")
      )
        return;
      e.preventDefault();
      searchInput.focus();
    }

    if (e.key === "Escape") {
      if (document.activeElement === searchInput) {
        if (searchInput.value) {
          searchInput.value = "";
          applyFilters();
        } else {
          searchInput.blur();
        }
      }
    }
  });

  // ===== URL State =====
  function syncURL() {
    const params = new URLSearchParams();
    if (searchInput.value) params.set("q", searchInput.value);
    if (activeFilter.value) {
      params.set("filter_type", activeFilter.type);
      params.set("filter", activeFilter.value);
    }
    const qs = params.toString();
    const url = qs ? `?${qs}` : location.pathname;
    history.replaceState(null, "", url);
  }

  function restoreURL() {
    const params = new URLSearchParams(location.search);
    if (params.has("q")) searchInput.value = params.get("q");
    if (params.has("filter")) {
      activeFilter = {
        type: params.get("filter_type") || "category",
        value: params.get("filter"),
      };
    }
    if (params.toString()) applyFilters();
  }

  restoreURL();
})();
