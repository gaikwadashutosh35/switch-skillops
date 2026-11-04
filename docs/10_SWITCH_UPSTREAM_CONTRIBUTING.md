# 10 — Contributing to the official Switch repository

This guide is for the case where you decide to contribute code **to `sandbox-quantum/switch` itself**. SkillOps is a separate product repository; ordinary SkillOps work does not require a Switch upstream pull request or Switch CLA.

Source: https://github.com/sandbox-quantum/switch/blob/main/CONTRIBUTING.md

> Re-read the live upstream file before opening a PR. Commands, labels and legal terms can change.

## 1. Before you start

- Read the Switch Code of Conduct: https://github.com/sandbox-quantum/switch/blob/main/CODE_OF_CONDUCT.md
- For security vulnerabilities, follow the process in the upstream `SECURITY.md`; do not open a public issue with vulnerability details.
- Read the current upstream `CONTRIBUTING.md`.
- For a hackathon core contribution, follow the hackathon's separate process too: find an issue labelled `hackathon`, comment with your proposed approach, wait for assignment, and link the assigned issue in your PR as `Closes #<number>`.
- Do not assume that a SkillOps feature is an upstream Switch change. Keep product code in the SkillOps repository unless the change genuinely belongs in Switch.

## 2. Development prerequisites and setup

Upstream prerequisites listed in `CONTRIBUTING.md`:
- Docker
- `uv`
- `just` (the guide gives `brew install just` for Homebrew users)

The current upstream contributor setup is:

```bash
just init-env
uv sync
just gateway-install
just up
```

Then run the backend and gateway in separate terminals:

```bash
just run
```

```bash
just gateway-dev
```

`just up` starts supporting Docker Compose services, including PostgreSQL and Mattermost. `switch-core` and the gateway are run locally for hot reload. The contributor guide says `just run` starts `switch-core` on port `8000`.

For simply trying Switch rather than developing Switch, upstream says the standalone stack is a shorter route:

```bash
just standalone-up
```

Stop it using:

```bash
just standalone-down
```

**Caution:** `just reset` and `just standalone-reset` wipe volumes. Do not run them unless you intentionally want to delete local development data. `just down` stops the dev stack without the documented volume wipe.

Run `just` with no arguments to see the current recipes. Treat the live `justfile` and contributor guide as authoritative.

## 3. Repository layout to understand before editing

The upstream guide describes this layout:

| Path | Purpose |
|---|---|
| `core/` | Self-contained Python backend project |
| `core/switch_core/` | Main Python service package |
| `core/tests/` | Backend test suite |
| `gateway/` | Operator dashboard frontend (Node/Vite) |
| `console/` | Switch Console desktop app |
| `deploy/` | Docker Compose and remote deployment assets |
| `docs/official/` | Generated published documentation; edit the docs source repository instead |
| `docs/old/` | Internal architecture/protocol/bridge references; some old architecture material is explicitly out of date |
| `switch-expert/` | Switch-specific agent instructions and knowledge |
| `justfile` | Repository task runner |

Do not infer that the SkillOps product should copy this layout. This table describes the upstream Switch repository.

## 4. Common commands and checks

The current contributor guide lists:

| Command | Purpose |
|---|---|
| `just init-env` | Generate `.env` with fresh random secrets |
| `just up` / `just down` | Start / stop local development support services |
| `just reset` | Stop and wipe dev volumes — destructive |
| `just standalone-up` / `just standalone-down` | Start / stop the standalone stack |
| `just standalone-reset` | Stop standalone stack and wipe volumes — destructive |
| `just run` | Run `switch-core` locally |
| `just migrate` | Apply database migrations |
| `just migration "message"` | Autogenerate an Alembic migration |
| `just format` | Format and autofix with Ruff |
| `just check` | Lint/format check in CI mode |
| `just typecheck` | Type-check with mypy |
| `just test` | Run backend tests |
| `just test -k test_name` | Run a selected test |
| `just gateway-dev` / `just gateway-build` | Run / build the gateway |

Before an upstream PR, run the required checks from the live guide:

```bash
just check
just typecheck
just test
```

The guide states that the backend suite lives in `core/tests/`, uses `pytest` and `pytest-asyncio`, and that store tests use a **real PostgreSQL instance — not mocks and not SQLite**. Make sure the supporting stack is running before running tests that require PostgreSQL.

Record the exact commands, exit codes and relevant outcomes in the PR description. Do not claim tests passed unless they actually passed.

## 5. Agent CLI and messaging platform contributions

These are separate contribution paths with dedicated technical guides:

- Adding support for a new agent CLI: https://github.com/sandbox-quantum/switch/blob/main/docs/official/ (find the current “Adding support for a new agent CLI” guide)
- Adding support for a new messaging platform: https://github.com/sandbox-quantum/switch/blob/main/docs/official/ (find the current “Adding support for a new messaging platform” guide)

The current `CONTRIBUTING.md` says an agent-CLI support PR should include a real-CLI test summary and a short video. A messaging-platform support PR should include the adapter's test summary and a short video. Read the linked technical guides and current docs before implementation.

SkillOps uses Mattermost and an already-supported agent for its MVP, so neither contribution path is automatically needed.

## 6. Contributor License Agreement (required for upstream contributions)

The current Switch contributor guide says every contributor must agree to a CLA before their contribution can be merged.

### Individual contributor

1. Open your pull request as usual.
2. Wait for the automated CLA assistant to comment with the CLA link and status check.
3. Reply to the PR with this exact sentence:

```text
I have read the CLA Document and I hereby sign the CLA
```

The guide says the signature is recorded automatically and applies to future contributions; it is a one-time step.

### Corporate contributor

If contributing on behalf of a company, the employer may sign the Corporate CLA instead:

1. Download the Corporate CLA linked from the upstream contributor guide.
2. Complete the corporation details, authorized employee GitHub usernames in Schedule A, and signature from someone authorized to bind the company.
3. Email the signed PDF to `legal@sandboxquantum.com`.
4. The project records the approved usernames. Send an updated signed copy if the authorized list changes.

Do not sign on behalf of an employer unless authorized to do so.

## 7. License

The current contributor guide states that contributions are licensed under the project's **Apache License 2.0 with the Commons Clause condition**. Read the actual upstream `LICENSE` before contributing and ensure you have the rights to submit the code.

This does not mean you should copy Switch code into SkillOps. Keep a clear boundary between your original project code, dependencies, and any upstream contribution.

## 8. Upstream PR checklist

- [ ] Confirm the change belongs in Switch, not only in SkillOps.
- [ ] For the hackathon core track, find a `hackathon`-labelled issue.
- [ ] Comment with a proposed approach and wait for assignment.
- [ ] Read the Code of Conduct and current contributor/security guidance.
- [ ] Set up the upstream repo using the current documented commands.
- [ ] Keep the PR scoped to the assigned issue.
- [ ] Add or update tests.
- [ ] Run `just check`, `just typecheck` and `just test`.
- [ ] For a new agent CLI, include the required real-CLI test summary and short video.
- [ ] For a new messaging platform, include adapter test summary and short video.
- [ ] Reference the assigned issue in the PR, for example `Closes #123`.
- [ ] Complete the individual or corporate CLA process.
- [ ] Confirm licensing and third-party notices.
- [ ] Document exact test outcomes and known limitations.

## 9. Decision for Switch SkillOps

**MVP recommendation:** do not modify Switch core. Build SkillOps in its own public repository and integrate through documented Switch capabilities. Consider an upstream PR only if you find a real Switch bug or a missing capability that is necessary for the project and you can follow the issue-assignment and CLA process.
