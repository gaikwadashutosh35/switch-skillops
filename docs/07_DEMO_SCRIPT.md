# 07 — Demo script (3–4 minutes)

## Demo objective

Show one human and one AI agent completing a real engineering task together in a Mattermost room through Switch. Make Switch central and visible.

## Before recording

- Start Switch and Mattermost using the documented local setup.
- Confirm the agent is connected and in `skillops-triage`.
- Use a clean demo repository and a known reproducible bug.
- Ensure tests run locally.
- Clear unrelated messages and sensitive information.
- Prepare a fallback recording only as backup; the primary demo should show the real running workflow.
- Never show API keys, tokens or private data.

## Run of show

### 0:00–0:25 — Problem
Show Mattermost. Explain: bug reports are usually separated from coding agents, decisions and test evidence.

### 0:25–0:50 — Human request
Post:

> @SkillOps The profile settings form crashes when an optional display name is empty. Reproduce it, add a regression test, fix it, and show the test results. Do not merge anything without my approval.

Point out that the request originates in the Mattermost room.

### 0:50–1:25 — Triage and workflow selection
Show the manager response:
- task classified as bug,
- acceptance criteria,
- missing information (if any),
- selected debugging/TDD workflow,
- reason for selection.

### 1:25–2:20 — Implementation and QA
Show the agent working through Switch:
- branch/worktree created,
- regression test added,
- code changed,
- tests executed,
- QA report references actual files and command output.

Do not speed past a fake result. Show a real test command/output.

### 2:20–3:00 — Human decision
Show QA summary and explicit approval request. Choose “request changes” once if time allows, or approve the specific next step. Demonstrate that no merge/deploy happens automatically.

### 3:00–3:35 — Result and Switch value
Show final status, branch/PR link if available, and the room history. Explain that Switch connected the agent to the shared room and carried the work context between the human and agent.

## Narration points

- “Mattermost is the team workspace; Switch brings the agent into this room.”
- “The router selects a workflow based on the task, rather than loading every skill for every request.”
- “The coding phase reports evidence, and the QA phase checks it against acceptance criteria.”
- “The human remains in control of consequential actions.”

## Final slide / closing

Show:
- GitHub repository URL.
- Setup command/README.
- Supported agent and room configuration.
- Test status.
- Known limitations.

## Demo quality checklist

- [ ] No fabricated UI or fake agent response.
- [ ] Switch participation is visible.
- [ ] Human request and human approval are visible.
- [ ] A real task is completed.
- [ ] Test evidence is readable.
- [ ] No secrets or private data.
- [ ] Demo fits within a few minutes.
