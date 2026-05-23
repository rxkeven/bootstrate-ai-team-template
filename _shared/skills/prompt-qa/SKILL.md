---
name: prompt-qa
description: 16-item boot prompt quality gate. Run against any role boot prompt before committing. All 16 must pass.
---

# Boot Prompt Quality Gate

Use this checklist when creating or reviewing a role boot prompt at `_shared/team/role-prompts/{role}.md`. All 16 items must pass before the prompt is committed. Fail = do not commit. Fix first.

Extracted from `_shared/skills/hr-manager/onboarding.md` Phase 2 for standalone use.

---

## When to run

- HR Manager: run on every new boot prompt created during onboarding (Phase 2)
- bs-code-eng: run when reviewing or updating existing boot prompts
- Any role reviewer: run when auditing role prompt quality

---

## The 16-item gate

| # | Item | Pass criteria |
|---|---|---|
| 1 | One-line identity | Role name, identifier, reports-to, surface present in opening line |
| 2 | Context-discipline reminder | Present near top of prompt; every-response format stated (`Context: ~X% used. Healthy.`) |
| 3 | Identity anchor | Re-paste instruction if session resets; names the file path to re-paste from |
| 4 | Role definition pointer | Points to `_shared/team/roles/{role}.md`; instruction to read on first cycle |
| 5 | Universal skills load order | All 5 listed in explicit numbered order; loop-sop first |
| 6 | Tools-to-load block | One ToolSearch call with `select:` syntax; includes all MCPs the role's surface supports |
| 7 | Where-things-live block | Inbox path, archive path (`_archive/_inbox/{role}/{YYYY-MM-DD}/`), repo access method, inboxes the role writes to |
| 8 | Scheduled monitor | Task ID, cron expression, loop type stated, DO NOT create duplicates warning |
| 9 | Session start steps | Numbered 1-N; todo check (`_todo/{role}.md`) appears before inbox check |
| 10 | Loop report format | Structured template with required fields: timestamp, inbox counts, health/status, next action |
| 11 | Swim lanes | Talk-to list, never-contact list, escalation criteria all present |
| 12 | Owns and does-not-own | Both sections present and non-empty |
| 13 | OpSec rules | No secrets/credentials, no out-of-scope writes, read-before-write stated |
| 14 | Self-improvement | References `_shared/skills/self-improvement/SKILL.md` |
| 15 | Standing conventions | Present; includes active-voice and one-question-max rules at minimum |
| 16 | Change log | Initial entry with date and author |

---

## Scoring

Count passes and fails before deciding to commit.

- **16/16 pass** — commit
- **Any fail** — do not commit; fix all failures; re-score

---

## Notes on item 5 (universal skills)

The 5 universal skills are:
1. `_shared/skills/loop-sop/SKILL.md`
2. `_shared/skills/team-comms/SKILL.md`
3. `_shared/skills/inbox-check/SKILL.md`
4. `_shared/skills/decision-escalation/SKILL.md`
5. `_shared/skills/context-discipline/SKILL.md`

Board and non-operational roles may omit some skills with documented justification.

## Notes on item 8 (scheduled monitor)

On-demand roles (e.g., Strategist, Designer) that have no recurring schedule may omit item 8 with a note: `Scheduled monitor: none — on-demand role, activated per task.`

## Notes on item 6 (tools-to-load)

The tool list must match what the role's surface and capabilities actually support. Claude Code roles need Bash and file tools. Cowork roles need GitHub MCP and scheduled-tasks. Verify against `_shared/team/roles/{role}.md` Surface and capabilities section.
