# 02 — Product specification

## Product name

**Switch SkillOps — a skill-aware AI engineering teammate in Mattermost.**

## Problem

A teammate reports a bug or asks for a feature, but the request is separated from the engineering agent that can act on it. Context is copied between chat, terminal, issue tracker and code review. The requester cannot see the reasoning, test evidence or approval state in one shared place.

## Promise

Turn a team-chat request into a transparent, human-approved engineering workflow without making teammates leave Mattermost.

## Target user

A small software team that receives bug reports and feature requests in chat and uses AI coding agents to accelerate implementation.

## MVP user journey

1. Human posts `@SkillOps` with a bug report or feature request in a Switch-connected Mattermost room.
2. Manager agent acknowledges it and creates a structured task:
   - short title and summary,
   - bug/feature classification,
   - missing information/questions,
   - acceptance criteria,
   - risk classification,
   - proposed workflow and reason.
3. If critical information is missing, agent asks a focused clarification question and waits.
4. Workflow router chooses one approved workflow:
   - bug investigation,
   - feature implementation,
   - UI change,
   - tests/review.
5. Coding agent works in a branch or isolated worktree, follows the selected workflow and reports changed files and test evidence.
6. QA/reviewer phase checks the diff against acceptance criteria and flags defects/security concerns.
7. Agent posts a concise review report in the same room.
8. Human explicitly approves, requests changes or rejects.
9. Only approved, non-destructive next steps occur. For MVP, stop at a local branch or a draft PR. Never auto-merge or deploy.
10. Agent posts final status, evidence and links.

## MVP scope — must build

- One working Mattermost room connected through Switch.
- One existing coding agent connected through documented Switch setup.
- One manager/triage workflow.
- Transparent skill/workflow router with deterministic tests.
- At least one actual coding task on a small sample repository or safe demo repo.
- QA/review step with evidence.
- Explicit human approval/revision step in the room.
- End-to-end demo and reproducible README.

## Stretch goals — only after MVP works

- GitHub issue/PR integration.
- Separate specialist agents if supported and valuable.
- Dashboard for workflow history/metrics.
- Additional messaging platforms.
- Persistent analytics and team-level skill performance.
- Best Blog post.

## Explicit non-goals

- Building a new chat application.
- Reimplementing Switch room history, agent transport or Mattermost bridge.
- Building a foundation model or generic autonomous coding platform.
- Installing every skill pack.
- Autonomous production deployments or auto-merge.
- Complex microservice architecture before proving the core workflow.

## Success metrics for the demo

These are project targets, not organizer requirements:
- A request can be submitted and acknowledged in one room.
- The agent produces acceptance criteria and a selected workflow.
- A real testable change is made in a branch.
- QA posts at least one verifiable test/review result.
- Human approval is required before the final gated action.
- A fresh developer can reproduce the flow from docs.

## Example demo request

> `@SkillOps The settings page crashes when a user saves a profile with an empty optional display name. Please reproduce it, add a regression test, fix it, and show me the test results. Do not merge anything without my approval.`

Use a deliberately small, safe demo repository where the bug can be reproduced reliably.
