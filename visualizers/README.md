# DSA Daily — Visualizers

Self-contained interactive HTML animations for problems where seeing the algorithm step-by-step locks it into memory better than reading code.

## File naming

`<YYYY-MM-DD>-<leetcode-slug>.html` — matches the corresponding `playground/<date>-<slug>.py`.

## Conventions

- **One HTML file per problem.** Fully self-contained — no CDN, no external JS, no internet needed. Double-click to open in any browser.
- **Clawpilot theme.** Every file uses the `--cp-*` CSS variables and the auto-detect `data-theme` script (light/dark follows your OS, override via `?clawpilotTheme=dark`).
- **Step + Play + Reset controls** at minimum, plus a speed slider.
- **Synced code panel** — the Python/pseudo-code on the right highlights the line currently executing on the left.
- **Plain-English narration** under the canvas — one sentence per step explaining what just happened.

## Workflow

When you want to recall how a problem works, open the visualizer instead of (or before) reading the playground `.py`:

```powershell
# Pick the visualizer for the question you want to revisit
start C:\Users\bhushanidhi\.copilot\skills\dsa-daily\visualizers\2026-05-14-number-of-islands.html
```

Then scroll to the `playground/<date>-<slug>.py` if you want to code it from scratch.

## Current visualizers

| Date | Problem | File |
|---|---|---|
| 2026-05-14 | #200 Number of Islands (DFS flood-fill) | `2026-05-14-number-of-islands.html` |

## Asking for a new visualizer

When a problem feels non-intuitive, say something like *"build a visualizer for today's problem"* — I'll generate a new HTML in this folder using the same conventions (theme, controls, narration, code sync).
