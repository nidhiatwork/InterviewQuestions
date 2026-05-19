/* =====================================================================
   Microsoft Interview Questions — single-page app
   ===================================================================== */
"use strict";

const state = {
  questions: [],   // sorted desc by date
  current: null,
};

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

// -------------------- theme toggle --------------------
$("#themeToggle").addEventListener("click", () => {
  const cur = document.documentElement.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("dsa-theme", next);
  applyHljsTheme();
});

function applyHljsTheme() {
  const dark = document.documentElement.getAttribute("data-theme") === "dark";
  $("#hl-light").disabled = dark;
  $("#hl-dark").disabled = !dark;
}
applyHljsTheme();

// -------------------- mobile nav --------------------
const sidebar = $("#sidebar");
const overlay = $("#overlay");
$("#navToggle").addEventListener("click", () => {
  sidebar.classList.toggle("open");
  overlay.classList.toggle("open");
});
overlay.addEventListener("click", () => {
  sidebar.classList.remove("open");
  overlay.classList.remove("open");
});

function closeMobileNav() {
  sidebar.classList.remove("open");
  overlay.classList.remove("open");
}

// -------------------- bootstrap --------------------
async function init() {
  try {
    const res = await fetch("manifest.json", { cache: "no-store" });
    if (!res.ok) throw new Error("manifest.json missing");
    const manifest = await res.json();
    state.questions = (manifest.questions || []).slice().sort((a, b) => b.date.localeCompare(a.date));
    if (manifest.repoUrl) $("#repoLink").href = manifest.repoUrl;
    renderSidebar();
    routeFromHash();
  } catch (err) {
    $("#content").innerHTML = `<div class="loading-page">Failed to load questions: ${err.message}</div>`;
  }
}

window.addEventListener("hashchange", routeFromHash);

