# Talking to Kids About AI — A Parent Manual

A plain-English, kitchen-table guide for parents talking with kids and teens about AI: what AI actually is, homework honesty and school policies, chatbots-as-friend warnings, sharing rules (photos, names, feelings), spotting a bad AI interaction, setting family defaults together, and a first-account checklist for when your kid is old enough.

By **Asdale Dynamics, LLC** — beginner-friendly AI education, explained like a friend would: plain English, step by step, never condescending.

## What's inside

| Page | What it covers |
|------|----------------|
| [docs/01-what-ai-actually-is.md](docs/01-what-ai-actually-is.md) | The kitchen-table explanation of AI, what it's good/bad at, kid questions answered |
| [docs/02-homework-honesty-and-school-policies.md](docs/02-homework-honesty-and-school-policies.md) | Finding your school's policy, honest vs dishonest use, disclosure |
| [docs/03-when-a-chatbot-feels-like-a-friend.md](docs/03-when-a-chatbot-feels-like-a-friend.md) | Why chatbots feel like friends, warning signs, what to say, 988 |
| [docs/04-sharing-rules-photos-names-feelings.md](docs/04-sharing-rules-photos-names-feelings.md) | The one rule that covers photos, names, locations, and feelings |
| [docs/05-spotting-a-bad-ai-interaction.md](docs/05-spotting-a-bad-ai-interaction.md) | Five red flags, the tell-me rule, what to do with a bad chat |
| [docs/06-setting-family-defaults-together.md](docs/06-setting-family-defaults-together.md) | The 30-minute kitchen-table meeting and seven family defaults |
| [docs/07-first-account-checklist.md](docs/07-first-account-checklist.md) | Before/during/after your kid's first AI account, monthly reviews |
| [docs/age-band-scripts.md](docs/age-band-scripts.md) | Actual scripts for ages 6–9, 10–12, 13–15, 16–18 |
| [docs/family-agreement-sheet.md](docs/family-agreement-sheet.md) | Printable one-page family AI agreement to sign together |
| [docs/glossary.md](docs/glossary.md) | Every AI word in parent-sized sentences |

## How to use it

Written to be read at home, away from a screen where possible:

1. Read [What AI Actually Is](docs/01-what-ai-actually-is.md) yourself (~10 minutes).
2. Print the [Family Agreement Sheet](docs/family-agreement-sheet.md).
3. Hold the kitchen-table meeting using [Setting Family Defaults Together](docs/06-setting-family-defaults-together.md), with the [age-band scripts](docs/age-band-scripts.md) in hand.

## Build the HTML site (local-first)

Everything is markdown plus a tiny build script. No accounts, no analytics, nothing leaves your computer.

```bash
pip install markdown      # only dependency
python3 build.py          # builds site/ from docs/
python3 build.py --check  # same, but fails on broken internal links
python3 -m unittest test_build.py -v   # run the test suite
```

The build outputs a static site to `site/` — 11 HTML pages with shared navigation and print styles (the [agreement sheet](docs/family-agreement-sheet.md) prints as one clean page).

## Related projects

- **free-teen-life-skills-pack** — the companion to this manual: the money, work, and independent-living skills a teen needs alongside these AI conversations.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Educational material only — not legal, medical, or mental-health advice.
