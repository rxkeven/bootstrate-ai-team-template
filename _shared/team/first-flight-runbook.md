# First-Flight Runbook

The smallest end-to-end test that proves a freshly-bootstrapped {COMPANY} AI team works. Run this immediately after the ai-team-bootstrap engagement closes. If the runbook passes, V1 operating model is live. If it fails, the failure point names the gap.

## Why this runbook exists

A scaffolded repo is not a working team. Files compile but communication does not. This runbook exercises the four load-bearing pieces of the architecture in one round-trip:

1. **Surface boot.** PM Cowork and Engineer Code sessions actually load and read their boot prompts.
2. **Hub-and-spoke routing.** PM receives, dispositions, and routes a brief without bypassing the hub.
3. **Escalation path.** A real blocker escalates to {CEO_ROLE}, decision returns, work resumes.
4. **Audit trail.** Dashboard regenerates, archive moves complete, commit history reflects the round-trip.

Fifteen to thirty minutes of CEO attention is enough to run it.

## Pre-flight checklist

Before starting, verify:

- Bootstrap engagement closed cleanly (status note committed to `_inbox/{CEO_ROLE}/`).
- GitHub repository variables `CEO_ROLE` and `COMPANY` are set on the target ops repo. Trigger a manual dashboard regen and confirm DASHBOARD.md renders with the substituted values, not the defaults.
- A code repo exists for the project the test sprint will exercise (Engineer needs somewhere to point even if the brief is just a smoke task).
- GitHub MCP is configured in your Cowork environment with write access to the ops repo.
- One PM Cowork session is registered with task ID `pm-inbox-monitor` on a `*/30 * * * *` cron.
- One Engineer Claude Code session is open against the code repo and the ops repo, with the engineer boot prompt pasted.
- No actual production work depends on the test sprint window. This is a smoke run.

## The round-trip

### Step 1: CEO writes the test brief

Action: Write a `task-brief` to `_inbox/pm/` with a deliberately tiny scope. Suggested content:

```yaml
---
from: {CEO_ROLE}
to: pm
project: {PROJECT_SLUG}
type: task-brief
priority: normal
date: {ISO-timestamp}
---
# First-flight smoke: add a README badge

Add a "first flight verified" badge to the project README in the code repo. One file change. No tests required. Acceptance: badge renders in GitHub UI.
```

Commit: `msg: {CEO_ROLE} -> pm: first-flight smoke brief`

**Pass signal:** Commit lands. DASHBOARD.md regenerates within ~30 seconds showing `pm` with 1 pending message.

**Fail signal:** The GitHub Action does not trigger, or DASHBOARD.md shows defaults `Company` / `ceo`. Cause: repo variables not set, or the GitHub Action's path filter missed `_inbox/pm/`. Fix the repo variables or the GitHub Action's path filter before continuing.

### Step 2: PM picks up the brief on its next tick

Wait up to 30 minutes (or trigger the PM session manually). When PM runs:

- Reads its role file
- Runs inbox-check
- Finds the brief
- Issues a `task-brief` to `_inbox/engineer/` (or `engineer-{PROJECT_SLUG}` for multi-project teams)
- Archives the original CEO brief (two-commit pattern)

Commits to look for: 
- `msg: pm -> engineer: first-flight smoke task`
- `chore: archive pm inbox {filename}`
- `chore: archive pm inbox {filename} (move complete)`

**Pass signal:** All three commits land. DASHBOARD.md regenerates showing `engineer` with 1 pending message and `pm` empty.

**Fail signal:** PM does not write to Engineer's inbox, or writes directly back to CEO bypassing the hub-and-spoke. Cause: boot prompt missing a `select:` tool load for `create_or_update_file`, or hub-and-spoke routing was not internalized. Re-check PM's boot prompt and CLAUDE.md routing section.

### Step 3: Engineer picks up the brief

In the Engineer Code session, run the boot prompt's first-actions: inbox-check, read the task-brief.

