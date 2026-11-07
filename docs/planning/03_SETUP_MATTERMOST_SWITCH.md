# 03 — Mattermost + Switch setup

## Principle

Use the official Switch setup, not a custom Mattermost bot as a substitute. The official hackathon page says the local Switch setup includes Mattermost, so no company workspace is required.

## Prerequisites

- A supported desktop OS and Switch Console build.
- Docker installed and running.
- Claude Code installed and authenticated (or another agent supported by the current Switch docs).
- Git.
- An API subscription/key required by the chosen agent/model.
- Enough disk/RAM for Docker services.

Check the current Switch docs for OS support and current release instructions.

## Recommended route: Switch Console

1. Open the official Switch getting-started page: https://docs.switchagents.ai/switch-rooms/getting-started
2. Install the current Switch Console release for your OS from the official Switch/GitHub release links.
3. Start Switch using the Console's documented local setup.
4. Confirm Mattermost is available from the Console's local environment.
5. Create a team/workspace and a room/channel for the demo, for example `skillops-triage`.
6. Connect Claude Code through the Console's documented agent connection flow.
7. Add the agent to the intended room and verify it can read/respond there.
8. Send a simple test message and capture the successful round trip before building SkillOps.

Do not guess the Mattermost URL, login credentials, port, room config format or Console menu labels. Use the values displayed by your installed Console and current docs.

## Claude Code docs MCP

The published Switch docs expose an MCP endpoint. Add it to Claude Code:

```bash
claude mcp add switch-docs --transport http https://docs.switchagents.ai/mcp
```

Then restart/reload Claude Code if required and verify the MCP server is available. Ask Claude:

```text
Use the Switch docs MCP. Walk me through the current supported local setup with Mattermost and connecting this Claude Code agent to a room. Cite the exact docs pages and do not guess settings.
```

## Source-from-repository developer route (optional)

Use this only if you need to develop Switch itself or inspect its internals. The current upstream contributor guide describes a development flow using Docker, `uv`, and `just`; it says `just up` starts PostgreSQL and Mattermost, while Switch core and gateway are run separately for hot reload.

```bash
git clone https://github.com/sandbox-quantum/switch.git
cd switch
just init-env
uv sync
just gateway-install
just up
```

In separate terminals, following the current CONTRIBUTING guide:

```bash
just run
```

```bash
just gateway-dev
```

The upstream repository may change. Read its current `CONTRIBUTING.md`, `README.md`, `.env.example` and docs before running commands. The source-development path is not necessary for a SkillOps product that only integrates with Switch.

## Verify the connection

Before proceeding, confirm all of the following manually:
- [ ] Switch Console reports the local environment healthy.
- [ ] Mattermost opens and you can sign in.
- [ ] The intended room exists.
- [ ] The selected agent appears as a participant in the room.
- [ ] A human message reaches the agent.
- [ ] The agent's reply appears in the same room.
- [ ] The agent can use the room context in a follow-up message.

Record actual versions, URLs and commands in `docs/LOCAL_TEST_RESULTS.md`. Never commit credentials.

## Troubleshooting approach

- Check Switch Console health/status first.
- Inspect the documented Switch logs and Mattermost service logs.
- Confirm the agent is connected and joined to the correct room.
- Confirm permissions and room membership.
- Verify that the configured model/API credentials work outside the workflow.
- Avoid changing ports, compose files or environment variables until the current docs/logs point to the issue.

## Official references

- Getting started: https://docs.switchagents.ai/switch-rooms/getting-started
- Switch docs: https://docs.switchagents.ai/
- Switch docs MCP: https://docs.switchagents.ai/mcp
- Upstream repo: https://github.com/sandbox-quantum/switch
- Upstream contributor setup: https://github.com/sandbox-quantum/switch/blob/main/CONTRIBUTING.md
