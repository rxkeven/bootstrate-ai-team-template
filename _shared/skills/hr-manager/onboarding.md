# HR Manager Sub-skill: Onboarding

Full Phase 0-6 process for adding a new role. {CEO_ROLE} directs; HR Manager executes.

---

## Phase 0: Authorization

Confirm {CEO_ROLE} direction exists: a message in `_inbox/hr-manager/` or explicit session instruction. Do not begin without confirmed authorization.

## Phase 0b: Identify the requester

Before beginning Phase 1, identify who originated this role request:

- **{CEO_ROLE} originated it directly:** {CEO_ROLE} is the sole Phase 1 spec approver. Proceed.
- **PM originated it:** PM must review the Phase 1 spec before {CEO_ROLE} approves. Send draft spec to PM first. Only then does the spec go to {CEO_ROLE}.
- **Strategist originated it:** Same as PM -- Strategist reviews Phase 1 spec first.

Reason: {CEO_ROLE} should not be the QA step for a spec mismatch that PM or Strategist would catch immediately.

---

## Phase 1: Role specification

### Phase 1a: Collect from {CEO_ROLE}

- Role name and identifier
- Surface (Claude Cowork, Claude Chat, Claude Code, Console Managed Agent)
- Reports-to
- Primary scope (one sentence)

If surface or toolset is unclear, run `recruiter.md` before proceeding.

### Phase 1b: Evaluate the role

| Dimension | Question |
|---|---|
| Surface fit | Is the proposed surface right for the work type? See `recruiter.md` for surface fit matrix. |
| Loop type | Which loop type? Fixed-interval / work-driven / on-demand / CEO-bottleneck. See `_shared/skills/loop-sop/SKILL.md`. |
| Task intake | How does this role receive new work without {CEO_ROLE} intervening? If the answer requires {CEO_ROLE} to manually open a session or paste a brief, that is a CEO-bottleneck. Not acceptable for recurring-work roles. Propose a scheduled inbox monitor or event trigger instead. Claude Chat with no scheduled monitor requires explicit {CEO_ROLE} sign-off with a documented reason. |
| Swim lanes | Who does this role talk to? Who is forbidden? |
| Tool access | Which MCPs and tools does this role need? |

### Phase 1c: Requester review (if applicable)

If PM or Strategist originated the request (Phase 0b), send draft spec to them before {CEO_ROLE}. Wait for their confirmation.

### Phase 1d: Draft spec for {CEO_ROLE} approval

File to `_inbox/{CEO_ROLE}/` (type: `task-brief`, subject: role spec for approval):

```
1. Role name and identifier
2. Surface
3. Reports-to
4. Primary scope (one sentence)
5. Loop type -- fixed-interval | work-driven | on-demand | CEO-bottleneck (with justification)
6. Tool access -- list of MCPs and tools
7. Swim lanes -- talk-to and never-contact list
8. Task intake mechanism -- How does this role receive new assignments without {CEO_ROLE} intervening?
   Options: scheduled inbox monitor (Cowork), Bash cron (Code), event-triggered webhook,
   PM-activated per-task session (valid for infrequent specialist work).
   If "{CEO_ROLE} opens a Chat session": document why and get explicit sign-off.
```

Wait for {CEO_ROLE} approval before proceeding to Phase 2.

---

## Phase 2: Boot prompt quality gate

Write the boot prompt for `_shared/team/role-prompts/{role}.md`. Run the 16-item quality gate. All 16 must pass before committing.

### 16-item boot prompt quality gate

| # | Item | Pass criteria |
|---|---|---|
| 1 | One-line identity | Role name, identifier, reports-to, surface present |
| 2 | Context-discipline reminder | Top of prompt, every-response format stated |
| 3 | Identity anchor | Re-paste instruction if session resets |
| 4 | Role definition pointer | Points to `_shared/team/roles/{role}.md` |
| 5 | Universal skills load order | All 4 listed in explicit numbered order |
| 6 | Tools-to-load block | One ToolSearch call with `select:` syntax |
| 7 | Where-things-live block | Inbox path, archive path, repos |
| 8 | Scheduled monitor | Task ID, loop type, DO NOT duplicate check |
| 9 | Session start steps | Numbered 1-N, todo before inbox |
| 10 | Loop report format | Structured template with required fields |
| 11 | Swim lanes | Talk-to, never-contact, escalation criteria |
| 12 | Owns and does-not-own | Both sections present |
| 13 | OpSec rules | No secrets, no out-of-scope writes, read-before-write |
| 14 | Self-improvement section | References `_shared/skills/self-improvement/SKILL.md` |
| 15 | Standing conventions | Present |
| 16 | Change log | Initial entry with date |

Fail = do not commit. Fix first.

---

## Phase 3: Create role definition file

Create `_shared/team/roles/{role}.md`. Required sections: identity, surface and capabilities, owns, does not own, communication paths, loop cadence, standing conventions.

Commit: `feat: add role definition for {role}`

---

## Phase 4: Infrastructure

1. Create `_inbox/{role}/.gitkeep` -- Commit: `chore: create inbox for {role}`
2. Create `_todo/{role}.md` (blank from `_shared/ops/todo-protocol.md`) -- Commit: `chore: create todo for {role}`

---

## Phase 5: Activation checklist

Verify all 7 before announcing activation:

- [ ] Role definition file exists
- [ ] Boot prompt exists and passed 16-item quality gate (all 16 pass)
- [ ] Inbox directory exists
- [ ] Todo file exists
- [ ] Team roster updated
- [ ] Welcome brief filed to `_inbox/{role}/`
- [ ] PM notified of roster addition

---

## Phase 6: Notifications

1. Update roster -- `docs: roster add {role}`
2. Notify PM -- `status-update` to `_inbox/pm/` (informing, not asking permission)
3. File welcome brief -- `_inbox/{role}/` with identity, skill pointers, first-cycle instructions
4. Report to {CEO_ROLE} -- `task-completion` to `_inbox/{CEO_ROLE}/` with role identifier, start date, quality gate pass status

---

## Session types reference

See `_shared/skills/loop-sop/SKILL.md` for full session type definitions.

**Per-task (valid):** PM dispatches a specific task brief. Role activates, processes, delivers, ends.

**Scheduled loop (preferred for recurring-work roles):** Role runs on a scheduled cadence. Checks inbox autonomously without {CEO_ROLE} or PM triggering a session.

**CEO-bottleneck (anti-pattern -- avoid unless justified):** {CEO_ROLE} must manually open a session for the role to receive any work. Acceptable only for genuinely infrequent specialist roles. Requires explicit {CEO_ROLE} sign-off with documented reason.

---

## Special cases: sunsetting a role

If a new role makes an existing role redundant, run `offboarding.md` for the outgoing role as part of the same onboarding cycle. Document the transition in both role files.
