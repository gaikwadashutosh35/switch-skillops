# Switch SkillOps

**A human-approved AI engineering workflow inside Mattermost, powered by Switch.**

Switch SkillOps turns a team-chat request into a traceable engineering workflow. A human posts a feature request or bug in a Mattermost room. A manager agent clarifies and scopes it, routes work to the right specialist workflow, a coding agent implements it, a QA/reviewer checks the result, and a human approves the final change.

> **Core principle:** Switch is the collaboration backbone, not a decorative chat integration. Room membership, shared conversation context, agent participation, handoffs and human decisions must happen through Switch.

## Why this project

AI coding agents are useful in terminals, but their work is isolated from the people who request, review and approve it. SkillOps makes the team chat the shared work surface and adds a selective skill-routing layer so the right engineering workflow is used for each task.

## Demo in one sentence

A teammate reports a bug in Mattermost; through Switch, the manager agent turns it into an actionable plan, the coding agent produces a tested fix, QA reports evidence, and the teammate explicitly approves the next step.

## Hackathon fit

- **Primary track:** Best Business Workflow.
- **Challenge:** At least one person and one AI agent complete a real task together in team chat, connected through Switch.
- **Messaging platform:** Mattermost (the local Switch setup can bundle it).
- **Agent runtime:** Claude Code for the initial implementation; keep the design open to other Switch-compatible agents.
- **Must-have proof:** show the human request, agent work, handoffs, review and human decision in the Mattermost room.

## Important scope boundary

This repository is the **SkillOps product**, not a fork or rewrite of Switch. Use the official Switch repository and supported setup as the integration layer. Do not recreate Mattermost, room history, agent transport or Switch's collaboration bridge.

## Quick start

1. Read [`docs/01_HACKATHON_REQUIREMENTS.md`](docs/01_HACKATHON_REQUIREMENTS.md).
2. Read [`docs/02_PRODUCT_SPEC.md`](docs/02_PRODUCT_SPEC.md).
3. Follow [`docs/03_SETUP_MATTERMOST_SWITCH.md`](docs/03_SETUP_MATTERMOST_SWITCH.md).
4. Give Claude Code the prompt in [`CLAUDE_CODE_PROMPT.md`](CLAUDE_CODE_PROMPT.md).
5. Work through [`docs/04_BUILD_PLAN.md`](docs/04_BUILD_PLAN.md).
6. Record the demo using [`docs/07_DEMO_SCRIPT.md`](docs/07_DEMO_SCRIPT.md).
7. Complete [`docs/08_SUBMISSION_CHECKLIST.md`](docs/08_SUBMISSION_CHECKLIST.md).

## Proposed workflow

```text
Human request in Mattermost
          |
          v
      Switch room
          |
          v
   Manager / triage agent
          |
   clarify + classify + plan
          |
          v
   Skill/workflow router
          |
          +------> Coding agent
          |             |
          |       branch + tests
          |             |
          +------> QA / reviewer
                        |
                 findings + evidence
                        |
                        v
              Human approval in room
                        |
             approved next action only
                        |
                        v
               Result + PR link in room
```

## Suggested repository layout

```text
switch-skillops/
├── README.md
├── CLAUDE_CODE_PROMPT.md
├── LICENSE
├── .env.example
├── .gitignore
├── .claude/
│   └── CLAUDE.md
├── docs/
│   ├── 01_HACKATHON_REQUIREMENTS.md
│   ├── 02_PRODUCT_SPEC.md
│   ├── 03_SETUP_MATTERMOST_SWITCH.md
│   ├── 04_BUILD_PLAN.md
│   ├── 05_ARCHITECTURE.md
│   ├── 06_SKILL_STACK.md
│   ├── 07_DEMO_SCRIPT.md
│   ├── 08_SUBMISSION_CHECKLIST.md
│   └── 09_SECURITY_AND_GUARDRAILS.md
├── app/                 # only if a dashboard is justified by the MVP
├── orchestrator/
├── integrations/
├── skills/
├── tests/
└── examples/
```

The exact code layout must be chosen after inspecting the current Switch docs, protocol and repository. Do not invent unsupported Switch APIs.

## Definition of done

A fresh developer can follow the README, start the supported local Switch + Mattermost setup, connect the documented agent, post a sample request, observe the workflow, approve/reject a gated action, and reproduce the test results.

## Official links

- Hackathon overview and submission requirements: https://www.wemakedevs.org/hackathons/switch
- Official rules: https://www.wemakedevs.org/hackathons/switch/rules
- Switch repository: https://github.com/sandbox-quantum/switch
- Switch documentation: https://docs.switchagents.ai/
- Switch docs MCP: https://docs.switchagents.ai/mcp
