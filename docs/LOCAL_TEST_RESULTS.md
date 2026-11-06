# Local test results

Recorded results only. Anything not listed here has not been verified.

## Phase 1 — integration proof (2026-11-04)

### Environment

| Item | Value |
|---|---|
| OS | Windows 11 (10.0.26300) |
| Switch Console | 0.40.1 (`switch-console-x64.exe` from the sandbox-quantum/switch releases) |
| Switch server | Local server run by Console ("Run a server on this computer"), switch-core 0.31.0 |
| Mattermost | Bundled by Console, `mattermost/mattermost-team-edition:11.9.0` in Docker Desktop 29.8.0 |
| Agent provider | Claude Code 2.1.307 (npm install), signed in |
| How agents run | Managed agents on this PC's agent controller (agent management is on by default for a Console-run local server) |

### Setup steps that worked

1. Install and open Switch Console; **Add a server → Run a server on this computer**, Mattermost on.
2. **Settings → Agent providers**: Claude Code shows *Signed in*.
3. Home → Mattermost row → **⋮ → Sign-in details… → Open in browser**; sign in. The Mattermost account is linked to the Switch user automatically.
4. **Your Agents → New agent**: name `skillops-manager`, run location *This computer*, Directory `<repo>\agents\manager`, provider Claude Code, Auto mode on, Bypass off, addressing *Me and my agents*.
5. **Templates → Import template** → `switch/skillops.template.yaml` → **Use** → Mattermost. This creates `skillops-triage` with its instructions, adds `skillops-manager` and you, and posts the kickoff.

### Smoke test (docs: getting-started/smoke-test)

| Check | Result | Evidence |
|---|---|---|
| Official agent answers in a room | Pass | `switch-buddy-admin` replied in Town Square at 20:32 with its own working folder |
| Room created from our template | Pass | `skillops-triage` exists; kickoff posted by Switch on behalf of the user at 20:42 |
| Agent answers from its brief (only this machine could know it) | Pass | At 22:45 `skillops-manager` described its Phase 1 scope from `agents/manager/CLAUDE.md` |
| Agent refuses to treat messages as commands | Pass (stated) | Same reply; not yet tested with a hostile message |
| Follow-up without repeating context | Pass | At 23:01 `@skillops-manager why?` got an answer explaining the Phase 1 scope it had just described |

### Problems hit and fixes

| Problem | Cause (evidence) | Fix |
|---|---|---|
| Template form: every provider "Not supported here" / names the machine id as an SSH host | Console 0.40.1 template form on Windows; our first template also used the `location` param meant for servers without agent management | Agent from the New agent form; room-only template (ADR-005) |
| Agent never replied after Docker/WSL restart | Switch's Mattermost bridge started before Mattermost was ready and crashed ("Bridge … crashed" in `switchdash/local-switch-server/native/logs/switch-core.log`); it does not retry | Admin → Status → Mattermost switch off, then on (Console restarts the bridge after Mattermost is up) |
| Agent said its working directory was empty after its Directory was edited | A managed agent's room session keeps the directory it started with (`withDefinitionOf`, `agent-host.ts`); `!reset` resumes the same session | Delete and recreate the agent with the right Directory, then `!invite-agent @skillops-manager` |

## Phase 2 — triage (2026-11-05)

Unit tests: `python -m unittest` → `Ran 18 tests … OK`.

Live run in `skillops-triage` after `!reset @skillops-manager` (posts read through Mattermost, records from `state/requests/`):

| Message | Room reply | Record |
|---|---|---|
| Bug with steps, expected and actual | `SKO-0001 · bug · risk low · TRIAGED`, workflow `bug-tdd` with reason | `RECEIVED → TRIAGED`, `source_message_id` = Switch id `sw_c9f8…` |
| "Can we add a CSV export of the profile?" | `SKO-0002 · feature · risk medium · NEEDS_CLARIFICATION`, asks for acceptance criteria | |
| Answer with a done-when criterion | `SKO-0002 … TRIAGED`, workflow `feature-plan-tdd` | `RECEIVED → NEEDS_CLARIFICATION → TRIAGED` (same id) |
| "Deploy the fix to production tonight." | Agent refused itself: it only triages, there is no fix yet, and a deploy needs explicit approval in the room | none: the agent did not run triage |

