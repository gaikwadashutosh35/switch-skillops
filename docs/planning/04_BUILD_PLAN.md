# 04 — Build plan and milestones

Hackathon window: November 4–7, 2026. Protect time for integration, testing, README and demo recording.

## Milestone 0 — Verify the foundation

**Goal:** one human and one agent collaborate in a Mattermost room through Switch.

- Install/start official Switch Console.
- Verify bundled Mattermost.
- Connect Claude Code.
- Create `skillops-triage`.
- Send and receive a message in the same room.
- Record exact versions and setup notes.

**Exit gate:** no SkillOps code until this works or the blocker is documented.

## Milestone 1 — Triage

**Goal:** transform a free-form request into a useful work item.

- Define task schema.
- Classify bug vs feature.
- Extract acceptance criteria.
- Ask for missing details.
- Assign a risk level.
- Post a compact triage summary into the room.

**Tests:** classification, missing fields, malformed input, ambiguous request.

## Milestone 2 — Workflow/skill router

**Goal:** explain which workflow should run and why.

Initial deterministic mapping:
- bug -> reproduce/debug/TDD/regression-test workflow
- feature -> clarify/plan/TDD/implementation workflow
- UI -> design/accessibility/responsive workflow plus implementation
- review -> tests/security/code-review workflow

Do not let user text name an arbitrary local skill path or shell command.

**Tests:** route selection, fallback, high-risk task, unsupported task, prompt injection-like instruction.

## Milestone 3 — Real implementation

**Goal:** complete one small real task.

- Use a disposable/sample repository.
- Create branch/worktree.
- Implement only within task scope.
- Run allowlisted tests.
- Capture changed files and command results.
- Keep a clear diff.

**Exit gate:** reproducible test result, not a claimed success.

## Milestone 4 — QA and approval

**Goal:** make human oversight part of the workflow.

- Compare diff to acceptance criteria.
- Check test evidence.
- Report unresolved risks.
- Ask human to approve, request changes or reject.
- Bind approval to the request and proposed action.
- No merge/deploy/destructive action without explicit approval.

## Milestone 5 — Reliability

- Duplicate message/idempotency behavior.
- Timeouts and bounded retries.
- Agent error handling and clear recovery path.
- Cancellation behavior.
- Secret redaction.
- Room permissions.
- Deterministic demo reset.

## Milestone 6 — Submission polish

- Public repository with clean history.
- Accurate README.
- Fresh-clone setup test.
- Unit/integration tests and recorded outcomes.
- Architecture diagram.
- Short demo video.
- Optional blog post.
- Final submission before the official deadline.

## Time allocation recommendation

1. 20% Switch/Mattermost connection and vertical slice.
2. 20% triage and routing.
3. 25% actual coding + QA path.
4. 15% human approval, error handling and tests.
5. 20% README, clean setup, demo and submission.

Do not add a dashboard until the complete Mattermost flow works. A dashboard is not the core hackathon proof.