Engineer's expected behavior: read the brief, recognize it as a smoke task, but deliberately surface a blocker for the runbook's sake. (We are exercising the escalation path, not the happy path.)

Write a `blocker` to `_inbox/pm/`:

```yaml
---
from: engineer
to: pm
project: {PROJECT_SLUG}
type: blocker
priority: normal
date: {ISO-timestamp}
references:
  - _archive/_inbox/engineer/{YYYY-MM}/{brief-filename}
---
# First-flight: cannot determine badge URL

Need authorization to add a custom badge that links to the ops repo dashboard. The URL points outside the project domain; flagging before commit.
```

Commit: `msg: engineer -> pm: first-flight blocker on badge URL`

**Pass signal:** Engineer writes to PM (not directly to CEO, not directly to Strategist). Blocker lands in `_inbox/pm/`.

**Fail signal:** Engineer writes directly to CEO or Strategist. Cause: forbidden-direct-path enforcement absent. Re-check Engineer role file and handoff-protocols.md, and verify the canonical state always wins rule was read on session start.

### Step 4: PM escalates the blocker to CEO

PM's next tick reads the blocker. Per decision-escalation, this is an inter-role conflict (sort of, since "authorization" is not in Engineer's scope), so PM escalates to CEO with options.

Write a `decision-request` to `_inbox/{CEO_ROLE}/`:

```yaml
---
from: pm
to: {CEO_ROLE}
project: {PROJECT_SLUG}
type: decision-request
priority: normal
{CEO_ROLE}_required: true
decision_needed: true
date: {ISO-timestamp}
---
# First-flight: badge link target

Engineer flagged a badge URL pointing outside the project domain. Options:

1. Link badge to ops repo dashboard (cross-domain, requires CEO ok)
2. Link badge to the code repo's own README anchor (no cross-domain)
3. Drop the badge entirely; runbook does not require a visible artifact

Recommendation: Option 2. Smaller blast radius and still proves the round-trip.

If no response by EOD, will default to Option 2.
```

Commit: `escalation: pm -> {CEO_ROLE}: first-flight badge target`

**Pass signal:** Decision-request lands in CEO inbox. DASHBOARD.md shows CEO with 1 pending. PM does NOT loop on this; PM continues parallel work or reports tick complete.

**Fail signal:** PM acts unilaterally without escalating. Cause: decision-escalation skill not internalized, or PM treated this as routine. Re-verify PM read the decision-escalation skill.

### Step 5: CEO returns a decision

CEO writes a `decision` to `_inbox/pm/`:

```yaml
---
from: {CEO_ROLE}
to: pm
project: {PROJECT_SLUG}
type: decision
priority: normal
references:
  - _inbox/{CEO_ROLE}/{escalation-filename}
date: {ISO-timestamp}
---
# Decision: first-flight badge target

Go with Option 2. Link to the README anchor. Document in the engineering doc that cross-domain badges require a separate review.
```

Commit: `decision: {PROJECT_SLUG}: first-flight badge target`

CEO archives the escalation message in `_inbox/{CEO_ROLE}/` (two-commit pattern). If a PA Cowork role is registered, PA may execute the archive after notifying CEO; otherwise CEO does it directly.

**Pass signal:** Decision file lands in PM's inbox. CEO's inbox empty in next dashboard regen.

**Fail signal:** Decision routed to Engineer directly. Cause: hub-and-spoke violated from the CEO side too. Reinforce that CEO replies route to the role that escalated, not skipping over PM.

### Step 6: PM routes decision to Engineer

PM's next tick reads the decision. PM writes a `task-brief` (or follow-up message) to Engineer with the disposition.

```yaml
---
from: pm
to: engineer
project: {PROJECT_SLUG}
type: task-brief
priority: normal
references:
  - _archive/_inbox/pm/{YYYY-MM}/{original-brief-filename}
  - _archive/_inbox/pm/{YYYY-MM}/{decision-filename}
date: {ISO-timestamp}
---
# First-flight: unblocked — proceed with Option 2

CEO decision: link the badge to the README anchor. Proceed.
```

