# HR Manager Sub-skill: Guardrail Monitor

Run on every loop cycle alongside the health check. Detects and documents protocol violations.

## What to check

### 1. Inbox routing violations
Check `_inbox/` directories for messages between roles that should not have direct paths. Cross-reference against `_shared/team/handoff-protocols.md`.

### 2. Direct repo writes outside role scope
Check recent `DASHBOARD.md` commit summaries and `_archive/` for signs a non-owner role created or modified files outside their permitted scope.
- Strategist-owned: north-star, backlog, strategy docs only
- Role files, boot prompts, skills: HR Manager (roster/roles) or Engineer (template) or PM (operational files)

### 3. Role creation outside onboarding process
If a new `_inbox/{role}/` or `_shared/team/roles/{role}.md` appears that HR Manager did not create, flag it.

### 4. Sprint/scope directives from non-authorized sources
If any role other than {CEO_ROLE} or Strategist (via PM) files `type: task-brief` messages with implementation instructions to engineers, flag it.

## Severity levels

- **HIGH**: Direct repo write outside role scope; role created outside onboarding. Immediate {CEO_ROLE} notification.
- **MEDIUM**: Inbox routing violation. Note in loop report, notify PM.
- **LOW**: Minor scope creep in a message. Note only.

## When a violation is detected

1. Document: role, violation type, evidence, date
2. Notify {CEO_ROLE} immediately (`type: status-update`, `flag: guardrail-violation`) for HIGH
3. Notify PM (`type: status-update`) for MEDIUM and HIGH
4. Do not take corrective action -- PM routes the fix

## Report format

```
Guardrail Report {HH:MM} -- hr-manager
Violations detected: {n}
HIGH: {details or "none"}
MEDIUM: {details or "none"}
LOW: {details or "none"}
```

Include when violations exist. No report needed if clean.