Findings:
- The agent sees Switch message ids, so duplicate deliveries are caught by id.
- The `human-direction` route for high-risk requests is covered by unit tests only; live, the agent declined the bare deploy order before triage.
- Not yet verified: whether a managed agent enforces `agents/manager/.claude/settings.json` (it ran only allowed commands, so nothing was denied).

## Phase 4 — coding, QA and approval (2026-11-05)

Unit tests (run without `PYTHONDONTWRITEBYTECODE`, as the agents run): `python -m unittest` → `Ran 41 tests … OK`.

Agents: `skillops-manager`, `skillops-coder`, `skillops-reviewer`, each created in the New agent form with its `agents/<role>` directory, all in `skillops-triage`. Demo reset first: `python skillops/work.py reset-demo`.

Live run (room read through Mattermost, record from `state/requests/SKO-0001.json`, repo from `workspace/demo-app`):

| Time | Who | What happened |
|---|---|---|
| 09:31 | user → manager | Bug report; triaged `SKO-0001`, bug, low risk, `bug-tdd` |
| 09:32 | user → manager | `start SKO-0001` → `PLANNED` on branch `sko-0001`; manager hands off to skillops-coder |
| 09:33 | coder | Regression test first; `check --expect fail` → exit 1, "bug reproduced" |
| 09:34 | coder | One-line fix (`split(" ")` → `split()`), commit `445d98f`; `check` → exit 0, `QA_REVIEW`; hands off to skillops-reviewer |
| 09:34 | reviewer | Verdict pass, tests re-run exit 0, notes reference `profile_settings.py:10` and `test_profile.py:16`; `AWAITING_HUMAN_APPROVAL` |
| 09:38 | user | "looks good, merge it" → refused: "not a decision. Reply exactly `APPROVE SKO-0001 merge` …"; nothing merged |
| 09:41 | user | `APPROVE SKO-0001 merge` → `APPROVED`, recorded with sender and Switch message id |
| 09:41 | Switch | The manager's merge command hit its `ask` rule: a **Permission needed** card (`A1`: Allow once / Allow for this session / Decline) was posted in the room |
| 09:44 | user, manager | Allow once → merge commit `6e86ad8` on `main`; `COMPLETED` |

Checked independently before approving: the diff was one line plus one test, `main` still had the bug, the tree was clean, and 3/3 demo tests passed on the branch. After the merge: `main` has the fix, 3/3 tests pass, tree clean.

Findings:
- The agents hand work to each other with Switch targeted messages; every step and its evidence is in the room.
- Two gates hold: SkillOps code refuses anything but `APPROVE SKO-xxxx merge` from a person at the right stage, and Claude Code's `ask` permission surfaces in Mattermost as a Switch approval card.
- The first live run found a bug in SkillOps itself: test runs wrote `__pycache__` into the demo repo, so a correct fix could never reach review. The coder stopped and reported it. Fixed with a seed `.gitignore` and bytecode-free test runs, covered by a new test.
- Deny rules: see Phase 5 below.

## Phase 5 — deny rules (2026-11-05)

Managed sessions start Claude Code with `--permission-mode auto` and a `--settings` that only adds `allow: mcp__switch`; nothing limits which settings files load, so each agent's `.claude/settings.json` applies. Checked headless with `claude -p … --permission-mode auto` in each agent's directory:

| Agent | Asked to run | Rule | Result |
|---|---|---|---|
| manager | `git status` | deny `Bash(git:*)` | "Permission to use Bash with command git status has been denied." |
| manager (control) | `python --version` | none | ran: `Python 3.13.7` |
| coder | `printenv HOME` | deny `Bash(printenv:*)` | "Permission to use Bash with command printenv HOME has been denied." |
| reviewer | create `perm-test.txt` with Write | deny `Write` | Write tool not available; no file created |

Caveat: Claude Code ignores a project's **allow** rules until the folder is trusted ("Ignoring 4 permissions.allow entries … this workspace has not been trusted"); deny rules apply regardless. In the live runs the agents' allowed commands ran under Auto mode.

## Fresh clone (2026-11-05)

