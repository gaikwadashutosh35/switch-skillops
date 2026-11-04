# 08 — Submission checklist

## Official deliverables

- [ ] Public project repository.
- [ ] Short demo video showing the workflow running.
- [ ] README explains which agents are connected.
- [ ] README explains how the Mattermost channel/room is configured.
- [ ] README explains how to run the project.
- [ ] Submit before the official deadline: November 7, 2026, 11:59 PM IST (re-check live page).

## Product and Switch proof

- [ ] Mattermost is used as the actual team chat.
- [ ] Switch is installed/configured through the documented supported route.
- [ ] At least one AI agent joins the room through Switch.
- [ ] Human request and agent response are visible in the same room.
- [ ] SkillOps workflow uses shared room context for triage, handoff and approval.
- [ ] README explains what Switch does and why it is essential.
- [ ] No direct Mattermost webhook is substituted for the central Switch integration.

## Reproducibility

- [ ] Fresh clone tested.
- [ ] Prerequisites and versions documented.
- [ ] `.env.example` contains placeholders only.
- [ ] No secrets committed.
- [ ] Setup instructions are exact and current.
- [ ] Sample task and reset instructions included.
- [ ] Tests and exact outcomes documented.
- [ ] Known limitations and manual steps documented.
- [ ] License and third-party notices included.

## Technical quality

- [ ] Routing unit tests.
- [ ] Workflow state transition tests.
- [ ] Failure/timeout behavior.
- [ ] Duplicate message behavior or documented limitation.
- [ ] Human approval gate tested.
- [ ] No arbitrary shell execution from chat input.
- [ ] No auto-merge or deployment.
- [ ] Logs redact secrets.

## Presentation

- [ ] Demo follows one real bug/feature end-to-end.
- [ ] Show Mattermost + Switch-connected agent.
- [ ] Show workflow routing and why it was selected.
- [ ] Show actual test output and QA evidence.
- [ ] Show explicit human approval.
- [ ] Keep video concise and legible.
- [ ] Verify public repository access from a logged-out/incognito browser if possible.

## Optional side tracks

- [ ] Blog post explaining setup, workflow, what worked and what did not (Best Blog).
- [ ] If pursuing Best Core Contribution: choose an issue labelled `hackathon`, comment with proposed approach, wait for assignment, read CONTRIBUTING.md and sign required CLA, work only on assigned issue, open PR within hackathon window and reference `Closes #number`.
- [ ] Share a genuine project post with `#HowISwitch` if desired.

## Final pre-submit audit

Ask a person unfamiliar with the project to follow the README from a clean environment. If they cannot reproduce the core flow, fix the docs or reduce setup complexity before adding features.
