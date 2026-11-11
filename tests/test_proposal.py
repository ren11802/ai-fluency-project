"""Checks on project-proposal.md (and on about-me.md for conflict markers).

Two kinds of check live here:

- Structure (always run): the file exists, it keeps the four section headings
  of the Week 1 template, and no merge-conflict markers are left in it (the
  <<<<<<< and >>>>>>> lines, and the ======= line between the two sides).
- Completeness (marked ``proposal_complete``): every section has been written,
  so no ``<!-- ... -->`` placeholder is left. On GitHub these run on your fork
  only; on your laptop ``uv run pytest`` runs them too, so you can see what is
  left before you push.

Run them with:  uv run pytest
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_NAME = "project-proposal.md"
PROPOSAL = ROOT / PROPOSAL_NAME
ABOUT_ME = ROOT / "about-me.md"

# The four sections of the Week 1 template. The patterns match the heading's
# words, so the level (##, ###), the number and the case may change.
SECTIONS = {
    "1. The problem and goal": r"problem and goal",
    "2. The simulator": r"the simulator",
    "3. The agent's role": r"agent(.{1,3}s)?\s+role",
    "Explain your project to someone outside your field": r"explain your project",
}

HEADING = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*$")
# The outer markers start a line and are followed by a space or nothing.
CONFLICT_MARKER = re.compile(r"^(<<<<<<<|>>>>>>>)( |$)")
# The divider between the two sides: a line that is exactly seven "=" (Git
# writes it that way). Longer or shorter runs of "=" are ordinary Markdown.
CONFLICT_DIVIDER = re.compile(r"^=======\s*$")


def read_proposal() -> list[str]:
    if not PROPOSAL.is_file():
        pytest.fail(
            f"{PROPOSAL_NAME} is missing. It must stay at exactly this path: "
            "put your Week 1 proposal there (keep the file name).",
            pytrace=False,
        )
    return PROPOSAL.read_text(encoding="utf-8").splitlines()


def section_spans(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Map each of the four sections to (heading line, end line), 0-based.

    A section runs from its heading to the next of the four headings, so any
    sub-headings you add inside a section stay part of it.
    """
    starts = {}
    for i, line in enumerate(lines):
        match = HEADING.match(line)
        if not match:
            continue
        for section, pattern in SECTIONS.items():
            if section not in starts and re.search(pattern, match["title"], re.IGNORECASE):
                starts[section] = i
                break
    ordered = sorted(starts.items(), key=lambda item: item[1])
    spans = {}
    for n, (section, start) in enumerate(ordered):
        end = ordered[n + 1][1] if n + 1 < len(ordered) else len(lines)
        spans[section] = (start, end)
    return spans


# --- Structure: always run --------------------------------------------------


def test_proposal_file_exists():
    read_proposal()


@pytest.mark.parametrize("section", list(SECTIONS))
def test_section_heading_is_kept(section):
    lines = read_proposal()
    if section not in section_spans(lines):
        pytest.fail(
            f'{PROPOSAL_NAME} has lost the heading "{section}". '
            "Keep the template's four headings and write under them.",
            pytrace=False,
        )


def test_no_merge_conflict_markers():
    lines = read_proposal()
    found = [
        f"line {i}: {line.strip()}"
        for i, line in enumerate(lines, start=1)
        if CONFLICT_MARKER.match(line)
    ]
    if found:
        pytest.fail(
            f"{PROPOSAL_NAME} still has merge-conflict markers "
            f"({'; '.join(found)}). Choose the text you want to keep, delete the "
            "<<<<<<<, ======= and >>>>>>> lines, then commit.",
            pytrace=False,
        )


def test_no_leftover_conflict_divider():
    lines = read_proposal()
    found = [f"line {i}" for i, line in enumerate(lines, start=1) if CONFLICT_DIVIDER.match(line)]
    if found:
        pytest.fail(
            f"{PROPOSAL_NAME} still has a merge-conflict divider, a line of exactly "
            f"seven = signs ({'; '.join(found)}). It is the line Git puts between "
            "your two versions: delete it, keep the sentence you want, then commit.",
            pytrace=False,
        )


def test_about_me_has_no_conflict_markers():
    if not ABOUT_ME.is_file():
        pytest.skip("about-me.md is not in this repository")
    lines = ABOUT_ME.read_text(encoding="utf-8").splitlines()
    found = [
        f"line {i}: {line.strip()}"
        for i, line in enumerate(lines, start=1)
        if CONFLICT_MARKER.match(line) or CONFLICT_DIVIDER.match(line)
    ]
    if found:
        pytest.fail(
            f"about-me.md still has merge-conflict markers ({'; '.join(found)}). Keep "
            "your own two lines, delete the <<<<<<<, ======= and >>>>>>> lines, then commit.",
            pytrace=False,
        )


# --- Completeness: on your fork in CI, and always on your laptop --------


@pytest.mark.proposal_complete
@pytest.mark.parametrize("section", list(SECTIONS))
def test_section_is_written(section):
    lines = read_proposal()
    spans = section_spans(lines)
    if section not in spans:
        pytest.skip(f'heading "{section}" is missing (reported by the structure check)')
    start, end = spans[section]
    placeholders = [
        f"line {i + 1}: {lines[i].strip()}"
        for i in range(start, end)
        if "<!--" in lines[i]
    ]
    if placeholders:
        pytest.fail(
            f'Section "{section}" in {PROPOSAL_NAME} still has a placeholder '
            f"({'; '.join(placeholders)}). Replace that line with your own answer, "
            "commit and push again.",
            pytrace=False,
        )
