"""Distribution checks for the standalone reference-first-figures skill repository.

These tests check the published package rather than the skill's behaviour: the
required resources are present, every relative Markdown link resolves inside the
repository, the skill metadata is readable, and no personal or cached files ship
with it. The reference corpus is the skill's evidence base, so each reference
document must stay readable and linked from SKILL.md.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "reference-first-figures"
REFERENCES = (
    "comparison-and-review.md",
    "micro-style.md",
    "nature-handoff.md",
    "search-and-selection.md",
    "sources.md",
    "workflow-handoff.md",
)
EXPECTED_ROOT = {
    ".github", ".gitignore", "LICENSE", "README.en.md", "README.md",
    "SKILL.md", "agents", "references", "tests",
}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BANNED_NAMES = {"__pycache__", "node_modules", ".venv", "venv", ".DS_Store"}
BANNED_SUFFIXES = (".pyc", ".pyo", ".log", ".zip", ".tar", ".tmp", ".bak")
# Built from parts so that this file does not match its own scan.
PERSONAL_MARKERS = tuple("/" + part for part in ("Users/", "home/")) + ("C:\\Users\\",)
TEXT_SUFFIXES = (".md", ".py", ".yaml", ".yml", ".txt", ".json", ".toml", ".cfg")


def published_files():
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:index]
    return []


def frontmatter_value(block, key):
    """Return a scalar or folded frontmatter value, joined for multi-line blocks."""
    for index, line in enumerate(block):
        if not line.startswith(key + ":"):
            continue
        value = line.split(":", 1)[1].strip()
        if value and value not in (">", ">-", "|", "|-"):
            return value
        parts = []
        for follow in block[index + 1:]:
            if follow.strip() and not follow.startswith((" ", "\t")):
                break
            parts.append(follow.strip())
        return " ".join(part for part in parts if part).strip()
    return None


class DistributionTests(unittest.TestCase):
    def test_required_resources_are_present(self):
        for relative in ("SKILL.md", "README.md", "README.en.md", "LICENSE",
                         "agents/openai.yaml"):
            self.assertTrue((ROOT / relative).is_file(), relative)
        for name in REFERENCES:
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_root_layout_is_the_skill_folder(self):
        entries = {path.name for path in ROOT.iterdir() if path.name != ".git"}
        self.assertEqual(entries, EXPECTED_ROOT)

    def test_reference_corpus_is_linked_from_the_skill(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in REFERENCES:
            self.assertIn(f"references/{name}", skill, name)

    def test_relative_links_resolve_inside_the_repository(self):
        checked = 0
        for path in published_files():
            if path.suffix.lower() != ".md":
                continue
            for target in LINK.findall(path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                checked += 1
                resolved = (path.parent / target.split("#")[0]).resolve()
                self.assertTrue(resolved.exists(), f"{path}: missing {target}")
                self.assertTrue(resolved.is_relative_to(ROOT), f"{path}: escapes repository: {target}")
        self.assertGreater(checked, 0, "no relative links were checked")

    def test_skill_metadata_is_readable(self):
        block = frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue(block, "SKILL.md frontmatter is missing")
        self.assertEqual(frontmatter_value(block, "name"), SKILL_NAME)
        self.assertTrue(frontmatter_value(block, "description"))
        agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("display_name:", agent)
        self.assertIn("default_prompt:", agent)
        self.assertIn(SKILL_NAME, agent)

    def test_no_personal_or_cached_files_ship(self):
        for path in published_files():
            self.assertNotIn(path.name, BANNED_NAMES, str(path))
            self.assertNotIn(path.suffix.lower(), BANNED_SUFFIXES, str(path))
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in PERSONAL_MARKERS:
                self.assertNotIn(marker, text, f"{path} contains a personal path")

    def test_license_is_present_and_complete(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("Permission is hereby granted", license_text)


if __name__ == "__main__":
    unittest.main()
