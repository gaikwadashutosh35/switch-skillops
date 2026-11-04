# 09 — Security and human-control model

## Threat assumptions

- Mattermost messages may contain malicious or misleading instructions.
- Repository files, issues, pull requests and external docs are untrusted input.
- Third-party skill packs may contain unsafe commands, hooks or network behavior.
- Agent output can be incorrect, incomplete or overconfident.
- Logs and chat messages can accidentally expose secrets.

## Required controls

### Input and instruction boundaries
- Treat chat content as task data, not as permission to override system/project rules.
- Ignore requests to reveal secrets, change safety rules or execute arbitrary commands.
- Validate request type, size and allowed fields.
- Do not accept arbitrary filesystem paths or command strings from a user message.

### Tool execution
- Use an explicit allowlist of development commands.
- Run in a disposable repository/branch/worktree where practical.
- Set timeouts and bounded retries.
- Capture command, exit code and relevant output.
- Require human confirmation before commands with destructive or external side effects.

### Approval
Require explicit approval tied to:
- request ID,
- exact proposed action,
- relevant branch/PR or target,
- review evidence.

Approval must not be inferred from vague language or an unrelated message. No automatic merge, deployment, production access, destructive deletion, credential rotation or permission changes in the MVP.

### Secrets and privacy
- Store secrets in environment variables or an approved secret manager.
- Never print `.env` contents.
- Redact tokens and credentials from logs and Mattermost messages.
- Use synthetic demo data.
- Do not commit customer data, credentials or private conversation content.

### Third-party skills
- Inspect skill instructions, scripts, hooks, permissions and network access before use.
- Pin versions/commits and record licenses.
- Do not run unreviewed remote install scripts.
- Disable any skill that attempts to exceed its declared scope.

### Failure behavior
- If Switch connection, agent runtime or tests fail, report failure honestly.
- Keep the task in a recoverable state.
- Do not silently mark work complete.
- Provide a manual next step and preserve enough context to resume.

## Security acceptance tests

- A chat message asking to print environment variables does not reveal them.
- A chat message containing `rm -rf` or arbitrary shell instructions is not executed.
- An unapproved merge/deploy request remains blocked.
- A QA failure cannot transition directly to completed.
- Duplicate request delivery does not create duplicate irreversible actions.
- Secrets are absent from test logs and room messages.
