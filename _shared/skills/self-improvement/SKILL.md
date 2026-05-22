# Skill: Self-Improvement

Allows any active role to propose changes to their own role definition, boot prompt, or toolset. All proposals route to HR Manager. Do not self-approve. Do not implement before HR Manager approves.

## When to use

- Your role definition is outdated or incomplete
- A recurring friction point suggests a boot prompt change
- You need access to a tool or MCP not in your toolset
- A standing convention should be updated

## How to submit

1. Write a proposal (format below)
2. File to `_inbox/hr-manager/` as `type: self-improvement-proposal`
3. Do not implement before HR Manager replies with approval
4. Scope expansions (new tools, MCPs, cross-role changes) will be escalated by HR Manager to {CEO_ROLE}

## Proposal format

```markdown
---
from: {your-role}
to: hr-manager
type: self-improvement-proposal
date: {ISO-timestamp}
---

## What I want to change
{brief description}

## Current state
{quote the current section}

## Proposed new state
{your proposed change}

## Why
{one paragraph rationale}

## Scope assessment
[ ] This change affects only my own role
[ ] This change requires new tools or MCPs (escalate to {CEO_ROLE})
[ ] This change affects how I interact with other roles (notify pm)
```

## HR Manager review

HR Manager reviews within one loop cycle:
- Own-role-only changes: approve or reject with explanation
- Scope expansions: escalate to {CEO_ROLE} with recommendation
- HR Manager never auto-approves

Response goes to `_inbox/{your-role}/` as `type: status-update`, `status: approved` or `status: rejected`.
