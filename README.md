# My course project

This repository holds your project for **00560413 AI Fluency and Agentic Methods for
Engineers** (Technion). You will build it over the semester, one milestone at a time. It
starts with your project proposal from Week 1; later weeks add your ground, your agent
and their tests.

Course website: <https://technionaifluency.github.io/www/>
(the [project page](https://technionaifluency.github.io/www/project/) describes the
milestones; the [exercises page](https://technionaifluency.github.io/www/exercises/)
has each week's slides).

## Two branches

| Branch | What it is for |
| --- | --- |
| `develop` | Where you work. Every change starts here. |
| `main` | What is finished. A change reaches `main` when you merge `develop` into it. |

Both start with an example in `about-me.md`: the lecturer's details. In Week 2 you put your
own details in on `develop`, and your merge into `main` stops on that file: Git cannot
choose between two versions of the same lines, so you choose.

## What lives where

| Path | What it is |
| --- | --- |
| `about-me.md` | Your name and faculty. |
| `project-proposal.md` | Your project proposal. It starts as the blank Week 1 template; replace it with your own. Keep the four section headings and the file name. |
| `docs/disclosure.md` | Your AI-usage log: one line at the end of every exercise session. |
| `tests/test_proposal.py` | Checks on the proposal and on `about-me.md` (see "The checks" below). Your own tests go in `tests/` too. |
| `.github/workflows/ci.yml` | Tells GitHub to run the checks on every change to `main`. |
| `pyproject.toml`, `uv.lock` | The Python project and its exact package versions, for `uv`. Commit both. |
| `.gitignore` | Files Git must never record, `.env` (your secrets) first. |

## How to start (Week 2)

The Week 2 exercise session walks through every step in VS Code.

1. **Fork this repository** to your own account. On the fork page, untick **Copy the
   `main` branch only**: you need `develop` too. Name your fork `my-project` for submission.
2. **Clone your fork** in VS Code, inside your Linux home folder (on Windows: in WSL,
   never under `/mnt/c`).
3. **Switch to `develop`.** Put your own name and faculty in `about-me.md`, copy in your
   Week 1 proposal as `project-proposal.md` in the repository root, and add your W02
   line at the end of `docs/disclosure.md`. Commit, and push `develop`.
4. **Merge `develop` into `main`.** Keep your own lines in `about-me.md`, commit the
   merge, and push `main`.

## The checks

| Check | When it runs | What it asks |
| --- | --- | --- |
| **Proposal structure** | every change on `main` | The proposal exists at `project-proposal.md` and keeps its four section headings, and neither it nor `about-me.md` has merge-conflict markers left (`<<<<<<<`, `>>>>>>>`, or a line of exactly seven `=`, `=======`). |
| **Proposal complete** | every change on `main` of your fork | No section of the proposal still has a `<!-- ... -->` placeholder. |

GitHub switches the checks off on a new fork: open your fork's **Actions** tab once and
enable its workflows.

A red check is information, not a punishment. Click **Details** next to it, scroll to
the summary at the end of the log, and read the `FAILED` line: it names the file and the
line to fix. On your laptop, `uv run pytest` runs both checks before you push.
