# 08 — Submission checklist

## Official deliverables

- [x] Public project repository. *(https://github.com/gaikwadashutosh35/switch-skillops)*
- [ ] Short demo video showing the workflow running.
- [x] README explains which agents are connected.
- [x] README explains how the Mattermost channel/room is configured.
- [x] README explains how to run the project.
- [ ] Submit before the official deadline: November 7, 2026, 11:59 PM IST (re-check live page).

## Product and Switch proof

- [x] Mattermost is used as the actual team chat.
- [x] Switch is installed/configured through the documented supported route.
- [x] At least one AI agent joins the room through Switch.
- [x] Human request and agent response are visible in the same room.
- [x] SkillOps workflow uses shared room context for triage, handoff and approval.
- [x] README explains what Switch does and why it is essential.
- [x] No direct Mattermost webhook is substituted for the central Switch integration.

## Reproducibility

- [ ] Fresh clone tested.
- [x] Prerequisites and versions documented.
- [x] `.env.example` contains placeholders only.
- [ ] No secrets committed. *(scanned before each commit; re-check before making the repo public)*
- [ ] Setup instructions are exact and current. *(verified on Windows only; not yet from a fresh clone)*
- [x] Sample task and reset instructions included.
- [x] Tests and exact outcomes documented.
- [x] Known limitations and manual steps documented.
- [x] License and third-party notices included. *(MIT; no vendored third-party code)*

## Technical quality

- [x] Routing unit tests.
- [x] Workflow state transition tests.
- [ ] Failure/timeout behavior. *(timeouts and refusals in code; refusals tested, timeouts not)*
- [x] Duplicate message behavior or documented limitation.
- [x] Human approval gate tested.
- [x] No arbitrary shell execution from chat input. *(deny rules verified headless per agent; see LOCAL_TEST_RESULTS)*
- [x] No auto-merge or deployment.
- [x] Logs redact secrets.

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