Commit: `msg: pm -> engineer: first-flight unblocked`

PM also archives the blocker and the decision in `_inbox/pm/` (two two-commit patterns).

**Pass signal:** Engineer inbox has the unblock message. PM inbox empty.

### Step 7: Engineer completes and reports done

Engineer takes the action in the code repo (or simulates it with a no-op commit if the actual badge is out of scope), then writes a `status-update` to `_inbox/pm/`:

```yaml
---
from: engineer
to: pm
project: {PROJECT_SLUG}
type: status-update
priority: normal
date: {ISO-timestamp}
---
# First-flight smoke: complete

Badge added per Option 2. README anchor link. Smoke run complete.
```

Commit: `msg: engineer -> pm: first-flight smoke complete`

PM archives this on next tick and writes a closeout to `_inbox/{CEO_ROLE}/`:

```yaml
---
from: pm
to: {CEO_ROLE}
project: {PROJECT_SLUG}
type: status-update
priority: normal
date: {ISO-timestamp}
---
# First-flight smoke: closed

Round-trip verified: brief -> Engineer -> blocker -> escalation -> decision -> unblock -> done. All hub-and-spoke paths respected. Archive complete. Dashboard reflects empty inboxes.
```

**Pass signal:** Final closeout message lands in CEO inbox. DASHBOARD.md eventually regenerates with all inboxes empty and recent-decisions section showing the badge-target decision.

## Overall pass criteria

The runbook passes when:

1. All six message files traversed the expected hub-and-spoke path with the right `from` and `to` fields.
2. No forbidden direct paths were used (no engineer-to-CEO, no engineer-to-strategist, no PM-to-other-PM).
3. The archive moved every actioned message (two-commit pattern executed on each).
4. DASHBOARD.md correctly reflected the inbox state at each step.
5. Repo variable substitution worked (dashboard says `{COMPANY}` and `{CEO_ROLE}`, not the defaults).
6. Total elapsed wall-clock time was 15 to 60 minutes depending on PM polling cadence and the runner's pace.

## What a failure tells you

| Failure | Likely cause |
|---|---|
| Step 1 fails: dashboard does not regenerate | GitHub Action not committed, or path filter wrong, or repo permission missing |
| Step 1 fails: dashboard shows `Company`/`ceo` defaults | Repo variables `CEO_ROLE` / `COMPANY` not set (B5 substep skipped) |
| Step 2 fails: PM does not pick up the brief | PM scheduled task not registered, or boot prompt did not load tool selection |
| Step 2 fails: PM bypasses Engineer | Hub-and-spoke not internalized; re-read CLAUDE.md routing section |
| Step 3 fails: Engineer routes to CEO directly | Forbidden direct paths not enforced; re-read handoff-protocols.md |
| Step 4 fails: PM does not escalate | decision-escalation skill not in boot prompt, or PM treated as routine |
| Step 5 fails: CEO decision routes to Engineer | Verify CEO understands the hub returns through PM |
| Step 7 fails: archive does not complete | Two-commit pattern not understood; review inbox-check archive steps |

## After the runbook passes

- Commit a status-update to `_inbox/{CEO_ROLE}/` with subject "first-flight verified"
- Update `_shared/team/team-roster.md` change log with: "{DATE}: first-flight runbook passed; team operationally live"
- Begin the first real sprint
- Schedule a 1-week retrospective to capture friction observed in the first real cycle

## Re-running the runbook

Re-run after:

- Adding or retiring a role (run the abbreviated 4-step version covering the new role's inbox)
- Surface migration of an existing role
- Any change to CLAUDE.md routing rules or handoff-protocols.md
- A real incident that suggests the round-trip may have regressed

This runbook is intentionally low-cost. Re-run it any time you suspect drift.
