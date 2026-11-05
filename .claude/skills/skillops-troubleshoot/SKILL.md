---
name: skillops-troubleshoot
description: Find why Switch SkillOps is stuck or misbehaving - agents not answering in Mattermost, an agent in the wrong folder, `work.py` refusing a step, a command denied, or a request in an unexpected state. Use when debugging the SkillOps setup or a demo run, not the demo app's code. Not for the skillops-manager, skillops-coder or skillops-reviewer agents; they follow only their CLAUDE.md.
---

# Troubleshoot SkillOps

Start from what the person sees, find the evidence, then apply the fix. Every fix below was hit and confirmed while building SkillOps (Windows 11, Switch Console 0.40.1, switch-core 0.31.0).

## 1. Where the evidence is

| Question | Look here |
|---|---|
| What state is a request in, what evidence and decisions does it have? | `python skillops/triage.py show SKO-xxxx`; raw record `state/requests/SKO-xxxx.json` |
| Why did a step refuse? | The `Refused: …` line printed by `work.py` (stderr) |
| Is the Switch server or the Mattermost bridge healthy? | Switch Console → **Admin → Status**, and its server log |
| What did an agent actually run, or get denied? | The agent's Claude Code transcript under `~/.claude/projects/<its folder, encoded>/` |
| What is in the demo repo? | `git -C workspace/demo-app status`, `log --oneline --all`, `branch` |

## 2. Symptom → cause → fix

**No agent answers in the room.**
1. Did the message start with `@agent-name`? A message that addresses nobody is ignored.
2. Check the thread under your message: replies and permission cards often land there.
3. Server log shows `Bridge … crashed` and no later `Started collaboration bridge`: Mattermost came up after the server (Docker restart, Admin → Restart). Fix: **Admin → Status**, turn Mattermost off and on. ([switch#1510](https://github.com/sandbox-quantum/switch/issues/1510))

**An agent says its brief or CLAUDE.md is missing, or its folder is empty.** Its room session started in the wrong directory, and editing the agent's Directory does not move it. Fix: delete the agent, create it again with the right Directory, then `!invite-agent @name` in the room. ([switch#1512](https://github.com/sandbox-quantum/switch/issues/1512))

**The template form offers no provider (Windows).** Turn on *Run managed agents on this computer* (Your Agents → +), create agents in the New agent form, and use the room-only template. ([switch#1511](https://github.com/sandbox-quantum/switch/issues/1511))

**`work.py check` does not move to QA_REVIEW.** Read its note:
- `tests fail` → the fix is incomplete; the output tail shows the failing test.
- `changes are not committed` → `git -C workspace/demo-app status`. Untracked `__pycache__/` means the demo repo is missing the seed `.gitignore`: run `python skillops/work.py reset-demo`.
- `branch has no committed changes` → the coder committed nothing on `sko-xxxx`.
- `the demo repo is not on sko-xxxx` → someone switched branches; check `git -C workspace/demo-app branch`.

**`decide` refuses an approval.** It needs the exact phrase (`APPROVE SKO-xxxx merge`, `CHANGES SKO-xxxx: …`, `REJECT SKO-xxxx`), from a person, for the right id, while the request is `AWAITING_HUMAN_APPROVAL`. The `Refused:` line says which of these failed.

**`merge` refuses.** The request is not `APPROVED`; `triage.py show` tells you where it is.

**An agent's command was denied, or ran when it should not have.** Check that agent's `agents/<name>/.claude/settings.json`. Deny rules always apply; allow rules are ignored until Claude Code trusts the folder, so Auto mode decides on unlisted commands.

**The merge never happens after APPROVE.** The merge waits on a Switch permission card in the room (often in a thread). Click *Allow once*.

**An agent keeps old context after a reset.** Run `python skillops/work.py reset-demo`, then `!reset @skillops-manager`, `!reset @skillops-coder`, `!reset @skillops-reviewer`.

## 3. Report

Say the symptom, the evidence you found (file, log line, `Refused:` text), the cause, and the fix you applied or recommend. If the evidence does not match any case above, say so; do not guess.
