# STATUS.md

**Project:** Talking to Kids About AI — Parent Manual
**Owner:** Asdale Dynamics, LLC
**Last verified:** 2026-10-28
**State:** Complete and verified — build passes, test suite passes (19 tests, run locally on Python 3.13).

## What was built

A self-contained, local-first parent manual for AI conversations with kids and teens. Markdown source in `docs/`, built into a static HTML site in `site/` via `build.py`. No accounts, no analytics, no network calls at build time (one dependency: the Python `markdown` package).

Content coverage (matches the original goal, item by item):

1. **What AI actually is, in kitchen-table words** — `docs/01-what-ai-actually-is.md` (definition, good-at/bad-at lists, real kid questions answered: "does it have a brain?", "can it lie?", etc.)
2. **Homework honesty and school policies** — `docs/02-homework-honesty-and-school-policies.md` (finding school policy, three honest / three dishonest uses, disclosure script, getting-caught repair steps)
3. **Chatbots-as-friend warnings** — `docs/03-when-a-chatbot-feels-like-a-friend.md` (why bots feel like friends, warning signs, 988 crisis guidance, what to say)
4. **Sharing rules (photos, names, feelings)** — `docs/04-sharing-rules-photos-names-feelings.md` ("poster at school" rule, photos/faces, names/identity, feelings, image-generator cautions)
5. **Spotting a bad AI interaction** — `docs/05-spotting-a-bad-ai-interaction.md` (five red flags, tell-me rule, screenshot/report/debrief steps)
6. **Setting family defaults together** — `docs/06-setting-family-defaults-together.md` (30-minute meeting plan, seven defaults, review cadence)
7. **First-account checklist** — `docs/07-first-account-checklist.md` (before/during/after first account, 30-day check-in, slowdown signs)
8. **Age-band scripts** — `docs/age-band-scripts.md` (verbatim scripts for ages 6–9, 10–12, 13–15, 16–18)
9. **Family agreement sheet** — `docs/family-agreement-sheet.md` (printable one-page co-signed agreement with checkboxes and signature fields)
10. **Glossary** — `docs/glossary.md` (AI, chatbot, hallucination, LLM, prompt, deepfake, ToS, parasocial, agent, etc.)

Plus: `README.md` (usage, page index, credit to Asdale Dynamics, LLC), `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"), `build.py`, `test_build.py`, and this `STATUS.md`. The manual is positioned as a companion to the free-teen-life-skills-pack (README + index page).

Build features: shared template with full-page navigation, print stylesheet (agreement sheet prints cleanly), real HTML checkboxes from markdown task lists, meta descriptions, internal-link checking (`--check`).

## How to run it

```bash
pip install markdown
python3 build.py          # build site/ from docs/
python3 build.py --check  # build + fail on broken internal links
python3 -m unittest test_build.py -v   # test suite
```

Open `site/index.html` in a browser to read the built site.

## Verification results (2026-10-28)

- `python3 build.py --check` — OK: 11 pages built, no broken internal links.
- `python3 -m unittest test_build.py -v` — OK: all 19 tests pass, covering:
  - build mechanics (one HTML per doc, complete documents, nav + footer on every page, checkbox conversion, meta descriptions)
  - content requirements (every goal topic file exists with keyword coverage; age bands 6–9/10–12/13–15/16–18 present; glossary terms present; markdown cross-references resolve)
  - hygiene (no secret-shaped strings, no placeholder text, min length per doc)
  - packaging (exact LICENSE line, README credit + build instructions, STATUS.md present)

## Known gaps

- **No live URLs verified beyond 988/findahelpline** — platform-specific age limits and settings menus change; the docs say "check the tool's current terms" rather than naming exact menu paths.
- **Single-locale bias** — crisis-line guidance defaults to US (988); other regions only get findahelpline.com. Localize as needed.
- **No PDF output** — agreement sheet prints nicely from the browser, but there's no generated PDF; add if wanted (e.g. weasyprint build target).
- **Accessibility pass is basic** — semantic HTML, one h1 per page, plain links; no screen-reader audit done.
- **Read-only AI-platform details** — the guides deliberately avoid naming specific products' features in detail so they don't date; that means less concrete hand-holding than some parents may want.
