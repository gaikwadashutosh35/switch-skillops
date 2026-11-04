# 01 — Hackathon requirements and scoring

This document separates **published organizer requirements** from our implementation strategy. Re-check official pages before final submission because organizers can update event details.

## Event and challenge

- Event: Flip the Switch Hackathon, powered by Switch AI; co-hosted by WeMakeDevs and DevTools Academy.
- Dates: **November 4–7, 2026**. Published close: **November 7, 2026, 11:59 PM IST**.
- Format: online.
- Team size: solo or up to four.
- Eligibility: official rules state entrants must be at least 18 (or age of majority if higher) and satisfy sanctions and other exclusions. Read the complete rules.
- Challenge: add at least one AI agent to a team chat using Switch and build a workflow where the agent and a person complete a real task together.
- Switch is mandatory and must be central; README must explain how it is used.
- Existing agents, libraries and templates may be used, but the Switch setup and workflow the agents run must be built during the hackathon.
- AI coding tools are permitted; participants must understand and be able to explain what they submit.

## Required submission items

The organizer's challenge page specifies:

1. A **public project repository**.
2. A **short demo video** showing the workflow running.
3. A **README** explaining:
   - which agents are connected,
   - how the channel/room is set up,
   - how to run the project.
4. Optional: a blog post (also enters the Best Blog side track).

Do not assume a submission portal field or upload format that is not stated on the current official page. Check the live submission instructions immediately before submitting.

## Judging rubric

| Criterion | Weight | What our submission should prove |
|---|---:|---|
| Use of Switch | 30% | Switch is essential: human and agent collaborate in Switch-managed rooms; removing Switch breaks the central workflow. |
| Technical execution | 25% | It runs; a judge can clone the public repo and reproduce the workflow. |
| Creativity and impact | 25% | It solves a recognizable team problem with a meaningful skill-aware workflow and human control. |
| Presentation and documentation | 20% | A short, clear demo and a README explain the agents, room setup and run steps. |

## Track choice

**Primary: Best Business Workflow.** SkillOps is designed for a software team handling bug reports and feature requests.

Other possibilities:
- Best Personal or Creative Workflow: not our focus.
- Best Core Contribution: separate track. Only pursue if contributing to Switch itself. The organizer requires choosing an issue labelled `hackathon`, commenting with an approach, waiting for assignment, reading `CONTRIBUTING.md`, and linking the assigned issue in the PR (`Closes #...`). Unassigned or low-effort/unreviewed AI PRs do not count.
- Best Blog: optional side track.

## Organizer timeline

- Kickoff livestream: November 2, 2026, 9:00 PM IST (published schedule).
- Hacking begins: November 4, 2026, 12:01 AM IST.
- Submissions close: November 7, 2026, 11:59 PM IST.

## Rules and compliance reminders

- Register using one accurate, verifiable identity; no automated or fraudulent entries.
- Respect eligibility and sanctions restrictions in the official rules.
- Entrant retains ownership but grants the sponsor a broad, non-exclusive license to use the submission for hackathon operation, judging, documentation and promotion.
- Ensure you have rights to all code/assets and comply with all third-party/open-source licenses.
- Do not include confidential information, private customer data, secrets or malicious code.
- Read the complete current rules; this summary is not legal advice.

## Our acceptance criteria mapped to judging

### Switch centrality
- Human request originates in a Mattermost room connected through Switch.
- Agent receives/responds through the Switch integration, not a separate demo-only webhook.
- Triage, handoff and approval context are visible in the shared room.
- README explains the exact Switch components and setup.

### Technical execution
- Clean setup instructions from a fresh clone.
- `.env.example`, pinned/declared dependencies, tests and reproducible sample task.
- Honest list of prerequisites, manual steps and known limitations.
- No secrets committed.

### Creativity and impact
- Skill/workflow routing chooses a fitting engineering process based on task type and risk.
- Human-in-the-loop approval is explicit and auditable.
- QA reports evidence, not just “looks good”.

### Presentation
- Short demo follows one real bug/feature from request to result.
- Show the Mattermost room and Switch agent participation clearly.
- README contains agents, room setup, run instructions and a short architecture diagram.

## Official sources

- Challenge, tracks, judging, deliverables and schedule: https://www.wemakedevs.org/hackathons/switch
- Official rules: https://www.wemakedevs.org/hackathons/switch/rules
- DevTools Academy event page: https://www.devtoolsacademy.com/hackathons/flip-the-switch
- Switch repository: https://github.com/sandbox-quantum/switch
- Switch docs: https://docs.switchagents.ai/

**Verified against published pages on November 4, 2026.** Re-check the live pages before submission.
