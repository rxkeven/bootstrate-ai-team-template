#!/usr/bin/env python3
"""
update_dashboard.py

Regenerates DASHBOARD.md from the current state of _inbox/ and projects/.

Run on every push via GitHub Actions, or manually:
    python scripts/update_dashboard.py

The script reads YAML frontmatter from every file in _inbox/{role}/ (excluding
.gitkeep), groups items by who they are addressed to and priority, and writes
a snapshot dashboard at DASHBOARD.md.
"""

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX_ROOT = REPO_ROOT / "_inbox"
ARCHIVE_ROOT = REPO_ROOT / "_archive" / "_inbox"
PROJECTS_ROOT = REPO_ROOT / "projects"
OUTPUT_PATH = REPO_ROOT / "DASHBOARD.md"

# Configure the CEO role identifier here; the bootstrap orchestrator sets this.
CEO_ROLE = os.environ.get("CEO_ROLE", "ceo")
COMPANY = os.environ.get("COMPANY", "Company")


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file's content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def read_inbox_items(role_dir: Path) -> list:
    """Return list of (filename, frontmatter dict) for messages in a role inbox."""
    items = []
    if not role_dir.exists():
        return items
    for path in sorted(role_dir.iterdir()):
        if path.name == ".gitkeep" or not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            items.append((path.name, fm))
        except Exception:
            continue
    return items


def list_active_roles() -> list:
    """All directories under _inbox/ (each is a role inbox)."""
    if not INBOX_ROOT.exists():
        return []
    return sorted([d.name for d in INBOX_ROOT.iterdir() if d.is_dir()])


def collect_archive_recent(days: int = 7) -> dict:
    """Scan _archive/_inbox for recently archived items by month directory."""
    recent_decisions = []
    recent_handoffs = []
    if not ARCHIVE_ROOT.exists():
        return {"decisions": recent_decisions, "handoffs": recent_handoffs}
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for role_dir in ARCHIVE_ROOT.iterdir():
        if not role_dir.is_dir():
            continue
        for month_dir in role_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for path in month_dir.iterdir():
                if path.name == ".gitkeep" or not path.is_file():
                    continue
                try:
                    content = path.read_text(encoding="utf-8")
                    fm = parse_frontmatter(content)
                    date_str = fm.get("date", "")
                    item_date = parse_iso(date_str)
                    if item_date and item_date >= cutoff:
                        msg_type = fm.get("type", "")
                        entry = (path.name, fm.get("from", "?"), role_dir.name)
                        if msg_type == "decision":
                            recent_decisions.append(entry)
                        elif msg_type in ("handoff", "context-handoff"):
                            recent_handoffs.append(entry)
                except Exception:
                    continue
    return {"decisions": recent_decisions, "handoffs": recent_handoffs}


def parse_iso(s: str):
    """Best-effort ISO timestamp parse."""
    if not s:
        return None
    s = s.strip().rstrip("Z")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def build_dashboard() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    roles = list_active_roles()

    # CEO-bound items
    ceo_items_high = []
    ceo_items_normal = []
    ceo_dir = INBOX_ROOT / CEO_ROLE
    for filename, fm in read_inbox_items(ceo_dir):
        from_role = fm.get("from", "?")
        msg_type = fm.get("type", "?")
        priority = fm.get("priority", "normal")
        project = fm.get("project", "shared")
        slug = filename.replace(".md", "")
        entry = f"- `{msg_type}` from **{from_role}** ({project}): {slug}"
        if priority in ("high", "urgent"):
            ceo_items_high.append(entry)
        else:
            ceo_items_normal.append(entry)

    # Per-role inbox counts
    inbox_counts = []
    for role in roles:
        count = sum(1 for _ in (INBOX_ROOT / role).iterdir() if _.name != ".gitkeep" and _.is_file())
        if count > 0 and role != CEO_ROLE:
            inbox_counts.append((role, count))

    archive_recent = collect_archive_recent(days=7)

    lines = []
    lines.append(f"# {COMPANY} AI Ops Dashboard")
    lines.append("")
    lines.append(f"_Auto-generated. Last updated: {now}_")
    lines.append("")
    lines.append("_This file is rebuilt on every push by the update-dashboard workflow. Do not edit manually._")
    lines.append("")

    # CEO section
    total_ceo = len(ceo_items_high) + len(ceo_items_normal)
    lines.append(f"## Waiting on {CEO_ROLE}")
    lines.append("")
    if total_ceo == 0:
        lines.append("_No items pending._")
    else:
        lines.append(f"**{total_ceo} item(s) pending.**")
        lines.append("")
        if ceo_items_high:
            lines.append("### High priority")
            lines.append("")
            lines.extend(ceo_items_high)
            lines.append("")
        if ceo_items_normal:
            lines.append("### Normal")
            lines.append("")
            lines.extend(ceo_items_normal)
    lines.append("")

    lines.append("## Active Work")
    lines.append("")
    lines.append("_No active tasks tracked yet._")
    lines.append("")

    # Inbox activity
    lines.append("## Inbox Activity")
    lines.append("")
    if not inbox_counts:
        lines.append("_All inboxes empty._")
    else:
        lines.append("| Agent | Pending Messages |")
        lines.append("|-------|------------------|")
        for role, count in inbox_counts:
            lines.append(f"| `{role}` | {count} |")
    lines.append("")

    # Recent decisions
    lines.append("## Recent Decisions (last 7 days)")
    lines.append("")
    if not archive_recent["decisions"]:
        lines.append("_No decisions logged in the past week._")
    else:
        for filename, from_role, to_role in archive_recent["decisions"]:
            lines.append(f"- {from_role} -> {to_role}: {filename}")
    lines.append("")

    # Recent handoffs
    lines.append("## Recent Handoffs (last 7 days)")
    lines.append("")
    if not archive_recent["handoffs"]:
        lines.append("_No handoffs logged in the past week._")
    else:
        for filename, from_role, to_role in archive_recent["handoffs"]:
            lines.append(f"- {from_role} -> {to_role}: {filename}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Generated by `scripts/update_dashboard.py`. Source: `_inbox/`, `projects/`._")
    return "\n".join(lines)


def main():
    output = build_dashboard()
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