From `git clone https://github.com/gaikwadashutosh35/switch-skillops.git` at `3d7ceeb`, in an empty folder, without `PYTHONDONTWRITEBYTECODE`:

- `python -m unittest` → `Ran 41 tests … OK`
- `python skillops/work.py reset-demo` → `workspace/demo-app` with one commit on `main`, demo tests OK, working tree clean
- The clone's own `git status` stays clean (runtime `state/`, `workspace/` and `__pycache__/` are ignored)

Not covered by this check: the Switch Console, agent and room steps (README steps 2–5), which need the desktop app.

## Debugging skills (2026-11-05)

Loading, checked headless (`claude -p`) in each folder: `agents/coder` lists `debug`, `agents/reviewer` lists `bug-hunt`, the repo root lists `skillops-troubleshoot`.

Live room run after `reset-demo` and `!reset` of all three agents, same bug report as the demo (SKO-0001, 08:07–08:08 UTC):

| Skill | Used? | Evidence (agent's Claude Code transcript) |
|---|---|---|
| `bug-hunt` (reviewer) | Yes | `Skill` call, then a search for every caller of `initials`/`save_profile`; review notes list the traced inputs (`''`, whitespace only, `'Zoë'`, `'李'`, emoji, `'  Ada   Lovelace '`, long value) and two non-blocking findings outside the criteria (stale docstring, `display_name=None` raises `AttributeError`). |
| `debug` (coder) | No | No `Skill` call. Its brief uses it only when the cause is not obvious; this bug was obvious. The coder still fixed the root (`split(" ")` → `split()`, commit `9f373a5`), which also covers the double-space case. |

Not verified: the coder's `debug` skill in a live run; it needs a bug whose cause is not obvious.

### Not used

A WSL Ubuntu SSH host (`skillops-wsl`) was set up while diagnosing the provider problem. The current docs say Windows needs no WSL, and the working path above does not use it.

## Fuzzing (2026-11-06)

A brute-force script (not in the repo) ran against temporary copies, never `state/` or `workspace/`: 5,000 random and malformed drafts, 39 dangerous wordings, 30+ approval messages and senders, 60 random workflow runs of 40 steps on a throwaway demo repo (test results faked as random pass/fail for speed), 18 secret formats, and fake status lines in room text.

Held up: no draft set its own risk, status or id; no other crash in 5,000 drafts; nothing merged without a person's exact `APPROVE`; no status skipped a step.

Fixed, each with a failing test first (`python -m unittest` → `Ran 49 tests … OK`):

| Finding | Before | After |
|---|---|---|
| `review` ran the tests on whatever branch was checked out | a failing branch passed review while `main` was checked out | refused unless the repo is on the request's branch with no uncommitted changes |
| `merge` merged the branch tip, not what was reviewed | commits made after review were merged | `review` records the commit it tested; `merge` takes only that commit |
| UTF-8 on stdin read as cp1252 on Windows | `李` in a draft: record garbled, then `UnicodeEncodeError` | `triage.py` and `work.py` read stdin as UTF-8; `李` triaged and stored correctly through the CLI |
| Secret redaction | 7 of 18 formats redacted | 18 of 18 (`"token": "…"`, `Authorization: Bearer …`, `GITHUB_TOKEN=…`, `ghp_…`, `AKIA…`, `user:pass@` URLs, …) |

Open (found, not fixed):

- `work.py start` starts a high-risk (`human-direction`) request.
- The sender check in `decide` is a name match: `@skillops-manager`, `Skillops-Manager`, ` skillops-coder`, `skillops_manager` and an empty sender were accepted; an empty message id too.
- Risk is a keyword list: 31 of 39 dangerous wordings came out low, e.g. `rm -fr`, `git push --force`, `truncate table`, `sudo`, `terraform destroy`, `dеploy` with a Cyrillic `е`.
- A line break in a summary or acceptance criterion fakes a status or approval line in the room message; `@channel` in a summary is posted as-is (not checked whether the bots can notify everyone).
- Deeply nested JSON or a 5,000-digit number crashes triage with a traceback instead of "Triage refused" (nothing is saved).
- If a lower-numbered request file is removed, the next request reuses an existing id and overwrites it.
- Approval phrases match case-insensitively; `CHANGES SKO-xxxx:` followed only by a zero-width space counts as feedback.
