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

### Not used

A WSL Ubuntu SSH host (`skillops-wsl`) was set up while diagnosing the provider problem. The current docs say Windows needs no WSL, and the working path above does not use it.
