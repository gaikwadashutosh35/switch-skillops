# 08 — Submission checklist

## Official deliverables

- [x] Public project repository. *(https://github.com/gaikwadashutosh35/switch-skillops)*
- [x] Short demo video showing the workflow running. *(1:25, https://youtu.be/NwBfaLTQvgw)*
- [x] README explains which agents are connected.
- [x] README explains how the Mattermost channel/room is configured.
- [x] README explains how to run the project.
- [x] Submitted before the official deadline: November 7, 2026, 11:59 PM IST. *(submitted on November 5)*

## Product and Switch proof

- [x] Mattermost is used as the actual team chat.
- [x] Switch is installed/configured through the documented supported route.
- [x] At least one AI agent joins the room through Switch.
- [x] Human request and agent response are visible in the same room.
- [x] SkillOps workflow uses shared room context for triage, handoff and approval.
- [x] README explains what Switch does and why it is essential.
- [x] No direct Mattermost webhook is substituted for the central Switch integration.

## Reproducibility

- [x] Fresh clone tested. *(public repo, November 7: all tests pass, reset-demo works, tree stays clean; the Console/agent/room steps were not repeated from scratch)*
- [x] Prerequisites and versions documented.
- [x] `.env.example` contains placeholders only.
- [x] No secrets committed. *(staged changes scanned before each commit)*
- [ ] Setup instructions are exact and current. *(verified on Windows only; not on macOS or Linux)*
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
- [x] Logs redact secrets. *(18 common formats, tested)*
- [x] Brute-force tested. *(fuzzing; fixed and open findings in LOCAL_TEST_RESULTS)*

## Presentation

- [x] Demo follows one real bug/feature end-to-end.
- [x] Show Mattermost + Switch-connected agent.
- [x] Show workflow routing and why it was selected.
- [x] Show actual test output and QA evidence.
- [x] Show explicit human approval.
- [x] Keep video concise and legible. *(1:25, 1080p, captioned)*
- [x] Verify public repository access from a logged-out browser. *(opens without signing in)*

## Optional side tracks

- [ ] Blog post explaining setup, workflow, what worked and what did not (Best Blog). *(drafted; publishing is the author's step)*
- [ ] Best Core Contribution. *(not pursued: every `hackathon` issue was already assigned with open pull requests; three bug reports filed upstream instead: switch#1510, #1511, #1512)*
- [ ] Share a genuine project post with `#HowISwitch`. *(drafted)*
