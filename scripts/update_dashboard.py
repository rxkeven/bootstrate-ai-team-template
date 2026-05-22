#!/usr/bin/env python3
"""
update_dashboard.py

Regenerates DASHBOARD.md and public/index.html from the current state of
_inbox/, _archive/, and projects/.

Run on every push via GitHub Actions, or manually:
    python scripts/update_dashboard.py

Brand colors and fonts are read from _shared/brand/visual-identity.md
frontmatter. Falls back to Bootstrate defaults if unpopulated or missing.
"""

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX_ROOT = REPO_ROOT / "_inbox"
ARCHIVE_ROOT = REPO_ROOT / "_archive" / "_inbox"
PROJECTS_ROOT = REPO_ROOT / "projects"
OUTPUT_MD = REPO_ROOT / "DASHBOARD.md"
OUTPUT_HTML = REPO_ROOT / "public" / "index.html"

CEO_ROLE = os.environ.get("CEO_ROLE", "ceo")
COMPANY = os.environ.get("COMPANY", "Company")

# Bootstrate brand defaults (used when visual-identity.md is missing or empty)
BRAND_DEFAULTS = {
    "primary": "#1e293b",
    "accent": "#3b82f6",
    "background": "#f1f5f9",
    "text": "#0f172a",
    "surface": "#ffffff",
    "border": "#e2e8f0",
    "font_family": "Inter, system-ui, sans-serif",
    "font_family_mono": "ui-monospace, monospace",
}


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter key-value pairs from markdown content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def load_brand_vars() -> dict:
    """Load brand CSS variables from visual-identity.md, falling back to defaults."""
    identity_path = REPO_ROOT / "_shared" / "brand" / "visual-identity.md"
    if not identity_path.exists():
        return BRAND_DEFAULTS.copy()
    try:
        fm = parse_frontmatter(identity_path.read_text(encoding="utf-8"))
        # Merge: use file values where present, defaults elsewhere
        return {k: fm.get(k, v) for k, v in BRAND_DEFAULTS.items()}
    except Exception:
        return BRAND_DEFAULTS.copy()


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
    """Scan _archive/_inbox for recently archived items."""
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
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def gather_data() -> dict:
    """Collect all dashboard data into a single dict."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    roles = list_active_roles()

    ceo_items_high, ceo_items_normal = [], []
    ceo_dir = INBOX_ROOT / CEO_ROLE
    for filename, fm in read_inbox_items(ceo_dir):
        from_role = fm.get("from", "?")
        msg_type = fm.get("type", "?")
        priority = fm.get("priority", "normal")
        project = fm.get("project", "shared")
        slug = filename.replace(".md", "")
        entry = {"type": msg_type, "from": from_role, "project": project, "slug": slug}
        if priority in ("high", "urgent"):
            ceo_items_high.append(entry)
        else:
            ceo_items_normal.append(entry)

    inbox_counts = []
    for role in roles:
        count = sum(
            1 for _ in (INBOX_ROOT / role).iterdir()
            if _.name != ".gitkeep" and _.is_file()
        )
        if count > 0 and role != CEO_ROLE:
            inbox_counts.append((role, count))

    archive_recent = collect_archive_recent(days=7)

    return {
        "now": now,
        "ceo_items_high": ceo_items_high,
        "ceo_items_normal": ceo_items_normal,
        "inbox_counts": inbox_counts,
        "decisions": archive_recent["decisions"],
        "handoffs": archive_recent["handoffs"],
    }


def build_markdown(data: dict) -> str:
    now = data["now"]
    ceo_items_high = data["ceo_items_high"]
    ceo_items_normal = data["ceo_items_normal"]
    inbox_counts = data["inbox_counts"]
    decisions = data["decisions"]
    handoffs = data["handoffs"]

    lines = []
    lines.append(f"# {COMPANY} AI Ops Dashboard")
    lines.append("")
    lines.append(f"_Auto-generated. Last updated: {now}_")
    lines.append("")
    lines.append("_This file is rebuilt on every push by the update-dashboard workflow. Do not edit manually._")
    lines.append("")

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
            for e in ceo_items_high:
                lines.append(f"- `{e['type']}` from **{e['from']}** ({e['project']}): {e['slug']}")
            lines.append("")
        if ceo_items_normal:
            lines.append("### Normal")
            lines.append("")
            for e in ceo_items_normal:
                lines.append(f"- `{e['type']}` from **{e['from']}** ({e['project']}): {e['slug']}")
    lines.append("")

    lines.append("## Active Work")
    lines.append("")
    lines.append("_No active tasks tracked yet._")
    lines.append("")

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

    lines.append("## Recent Decisions (last 7 days)")
    lines.append("")
    if not decisions:
        lines.append("_No decisions logged in the past week._")
    else:
        for filename, from_role, to_role in decisions:
            lines.append(f"- {from_role} -> {to_role}: {filename}")
    lines.append("")

    lines.append("## Recent Handoffs (last 7 days)")
    lines.append("")
    if not handoffs:
        lines.append("_No handoffs logged in the past week._")
    else:
        for filename, from_role, to_role in handoffs:
            lines.append(f"- {from_role} -> {to_role}: {filename}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Generated by `scripts/update_dashboard.py`. Source: `_inbox/`, `_archive/`, `projects/`._")
    return "\n".join(lines)


def build_html(data: dict, brand: dict) -> str:
    now = data["now"]
    ceo_items_high = data["ceo_items_high"]
    ceo_items_normal = data["ceo_items_normal"]
    inbox_counts = data["inbox_counts"]
    decisions = data["decisions"]
    handoffs = data["handoffs"]

    def section(title: str, content: str) -> str:
        return f'<section><h2>{title}</h2>{content}</section>\n'

    def badge(text: str) -> str:
        return f'<span class="badge">{text}</span>'

    # CEO section
    total_ceo = len(ceo_items_high) + len(ceo_items_normal)
    if total_ceo == 0:
        ceo_html = '<p class="empty">No items pending.</p>'
    else:
        rows = ""
        for e in ceo_items_high:
            rows += f"<tr><td>{badge('high')}</td><td><code>{e['type']}</code></td><td>{e['from']}</td><td>{e['project']}</td><td>{e['slug']}</td></tr>\n"
        for e in ceo_items_normal:
            rows += f"<tr><td></td><td><code>{e['type']}</code></td><td>{e['from']}</td><td>{e['project']}</td><td>{e['slug']}</td></tr>\n"
        ceo_html = f'<p><strong>{total_ceo} item(s) pending.</strong></p><table><tr><th>Priority</th><th>Type</th><th>From</th><th>Project</th><th>Message</th></tr>{rows}</table>'

    # Inbox counts
    if not inbox_counts:
        inbox_html = '<p class="empty">All inboxes empty.</p>'
    else:
        rows = "".join(f"<tr><td><code>{role}</code></td><td>{count}</td></tr>" for role, count in inbox_counts)
        inbox_html = f'<table><tr><th>Agent</th><th>Pending</th></tr>{rows}</table>'

    # Decisions
    if not decisions:
        dec_html = '<p class="empty">No decisions logged in the past week.</p>'
    else:
        items = "".join(f"<li>{fr} &rarr; {to}: {fn}</li>" for fn, fr, to in decisions)
        dec_html = f"<ul>{items}</ul>"

    # Handoffs
    if not handoffs:
        hoff_html = '<p class="empty">No handoffs logged in the past week.</p>'
    else:
        items = "".join(f"<li>{fr} &rarr; {to}: {fn}</li>" for fn, fr, to in handoffs)
        hoff_html = f"<ul>{items}</ul>"

    body = (
        section(f"Waiting on {CEO_ROLE}", ceo_html)
        + section("Active Work", '<p class="empty">No active tasks tracked yet.</p>')
        + section("Inbox Activity", inbox_html)
        + section("Recent Decisions (last 7 days)", dec_html)
        + section("Recent Handoffs (last 7 days)", hoff_html)
    )

    p = brand["primary"]
    a = brand["accent"]
    bg = brand["background"]
    tx = brand["text"]
    su = brand["surface"]
    bo = brand["border"]
    ff = brand["font_family"]
    fm = brand["font_family_mono"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{COMPANY} AI Ops Dashboard</title>
<style>
:root{{
  --primary: {p};
  --accent: {a};
  --background: {bg};
  --text: {tx};
  --surface: {su};
  --border: {bo};
  --font: {ff};
  --mono: {fm};
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--background);color:var(--text);font-family:var(--font);padding:0}}
header{{background:var(--primary);color:#fff;padding:1.25rem 2rem}}
header h1{{font-size:1.1rem;font-weight:600}}
.meta{{font-size:0.75rem;opacity:0.7;margin-top:0.25rem}}
main{{padding:1.5rem 2rem;max-width:900px;margin:0 auto}}
section{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:1.25rem;margin-bottom:1rem}}
h2{{font-size:0.9rem;font-weight:600;color:var(--primary);margin-bottom:0.75rem;text-transform:uppercase;letter-spacing:0.05em}}
table{{width:100%;border-collapse:collapse;font-size:0.85rem}}
th{{text-align:left;border-bottom:2px solid var(--border);padding:0.4rem 0.5rem;font-weight:600}}
td{{padding:0.4rem 0.5rem;border-bottom:1px solid var(--border)}}
code{{background:var(--background);padding:0.1em 0.35em;border-radius:3px;font-family:var(--mono);font-size:0.8em}}
.badge{{display:inline-block;background:var(--accent);color:#fff;border-radius:999px;padding:0.1em 0.5em;font-size:0.75em;font-weight:600}}
.empty{{color:#888;font-style:italic;font-size:0.875rem}}
ul{{list-style:none;font-size:0.875rem}}li{{padding:0.3rem 0;border-bottom:1px solid var(--border)}}li:last-child{{border-bottom:none}}
footer{{text-align:center;font-size:0.7rem;color:#aaa;padding:1.5rem 2rem}}
</style>
</head>
<body>
<header>
  <h1>{COMPANY} AI Ops Dashboard</h1>
  <div class="meta">Last updated: {now} &mdash; auto-generated</div>
</header>
<main>
{body}</main>
<footer>Generated by <code>scripts/update_dashboard.py</code> &middot; Source: <code>_inbox/</code>, <code>_archive/</code>, <code>projects/</code></footer>
</body>
</html>
"""


def main():
    brand = load_brand_vars()
    data = gather_data()

    OUTPUT_MD.write_text(build_markdown(data), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(build_html(data, brand), encoding="utf-8")
    print(f"Wrote {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
