# Microsoft Interview Questions

A daily Microsoft-style DSA interview question, picked automatically by my
`/dsa-daily` Clawpilot skill and published here for me to access from any
device — phone, tablet, anything with a browser.

🌐 **Live site:** see the GitHub Pages URL in the repo's "About" sidebar.

## What's here

- **`playground/`** — one Python file per question. Each file has:
  1. Problem statement (module docstring)
  2. `Solution` class boilerplate (`raise NotImplementedError`)
  3. Unittest suite (must pass when you've solved it)
  4. `REFERENCE` string at the bottom with the canonical solution + interview tips
- **`visualizers/`** — optional interactive HTML animations for problems where seeing the algorithm step-by-step locks it into memory.
- **`state/`** — rotation state and curated seed problems used by the daily picker.
- **`index.html` + `assets/`** — the website. Pure HTML/CSS/JS; no build step.
- **`scripts/build_manifest.py`** — regenerates `manifest.json` from `state/state.json`. The website reads `manifest.json` to populate its nav.

## How the website works

1. `index.html` loads `manifest.json` (list of all questions, newest first).
2. Default route opens **today's question** (or the most recent if today's hasn't been picked yet).
3. Each question is rendered with 4 collapsible sections:
   - 📖 **Problem** — from the file's docstring
   - ⌨️ **Boilerplate** — the `Solution` class with `NotImplementedError` bodies
   - ✅ **Tests** — the unittest suite
   - 💡 **Solution** — **hidden by default**; click "Reveal solution" only after attempting the problem
4. Sidebar navigates to any past question. URL hash (`#YYYY-MM-DD-slug`) is shareable / bookmarkable.

## Single source of truth

The `playground/*.py` files are canonical. The website **parses them at runtime in the browser** — there is no duplicate solution markdown anywhere.

## Daily flow

Every day my Clawpilot `/dsa-daily` skill:

1. Picks a fresh LeetCode Medium for today's rotated data-structure.
2. Generates `playground/<date>-<slug>.py`.
3. Updates `state/state.json`.
4. Runs `python scripts/build_manifest.py` to refresh `manifest.json`.
5. `git add . && git commit && git push` — GitHub Pages redeploys, the site updates.

## Local preview

```powershell
cd <repo>
python -m http.server 8000
# open http://localhost:8000/
```

## Adding a visualizer

Drop `visualizers/<date>-<slug>.html` into the folder. The next `build_manifest.py`
run will detect it and the website will show a "🎬 Visualizer" link on that
question's page.
