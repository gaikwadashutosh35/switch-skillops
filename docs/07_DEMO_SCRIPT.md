# 07 — Demo script (about 4 minutes)

Every message below was sent in the verified run of 2026-11-05 (see `LOCAL_TEST_RESULTS.md`). Send each one as its own message in `skillops-triage`.

## Before recording

1. `python skillops/work.py reset-demo`: clears requests and recreates `workspace/demo-app`.
2. Switch Console shows the local server *Running*; Admin → Status shows Mattermost on. If the server or Docker restarted, turn the Mattermost switch off and on once.
3. In the room, reset the agents so each starts from its brief:
   ```
   !reset @skillops-manager
   !reset @skillops-coder
   !reset @skillops-reviewer
   ```
4. Close anything showing tokens, `.switch/` files or other private data.

## Run of show

### 0:00–0:20 — The problem
Show the Mattermost room and its member list (three bots and you). Bug reports, coding agents, test evidence and approvals usually live in different places; here they share one room through Switch.

### 0:20–0:50 — Request and triage
```
@skillops-manager The settings page crashes when I save a profile with an empty optional display name. Steps: open Settings, clear Display name, click Save. Expected: it saves. Actual: a 500 error. Don't merge anything without my approval.
```
Point out the reply: `SKO-0001 · bug · risk low · TRIAGED`, acceptance criteria, workflow `bug-tdd` and **why** it was chosen.

Optional, 20 seconds: show clarification with `@skillops-manager Can we add a CSV export of the profile?`. It asks for acceptance criteria instead of guessing.

### 0:50–1:50 — Handoffs and evidence
```
@skillops-manager start SKO-0001
```
Show, in order: the manager's `PLANNED` reply and its handoff to skillops-coder; the coder's failing regression test (`exit 1`, "bug reproduced"); the fix and passing tests (`exit 0`, changed files); the handoff to skillops-reviewer; the reviewer's verdict with file references and its own test run.

### 1:50–2:50 — The human decides
First show that a casual reply does not count:
```
@skillops-manager looks good, merge it
```
It is refused, and nothing is merged. Then:
```
@skillops-manager APPROVE SKO-0001 merge
```
Show the **Permission needed** card that Switch posts in the room for the merge. Click **Allow once**.

### 2:50–3:30 — Result
Show the final `COMPLETED` report with the merge commit. Optionally show `git -C workspace/demo-app log --oneline --graph` in a terminal: the fix commit and the merge "approved by user".

### 3:30–4:00 — Close
- Switch put three agents and a person in one room, carried the handoffs and showed the approval card.
- The code, not the agents, decides risk, state and when a merge is allowed.
- Repository link, `python -m unittest` (49 tests), known limitations in the README.

## Narration points

- "The manager, coder and reviewer are three separate Switch agents; you can see each one in the member list."
- "Risk and the workflow come from code, from my own words; the agent can't lower them."
- "A casual 'looks good' isn't an approval. Only `APPROVE SKO-0001 merge` from a person is, and the merge still stops at Switch's approval card."

## Demo quality checklist

- [ ] No fabricated UI or agent responses: record the real run.
- [ ] The three bots are visible as room members.
- [ ] Request, evidence (exit codes) and human decision are readable.
- [ ] The refused "looks good" and the approval card are both shown.
- [ ] No secrets or private data on screen.
