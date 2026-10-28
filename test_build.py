#!/usr/bin/env python3
"""Tests for the Talking to Kids About AI guide build.

Run with:  python3 -m unittest test_build.py -v
Uses only the Python standard library + the project's own build.py.
"""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

REQUIRED_PAGES = {
    "index": ["start here", "how to use this manual"],
    "01-what-ai-actually-is": [
        "kitchen-table", "autocomplete", "hallucination", "does it have a brain",
    ],
    "02-homework-honesty-and-school-policies": [
        "policy", "teacher", "disclosure", "disclose",
    ],
    "03-when-a-chatbot-feels-like-a-friend": [
        "friend", "988", "mirror",
    ],
    "04-sharing-rules-photos-names-feelings": [
        "photo", "name", "feelings", "poster",
    ],
    "05-spotting-a-bad-ai-interaction": [
        "red flag", "screenshot", "secret",
    ],
    "06-setting-family-defaults-together": [
        "together", "defaults", "agreement sheet",
    ],
    "07-first-account-checklist": [
        "checklist", "account", "privacy", "password",
    ],
    "age-band-scripts": [
        "ages 6", "ages 10", "ages 13", "ages 16",
    ],
    "family-agreement-sheet": [
        "signature", "988",
    ],
    "glossary": [
        "hallucination", "chatbot", "prompt", "deepfake",
        "large language model", "terms of service",
    ],
}

INTERNAL_RE = re.compile(r'href="([^"#]+\.html)"')


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build into a temp dir so we never leave partial output in the repo
        # tree; assertions on repo state use the real SITE built last.
        cls.tmp = Path(tempfile.mkdtemp(prefix="ttk-build-"))
        import build as build_module
        cls.orig_site = build_module.SITE
        build_module.SITE = cls.tmp / "site"
        cls.built = build_module.build(check_links=True)
        cls.built_files = sorted(p.name for p in build_module.SITE.glob("*.html"))
        cls.site = build_module.SITE
        cls._orig_site_saved = build_module.SITE

    @classmethod
    def tearDownClass(cls):
        import build as build_module
        build_module.SITE = cls.orig_site
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def docs_text(self, stem: str) -> str:
        return (DOCS / f"{stem}.md").read_text(encoding="utf-8")

    def html_text(self, stem: str) -> str:
        return (self.site / f"{stem}.html").read_text(encoding="utf-8")

    # --- build mechanics -------------------------------------------------

    def test_builds_all_entries(self):
        expected = set(REQUIRED_PAGES)
        self.assertEqual(expected, set(self.built))

    def test_site_contains_one_html_per_doc(self):
        doc_stems = sorted(p.stem for p in DOCS.glob("*.md"))
        self.assertEqual(doc_stems, sorted(Path(f).stem for f in self.built_files))

    def test_every_htmlpage_is_complete_document(self):
        for name in self.built_files:
            html = (self.site / name).read_text(encoding="utf-8")
            self.assertTrue(html.lstrip().lower().startswith("<!doctype html"),
                            msg=name)
            self.assertIn("</html>", html, msg=name)

    def test_no_broken_internal_links(self):
        for name in self.built_files:
            html = (self.site / name).read_text(encoding="utf-8")
            for target in INTERNAL_RE.findall(html):
                tgt = Path(target).name
                self.assertTrue((self.site / tgt).exists(),
                                msg=f"{name} -> {target}")

    def test_nav_on_every_page(self):
        for name in self.built_files:
            html = (self.site / name).read_text(encoding="utf-8")
            self.assertIn('class="pages"', html, msg=name)
            self.assertIn('href="index.html"', html, msg=name)

    def test_footers_carry_copyright(self):
        for name in self.built_files:
            html = (self.site / name).read_text(encoding="utf-8")
            self.assertIn("Asdale Dynamics, LLC", html, msg=name)
            self.assertIn("Copyright (c) 2026", html, msg=name)

    def test_checkboxes_render_as_inputs(self):
        html = self.html_text("family-agreement-sheet")
        self.assertGreaterEqual(html.count('type="checkbox"'), 8)

    def test_agreement_sheet_has_signature_fields(self):
        html = self.html_text("family-agreement-sheet")
        self.assertGreaterEqual(html.count("____"), 10)

    def test_meta_description_present(self):
        html = self.html_text("index")
        self.assertIn('name="description"', html)

    # --- content requirements --------------------------------------------

    def test_required_topics_covered(self):
        for stem, keywords in REQUIRED_PAGES.items():
            text = self.docs_text(stem).lower()
            for kw in keywords:
                self.assertIn(kw, text, msg=f"{stem}.md missing keyword: {kw!r}")

    def test_goal_topics_all_present_as_files(self):
        must_exist = [
            "01-what-ai-actually-is",            # what AI actually is
            "02-homework-honesty-and-school-policies",  # homework honesty
            "03-when-a-chatbot-feels-like-a-friend",    # chatbots-as-friend
            "04-sharing-rules-photos-names-feelings",   # sharing rules
            "05-spotting-a-bad-ai-interaction",         # bad interaction
            "06-setting-family-defaults-together",      # family defaults
            "07-first-account-checklist",               # first account
            "age-band-scripts",
            "family-agreement-sheet",
            "glossary",
        ]
        for stem in must_exist:
            self.assertTrue((DOCS / f"{stem}.md").exists(), msg=stem)

    def test_cross_references_resolve_in_markdown(self):
        for src in DOCS.glob("*.md"):
            text = src.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)#\s]+\.html)\)", text):
                stem = Path(target).stem
                self.assertTrue((DOCS / f"{stem}.md").exists(),
                                msg=f"{src.name} -> {target}")

    def test_age_bands_listing(self):
        text = self.docs_text("age-band-scripts")
        for band in ("6–9", "10–12", "13–15", "16–18"):
            self.assertIn(band, text)

    def test_free_teen_life_skills_pack_companion_is_mentioned(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
        index_doc = self.docs_text("index")
        self.assertIn("free-teen-life-skills-pack", readme + index_doc)

    # --- hygiene ----------------------------------------------------------

    def test_no_secret_looking_strings(self):
        patterns = [
            r"sk-[A-Za-z0-9]{10,}",        # openai-style keys
            r"api[_-]?key\s*[:=]\s*\S+",
            r"AKIA[0-9A-Z]{12,}",          # AWS access keys
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
            r"[A-Za-z0-9._%+-]+@(?!example)[a-z0-9.-]+\.[a-z]{2,}\b",
        ]
        for src in DOCS.glob("*.md"):
            text = src.read_text(encoding="utf-8")
            for pat in patterns:
                self.assertIsNone(re.search(pat, text),
                                  msg=f"{src.name} matches {pat!r}")

    def test_docs_are_not_empty_or_stubbed(self):
        for src in DOCS.glob("*.md"):
            text = src.read_text(encoding="utf-8")
            self.assertGreater(len(text), 1500, msg=f"{src.name} too short")
            self.assertNotIn("TODO", text, msg=src.name)
            self.assertNotIn("lorem ipsum", text.lower(), msg=src.name)

    # --- packaging ----------------------------------------------------------

    def test_license_line_is_exact(self):
        lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", lic)
        self.assertTrue(lic.startswith("MIT License"))

    def test_readme_credits_and_mentions_build(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("python3 build.py", readme)
        self.assertIn("free-teen-life-skills-pack", readme)

    def test_status_md_exists(self):
        self.assertTrue((ROOT / "STATUS.md").exists())


if __name__ == "__main__":
    unittest.main()
