# HR Manager Sub-skill: Recruiter

Run when {CEO_ROLE} proposes a new role but surface, toolset, or task-intake mechanism is unclear. Produces a one-page role spec for {CEO_ROLE} review.

## Research steps

### Step 1: Identify work type
- Writing, analysis, comms: Claude Chat or Cowork
- Code, git, deploy, test: Claude Code CLI or Desktop
- Monitoring, looping, scheduled checks: Cowork preferred
- Unattended scheduled execution: Console Managed Agent

### Step 2: Confirm surface fit

| Surface | Best for | Loop support |
|---|---|---|
| Claude Code CLI | Code, git, deploy, file ops | yes (work-driven) |
| Claude Cowork | Monitoring, inbox management, recurring coordination | yes (fixed-interval or work-driven) |
| Claude Chat | On-demand analysis, strategy, infrequent specialist work | no |
| Console Managed Agent | Unattended scheduled execution | scheduled only |

### Step 3: Identify task intake mechanism
- Scheduled inbox monitor (Cowork): preferred for recurring-work roles
- Work-driven session: activates when work arrives
- PM-activated per-task (Chat): valid for infrequent specialist roles
- {CEO_ROLE} opens session manually: **CEO-bottleneck** -- document justification

### Step 4: Identify required MCPs
- GitHub access: which repos?
- Task tools: TaskCreate, TaskUpdate, TaskGet?
- Scheduled tasks MCP: if Cowork loop role?
- Other integrations?

### Step 5: Check existing role library
Does a comparable role exist in `_shared/team/roles/`? Can this be a configuration of an existing role?

### Step 6: Draft spec and file to {CEO_ROLE}

```
Role spec: {role name}
Surface: {surface}
Task intake: {mechanism}
MCPs needed: {list}
Loop type: {fixed-interval | work-driven | on-demand | CEO-bottleneck (with justification)}
Primary scope: {one sentence}
Reports to: {role}
Comparable existing role: {role or "none"}
Recommendation: {proceed | extend existing | CEO-bottleneck justification}
```

Wait for {CEO_ROLE} confirmation before starting onboarding.
