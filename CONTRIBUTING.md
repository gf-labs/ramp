# Contributing to ramp

Thanks for looking under the hood. This repo runs Git Flow with CI-enforced releases —
the rules below are checked by machines, so knowing them saves you a rejected PR.

## Branches and PRs

- `main` is stable releases only; `develop` is daily integration.
- Branch `feature/<name>` off `develop`; PRs into `develop` are **squash-merged**.
- `release/*` and `hotfix/*` branches merge into `main` via merge-commit PRs. Releases
  are tagged on the release-branch tip — if you're not cutting a release, you'll never
  touch `main` directly.

## The gates (what CI will hold you to)

- **test.yml** — ruff lint + the stdlib pytest suite on Python 3.8 (the floor) and
  current. Run locally: `python3 -m pip install -r requirements-dev.txt && python3 -m
  pytest tests/ -q && ruff check .`
- **release-gate.yml** — a PR into `main` must have a `## [<manifest version>]` section
  in `CHANGELOG.md`; a push to `main` must match the nearest reachable tag.
- **check-docs.py** — README tables, count badges, the CLAUDE.md structure listing, and
  relative links must match the tree. Run locally: `python3 scripts/check-docs.py`
- Actions are SHA-pinned; Dependabot maintains them. Don't hand-edit pins.

## Changes

- Every user-visible change adds a `## [Unreleased]` CHANGELOG entry (Keep-a-Changelog).
- Python is **stdlib-only** and must run on 3.8. Commands are pure Markdown — see
  [`docs/topic-authoring.md`](docs/topic-authoring.md) before touching a topic schema.
- Commit style: `type(scope): imperative summary` (≤ 50 chars).
- Pre-release checklist: re-verify README claims against the diff.

## Adding a topic

One file: `topics/<name>.md`, following the authoring contract
([`docs/topic-authoring.md`](docs/topic-authoring.md)) — the linter
(`python3 ramp_core.py lint <name>`) must pass with 0 problems. `/ramp:ingest` drafts a
starting schema from a source document.

Licensed MIT — contributions land under the same license.
