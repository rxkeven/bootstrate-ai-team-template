# HR Manager Sub-skill: Roster Maintenance

Review and maintain `_shared/team/team-roster.md`. Run at the start of every loop cycle.

## On every loop

1. Read `_shared/team/team-roster.md`.
2. Check for discrepancies:
   - Role listed as Active but `_inbox/{role}/` does not exist
   - Role listed as Active but no role file in `_shared/team/roles/`
   - Role listed as Active but no boot prompt in `_shared/team/role-prompts/`
   - New role appeared that HR Manager did not create (flag to {CEO_ROLE}; check guardrail-monitor.md)
3. Flag discrepancies in the loop report.

## Update triggers

- New role activated (onboarding Phase 6)
- Role offboarded (offboarding step 3)
- Role's surface or status changes

## Rules

- **Never delete a row.** Mark retired roles `Offboarded` with date and reason.
- **Always add a change log entry** for every modification.
- **Notify PM** on any roster change that affects project coordination.

## Roster columns

| Column | Values |
|---|---|
| Role | Display name |
| Identifier | Lowercase hyphenated |
| Surface | Claude Cowork / Claude Chat / Claude Code / Console Managed Agent |
| Reports to | Role identifier or `{CEO_ROLE}` |
| Status | Active / Active (on-demand) / Active (per-checkpoint) / Offboarded |
| Started | ISO date |
