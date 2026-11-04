# Architecture decisions

Use this file to record decisions as they are made. Do not treat proposed decisions as implemented facts.

## ADR-001 — Mattermost is the primary chat surface

**Status:** Accepted for MVP  
**Decision:** Use the Mattermost instance supplied by the documented local Switch setup.  
**Reason:** It reduces workspace/admin setup and keeps the core human-agent workflow in a real team chat.  
**Trade-off:** The demo is local-first; additional platforms are out of MVP scope.

## ADR-002 — Switch is the collaboration backbone

**Status:** Accepted for MVP  
**Decision:** Use Switch-supported agent/room integration rather than a direct Mattermost webhook as the core path.  
**Reason:** Switch centrality is a major judging criterion and a mandatory part of the challenge.  
**Trade-off:** Must follow the current Switch docs/protocol rather than inventing a private adapter.

## ADR-003 — One manager workflow before multiple agents

**Status:** Accepted for MVP  
**Decision:** Start with one connected agent using distinct triage, coding and review phases. Split into separate agent processes only if the supported Switch integration makes it reliable and materially better.  
**Reason:** End-to-end reliability matters more than agent count.  
**Trade-off:** Role separation is initially logical rather than necessarily separate runtime instances.

## ADR-004 — Explicit human approval

**Status:** Accepted for MVP  
**Decision:** Require human approval before merge, deploy or other consequential side effects.  
**Reason:** Trust, safety and explainability.  
**Trade-off:** Some automation remains intentionally manual.

## ADR-005 — Agent from the New agent form, room from a template

**Status:** Accepted (verified 2026-11-04 on Windows 11, Switch Console 0.40.1, switch-core 0.31.0)  
**Decision:** Create `skillops-manager` in Switch Console's New agent form with its Directory set to `agents/manager` at creation. Create the `skillops-triage` room, its instructions and kickoff from the room-only template `switch/skillops.template.yaml`. The agent's brief lives in `agents/manager/CLAUDE.md`.  
**Reason:** On a local server Switch Console runs, agents are managed agents. Console 0.40.1's template form offered no usable provider for a new agent on Windows, while the New agent form did. A managed agent's existing room session keeps the directory it started with even after the agent is edited (`withDefinitionOf` in `console/packages/agent-providers/src/host/agent-host.ts`), so the directory must be right when the agent is created.  
**Trade-off:** Setup is two Console steps instead of one template run; the README must list the agent form's values exactly.
