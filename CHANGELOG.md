# bootstrate-ai-team-template Changelog

## v1.2.1 — 2026-05-29

### Added
- Time-awareness enforcement across all role prompts and role templates: an A0 explicit `date` check before the kill-switch check, plus a "never estimate time from timestamps" rule in A0 and B1. Ported from the VH HR Manager v1.7 fix (root cause: time estimated from stale dashboard data produced a false end-of-day report). Validated by bs-validator 2026-05-28 (PASS on all role templates).
- Commit-batching policy in `_shared/skills/team-comms/` and role prompts: commit by logical operation (inbox-processing / outgoing-messages / discrete-decisions) rather than per file, with `push_files` guidance for multi-file commits. CEO-approved 2026-05-28.

## v1.2 — 2026-05-27 (finalized 2026-05-29)

V1.2 is the first versioned release of bootstrate-ai-team-template. As the inaugural release, this entry catalogs the full skill set and team assets that constitute the framework baseline.

### Skills (`_shared/skills/`)
- `preflight/` — kill-switch and inbox preflight (Flow A / Flow B)
- `remember/` — canonical full-context-load skill
- `loop-sop/` — loop SOP for all looping roles (incl. the date/time check)
- `team-comms/` — team communication protocol
- `inbox-check/` — inbox processing protocol
- `decision-escalation/` — CEO escalation protocol
- `context-discipline/` — context window management
- `council-consult/` — multi-role council consultation
- `standup/` — standup generation
- `task-router/` — task routing
- `engineer-loop/` — engineer loop SOP and boundary rules
- `prompt-qa/` — role-prompt quality assurance
- `self-improvement/` — self-improvement / retrospective
- `hr/`, `hr-manager/`, `hr-health-check/` — HR Manager operations and team health monitoring
- `ai-team-bootstrap/` — new-instance orchestrator (scaffolds new instances; template/new-instance only)

### Team assets (`_shared/team/`)
- `role-templates/` — genericized role prompt templates (finalized via Phase 2 HR Manager rewrites)
- `role-prompts/` — concrete role prompts
- `roles/` — role definitions
- `team-roster.md`, `handoff-protocols.md`, `onboarding-new-team-member.md`, `placeholders.md`, `first-flight-runbook.md`, `mcp-availability.md`

### Manifest
- `VERSION.md` — template version manifest
- `CHANGELOG.md` — this file

### Changed
- Role templates finalized via Phase 2 HR Manager rewrites — the prior "will be superseded post-Phase-2" caveat is resolved.
