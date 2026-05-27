---
name: preflight
description: Lightweight pre-work check that decides whether a session-start or loop tick has any work to do before paying the cost of a full context load. Two flows (A = session-start, B = loop-tick).
---

# Preflight Skill

Fast, explicit script that decides whether work exists before paying the cost of a full context load.

Two flows:
- **Flow A — Session start** (fresh process, role-prompt pasted)
- **Flow B — Loop tick** (cron fires inside a live session)

Pair with `_shared/skills/remember/SKILL.md`.

---

## Flow A — Session start

### A1. Minimal identity load

Already done by the role-prompt header. At this point you know:
- Role identifier and manager
- Inbox path
- `SYSTEM_STATE.md` `LOOPS_ENABLED` value
- `_state/{role}/last-remember-utc.txt` is treated as **null** (fresh process)

### A2. Preflight script

**Step 1 — Inbox count**
- Tool: `{GITHUB_MCP}__get_file_contents`
- Args: `owner={COMPANY_SLUG}`, `repo={COMPANY}-ai-ops`, `path=_inbox/{role}/`
- Set: `inbox_has_work = (non-.gitkeep file count > 0)`

**Step 2 — Handoff check (SESSION-START ONLY)**
- Tool: `{GITHUB_MCP}__get_file_contents`
- Args: `path=_handoff/{role}/`
- Set: `handoff_pending = (any non-.gitkeep .md present)`

**Step 3 — Todo HIGH/URGENT scan**
- Tool: `{GITHUB_MCP}__get_file_contents`
- Args: `path=_todo/{role}.md`
- Scan for lines containing `| HIGH |` or `| URGENT |` in the `## Active` section
- Set: `todo_urgent = (matches > 0)`

**Step 4 — Kill switch**
Already computed in A1. If `LOOPS_ENABLED` not exactly lowercase `true`, halt and run End-of-day SOP.

### A3. Branch

```
work_found = inbox_has_work || handoff_pending || todo_urgent

if !work_found:
    Print: "Preflight clean: 0 inbox, 0 handoff, 0 urgent todo. Idle."
    Schedule next check per role cadence
    End turn

if work_found:
    Invoke /remember (reads _shared/skills/remember/SKILL.md, loads full context)
    Write _state/{role}/last-remember-utc.txt with current ISO UTC
    Process the work
```

---

## Flow B — Loop tick

### B1. Preflight script

**Step 1 — Inbox count** (same as A2 Step 1)

**Step 2 — SKIP** — handoff check is session-start only. If `_handoff/{role}/` is non-empty during a loop tick, treat as alert condition — surface to user and continue normally.

**Step 3 — Todo HIGH/URGENT scan** (same as A2 Step 3)

**Step 4 — Kill switch** — re-read `SYSTEM_STATE.md`. Halt if `LOOPS_ENABLED` not exactly `true`.

**Step 5 — Context freshness**
- Read `_state/{role}/last-remember-utc.txt`
- `context_stale = (now - last_remember_utc > 60 min)`
- Missing or unparseable → `context_stale = true` (fail-safe)

### B2. Branch

```
work_found = inbox_has_work || todo_urgent

if !work_found:
    Write: "Loop {HH:MM} — clean"
    Reschedule next tick
    End turn

if work_found && !context_stale:
    Process the work directly. Context is fresh.

if work_found && context_stale:
    Invoke /remember
    Update _state/{role}/last-remember-utc.txt
    Process the work
```

### B3. Refresh marker (always, end of tick)

Before scheduling the next loop or ending the turn, write `_state/{role}/last-remember-utc.txt` with current ISO UTC. Applies to ALL three B2 branches. Keeps the freshness proxy accurate within long sessions.

---

## What counts as work

1. **Inbox** — any non-.gitkeep file in `_inbox/{role}/`
2. **Handoff** — any non-.gitkeep .md in `_handoff/{role}/` (Flow A only)
3. **Todo HIGH or URGENT** — any line containing `| HIGH |` or `| URGENT |` in the `## Active` section of `_todo/{role}.md`

MEDIUM and LOW todo items do not trigger work-found. They are processed if a tick is already happening for other reasons.

---

## Failure modes and fail-safes

- **Missing `_state/{role}/last-remember-utc.txt`** → `context_stale = true`, force /remember
- **Unparseable timestamp** → `context_stale = true`
- **Inbox path returns 404** → surface to user and halt. Path bug is unrecoverable without human intervention.
- **`LOOPS_ENABLED` not exactly `true`** → halt, run End-of-day SOP
- **`_handoff/{role}/` non-empty during Flow B** → alert condition, continue Flow B normally

---

## Why this design

The old pattern loaded everything (universal skills, role file, todo, recent handoffs) on every session start and every loop tick. That burned tokens on cycles where there was nothing to do.

Preflight is the cheap gate. Three small `get_file_contents` calls answer "is there work?" in ~3k tokens. Only when the answer is yes do we pay the full context-load cost via /remember.

The 60-minute freshness window on Flow B is the second optimisation — once /remember has loaded context, subsequent loop ticks within an hour skip the reload.

---

## Change log

- 2026-05-27 v1.0 — Ported to bootstrate-ai-team-template (Phase 1 sprint). Placeholders applied for COMPANY_SLUG, COMPANY, GITHUB_MCP.
