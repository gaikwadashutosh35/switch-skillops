# 06 — Selective Claude Code skill stack

This is based on the skill-stack research supplied for this project. Treat the repository descriptions as a shortlist to inspect, not as a guarantee that every skill is current, safe or compatible.

## Principle

Do not install all skill packs. Select one workflow at a time. A skill is reusable instructions; an agent is a runtime/role; a tool or MCP server provides capabilities. These are not interchangeable.

## Recommended stack

| Priority | Source | Use in SkillOps | Guidance |
|---|---|---|---|
| Core | Superpowers — https://github.com/obra/superpowers | Brainstorming, planning, TDD, debugging, code review, subagent workflow | Adopt selectively; verify current install method and Claude Code compatibility. |
| Core principles | Karpathy skills — https://github.com/multica-ai/andrej-karpathy-skills | Think before coding, simplicity, minimal changes, goal-driven execution | Prefer translating principles into project rules after review. |
| Selective engineering | Everything Claude Code — https://github.com/affaan-m/ecc | Architecture, coding, testing, security, docs | Do not install the entire pack by default. Select only what the actual stack needs. |
| UI only | Hallmark — https://github.com/nutlope/hallmark | UI/UX, visual design, landing/dashboard polish | Add only if a meaningful UI is part of the finished workflow. |
| Motion only | Emil Kowalski skills — https://github.com/emilkowalski/skills | Animation and interaction polish | Optional; low priority for this hackathon's core proof. |
| Requirements only | Matt Pocock skills — https://github.com/mattpocock/skills | Requirements clarification, engineering, TDD, debugging, docs | Use selectively where it improves request clarification. |
| Optional alternative | Ponytail — https://github.com/dietrichgebert/ponytail | Clean code, YAGNI, cost/security auditing | Do not stack blindly with Karpathy; choose one source of overlapping principles. |
| Discovery only | https://github.com/topics/agent-skills | Find additional skills | Not itself an installable skill pack. |
| Specialized | REA — https://github.com/morluto/rea | Reference/competitor reverse engineering | On-demand only; not necessary for MVP. |

## Task-to-workflow mapping

| Task type | Workflow |
|---|---|
| New feature | Clarify requirements -> acceptance criteria -> plan -> TDD -> implement -> review |
| Bug | Reproduce -> isolate -> regression test -> fix -> run tests -> review |
| UI | Inspect current design system -> user flow -> accessibility/responsive checks -> implement -> visual review |
| Security-sensitive | Stop and request human direction; threat model and safe review only; no production actions |
| Final review | Diff review -> tests -> security checks -> documentation -> human approval |

## Installation policy

Before installing any third-party skill repository:
1. Read its README and license.
2. Inspect every skill's `SKILL.md`.
3. Inspect scripts, hooks, shell commands, network access and file access.
4. Confirm compatibility with the current Claude Code version.
5. Pin a commit/tag and record it.
6. Install only the minimum skills needed.
7. Test activation with a harmless task.
8. Keep a way to remove/disable it.

Do not blindly execute remote install scripts or copy unknown hooks into a live project.

## Suggested project-local skills

If third-party packs are too heavy or incompatible, write small portable instructions in `skills/`:

- `requirements-triage/SKILL.md`
- `bug-investigation/SKILL.md`
- `feature-planning/SKILL.md`
- `tdd-implementation/SKILL.md`
- `qa-review/SKILL.md`
- `security-boundary-review/SKILL.md`

A project-local skill is still only an instruction file. It does not itself connect to Switch, run tools or create an agent.

## Runtime compatibility warning

Claude Code skills and plugins are runtime-specific. Do not assume that a Claude Code slash command, plugin, hook or skill installer automatically works in Codex, OpenCode or another runtime. Verify each runtime's documented skill mechanism separately.