function routeFromHash() {
  const hash = (window.location.hash || "").replace(/^#/, "");
  if (!hash || hash === "today") {
    const today = todayISO();
    const t = state.questions.find(q => q.date === today) || state.questions[0];
    if (t) {
      renderQuestion(t);
    } else {
      renderWelcome();
    }
    return;
  }
  const q = state.questions.find(q => entryId(q) === hash);
  if (q) renderQuestion(q);
  else renderWelcome();
}

function todayISO() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function entryId(q) { return `${q.date}-${q.slug}`; }

// -------------------- sidebar --------------------
function renderSidebar() {
  const list = $("#navList");
  list.innerHTML = "";
  const today = todayISO();
  state.questions.forEach(q => {
    const a = document.createElement("a");
    a.className = "nav-link";
    a.href = `#${entryId(q)}`;
    const isToday = q.date === today;
    a.innerHTML = `
      <span class="nav-date">${formatDateShort(q.date)}${isToday ? " · today" : ""}</span>
      <span><span class="nav-ds">${escapeHtml(q.dataStructure)}</span>${escapeHtml(q.title)}</span>
    `;
    a.dataset.id = entryId(q);
    a.addEventListener("click", closeMobileNav);
    list.appendChild(a);
  });
}

function highlightActive(id) {
  $$(".nav-list .nav-link").forEach(a => a.classList.toggle("active", a.dataset.id === id));
}

function formatDateShort(iso) {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

// -------------------- welcome --------------------
function renderWelcome() {
  const tpl = $("#welcomeTemplate").content.cloneNode(true);
  const content = $("#content");
  content.innerHTML = "";
  content.appendChild(tpl);
  highlightActive(null);
}

// -------------------- render one question --------------------
async function renderQuestion(q) {
  highlightActive(entryId(q));
  const content = $("#content");
  content.innerHTML = `<div class="loading-page">Loading ${escapeHtml(q.title)}…</div>`;

  try {
    const rawUrl = `playground/${encodeURIComponent(q.filename)}`;
    const res = await fetch(rawUrl, { cache: "no-store" });
    if (!res.ok) throw new Error(`Could not fetch ${q.filename}`);
    const text = await res.text();
    const parsed = parsePyFile(text);

    const tpl = $("#questionTemplate").content.cloneNode(true);
    tpl.querySelector("[data-ds]").textContent = q.dataStructure;
    tpl.querySelector("[data-diff]").textContent = q.difficulty || "Medium";
    tpl.querySelector("[data-date]").textContent = formatDateShort(q.date);
    tpl.querySelector("[data-lcid]").textContent = `#${q.leetcodeId}`;
    tpl.querySelector("[data-title]").textContent = q.title;
    tpl.querySelector("[data-leet]").href = q.url;
    tpl.querySelector("[data-raw]").href = rawUrl;

    if (q.hasVisualizer) {
      const v = tpl.querySelector("[data-viz]");
      v.href = `visualizers/${q.date}-${q.slug}.html`;
      v.hidden = false;
    }

    tpl.querySelector("[data-problem]").textContent = parsed.problem || "(no problem statement found)";
    tpl.querySelector("[data-boilerplate]").textContent = parsed.boilerplate || "(no boilerplate found)";
    tpl.querySelector("[data-tests]").textContent = parsed.tests || "(no tests found)";
    tpl.querySelector("[data-reference]").textContent = parsed.reference || "(no reference solution found)";

    const revealBtn = tpl.querySelector("[data-reveal]");
    const solutionBody = tpl.querySelector("[data-solution]");
    revealBtn.addEventListener("click", () => {
      solutionBody.hidden = false;
      revealBtn.hidden = true;
      window.hljs && window.hljs.highlightElement(solutionBody.querySelector("code"));
      solutionBody.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    content.innerHTML = "";
    content.appendChild(tpl);

    // syntax highlight problem/boilerplate/tests immediately; solution on reveal
    if (window.hljs) {
      $$("code.language-python", content).forEach(el => {
        if (!el.closest(".solution-body")) window.hljs.highlightElement(el);
      });
    }

    document.title = `${q.title} · Microsoft Interview Questions`;
    window.scrollTo({ top: 0 });
  } catch (err) {
    content.innerHTML = `<div class="loading-page">⚠ Failed to load question: ${escapeHtml(err.message)}</div>`;
  }
}

// -------------------- parse playground .py file --------------------
function parsePyFile(text) {
  const result = { problem: "", boilerplate: "", tests: "", reference: "" };

  // 1) Module docstring = first """...""" block at file start
  const docMatch = text.match(/^"""([\s\S]*?)"""/);
  let cursor = 0;
  if (docMatch) {
    result.problem = docMatch[1].trim();
    cursor = docMatch[0].length;
  }

  // 2) Find tests marker comment
  const testsMarker = text.match(/# -+\s*tests\s*-+/i);
  const testsIdx = testsMarker ? testsMarker.index : -1;

  // 3) Find helpers marker (some files have helpers between boilerplate and tests)
  const helpersMarker = text.match(/# -+\s*helpers\s*-+/i);
  const helpersIdx = helpersMarker ? helpersMarker.index : -1;

  // 4) Find REFERENCE marker
  const refMarker = text.match(/REFERENCE\s*=\s*"""/);
  const refIdx = refMarker ? refMarker.index : -1;

  // 5) Find banner comment above REFERENCE (preferred end of tests)
  const banner = text.match(/# =+\s*\r?\n# REFERENCE[\s\S]*?# =+/);
  const bannerIdx = banner ? banner.index : -1;

  // Boilerplate = from after docstring up to first marker (helpers or tests)
  const boilerEnd = (helpersIdx > 0 ? helpersIdx : (testsIdx > 0 ? testsIdx : (bannerIdx > 0 ? bannerIdx : text.length)));
  result.boilerplate = text.substring(cursor, boilerEnd).trim();
  // If helpers exist, include them visually with boilerplate (they're test-support code, not solution)
  if (helpersIdx > 0 && testsIdx > 0) {
    // append helpers to boilerplate section
    result.boilerplate += "\n\n" + text.substring(helpersIdx, testsIdx).trim();
  }

  // Tests = from tests marker to banner (or REFERENCE)
  if (testsIdx >= 0) {
    const testsEnd = bannerIdx > 0 ? bannerIdx : (refIdx > 0 ? refIdx : text.length);
    result.tests = text.substring(testsIdx, testsEnd).trim();
  }

  // Reference = inside the triple-quoted string after REFERENCE = """
  if (refIdx >= 0) {
    const start = refIdx + refMarker[0].length;
    const end = text.indexOf('"""', start);
    if (end >= 0) result.reference = text.substring(start, end).trim();
  }

  return result;
}

// -------------------- utils --------------------
function escapeHtml(str) {
  if (str == null) return "";
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

init();
