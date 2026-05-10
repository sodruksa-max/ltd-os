"""
weekly-audit.py — ตรวจสุขภาพระบบรายสัปดาห์ + หาจุดอ่อน
Run: Sunday 10:00 AM Thailand (3:00 AM UTC) via GitHub Actions
Output: vault/90_archive/weekly-audits/YYYY-W##.md
"""

import os
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

from groq import Groq

REPO = Path(__file__).resolve().parent.parent
VAULT = REPO / "vault"
AUDIT_DIR = VAULT / "90_archive" / "weekly-audits"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = date.today()
WEEK = TODAY.isocalendar()[1]
YEAR = TODAY.year
AUDIT_FILE = AUDIT_DIR / f"{YEAR}-W{WEEK:02d}.md"


# ── Helpers ──────────────────────────────────────────────────────────────────

def word_count(text: str) -> int:
    return len(text.split())


def days_old(path: Path) -> int:
    mtime = datetime.fromtimestamp(path.stat().st_mtime).date()
    return (TODAY - mtime).days


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


# ── Check 1: Inbox ────────────────────────────────────────────────────────────

def check_inbox() -> list[str]:
    inbox = VAULT / "00_inbox"
    issues = []
    if not inbox.exists():
        return issues
    for f in inbox.glob("*.md"):
        if f.name == "README.md":
            continue
        age = days_old(f)
        if age > 7:
            issues.append(f"  - `{f.name}` — ค้างมา {age} วัน")
    return issues


# ── Check 2: Note size ────────────────────────────────────────────────────────

def check_note_sizes() -> list[str]:
    issues = []
    skip_dirs = {"90_archive", "_assets", "_templates", "_memory", "daily"}
    for md in VAULT.rglob("*.md"):
        if any(p in md.parts for p in skip_dirs):
            continue
        text = read_file(md)
        wc = word_count(text)
        rel = md.relative_to(VAULT)
        if wc >= 5000:
            issues.append(f"  - `{rel}` — {wc:,} คำ ⛔ เกิน block limit")
        elif wc >= 2000:
            issues.append(f"  - `{rel}` — {wc:,} คำ ⚠️ เกิน warn limit")
    return issues


# ── Check 3: Daily notes gap ──────────────────────────────────────────────────

def check_daily_gaps() -> list[str]:
    daily_dir = VAULT / "daily"
    issues = []
    existing = {f.stem for f in daily_dir.glob("????-??-??.md")}
    for i in range(1, 8):
        d = (TODAY - timedelta(days=i)).isoformat()
        if d not in existing:
            issues.append(f"  - `{d}` — ไม่มี daily note")
    return issues


# ── Check 4: Nick KB gaps HIGH ───────────────────────────────────────────────

def check_nick_kb_gaps() -> list[str]:
    weekly_dir = VAULT / "20_investment" / "nick" / "weekly"
    files = sorted(weekly_dir.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return ["  - ไม่พบ weekly rec"]
    text = read_file(files[0])
    rec_date = files[0].stem.split("_")[0]
    issues = []
    gaps_match = re.search(r"## KB Gaps.*?\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if gaps_match:
        for line in gaps_match.group(1).splitlines():
            if "| High |" in line or "HIGH" in line.upper():
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 3 and parts[0] not in ("Topic", "---"):
                    issues.append(f"  - HIGH: **{parts[0]}** — {parts[1]} (จาก {rec_date})")
    return issues


# ── Check 5: NAV log freshness ───────────────────────────────────────────────

def check_nav_freshness() -> list[str]:
    nav_log = VAULT / "20_investment" / "nick" / "performance" / "nav_log.md"
    if not nav_log.exists():
        return ["  - nav_log.md ไม่มี"]
    text = read_file(nav_log)
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if not dates:
        return ["  - nav_log.md ไม่มีข้อมูล"]
    last = dates[-1]
    last_date = date.fromisoformat(last)
    age = (TODAY - last_date).days
    if age > 3:
        return [f"  - NAV log ล่าสุด: {last} ({age} วันที่แล้ว) — ควรอัปเดต"]
    return []


# ── Check 6: Git uncommitted ─────────────────────────────────────────────────

def check_git_status() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, cwd=REPO
        )
        lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
        if lines:
            return [f"  - {len(lines)} ไฟล์ที่ยังไม่ commit: " + ", ".join(l[3:] for l in lines[:5])]
        return []
    except Exception:
        return []


# ── Check 7: Open questions from last weekly review ───────────────────────────

def get_open_questions() -> list[str]:
    files = sorted((VAULT / "90_archive" / "weekly-reviews").glob("*.md"), reverse=True)
    if len(files) < 1:
        return []
    text = read_file(files[0])
    qs = re.findall(r"-\s+(.+\?)", text)
    return qs[:5]


# ── Check 8: Git log patterns (last 14 days) ──────────────────────────────────

def get_git_log() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--since=14 days ago", "--pretty=format:%s"],
            capture_output=True, text=True, cwd=REPO
        )
        return result.stdout.strip()
    except Exception:
        return ""


# ── Check 9: OUTCOMES patterns ───────────────────────────────────────────────

def get_outcomes_summary() -> str:
    text = read_file(VAULT / "_memory" / "OUTCOMES.md")
    entries = re.findall(r"## \d{4}-\d{2}-\d{2}.*?(?=\n## |\Z)", text, re.DOTALL)
    summary = []
    for e in entries:
        outcome_match = re.search(r"\*\*Outcome.*?\*\*:\s*(.+)", e)
        title_match = re.search(r"## \d{4}-\d{2}-\d{2} — (.+)", e)
        if title_match and outcome_match:
            summary.append(f"{title_match.group(1)}: {outcome_match.group(1)}")
    return "\n".join(summary) if summary else "ยังไม่มี outcomes"


# ── LLM: Weakness synthesis ───────────────────────────────────────────────────

def synthesize_weaknesses(audit_data: dict) -> str:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = f"""คุณเป็น system analyst ที่ตรวจสอบ personal knowledge + trading OS ชื่อ ltd-os

ข้อมูล audit สัปดาห์นี้:

## Vault Health Issues
{chr(10).join(audit_data["inbox"]) or "ไม่มีปัญหา"}

## Note Size Issues
{chr(10).join(audit_data["note_sizes"]) or "ไม่มีปัญหา"}

## Daily Note Gaps
{chr(10).join(audit_data["daily_gaps"]) or "ไม่มีปัญหา"}

## Nick KB Gaps (HIGH priority ยังไม่ได้ทำ)
{chr(10).join(audit_data["kb_gaps"]) or "ไม่มี"}

## NAV Log Issues
{chr(10).join(audit_data["nav"]) or "ไม่มีปัญหา"}

## Git Uncommitted
{chr(10).join(audit_data["git_status"]) or "สะอาด"}

## Open Questions จาก Weekly Review ที่แล้ว
{chr(10).join(audit_data["open_questions"]) or "ไม่มี"}

## Git Log 14 วันที่ผ่านมา (pattern analysis)
{audit_data["git_log"][:2000]}

## Outcomes ที่บันทึกไว้
{audit_data["outcomes"]}

---

วิเคราะห์และตอบใน format นี้เท่านั้น (ภาษาไทย):

## จุดอ่อนที่พบ
(3-5 จุด เรียงตาม severity สูงไปต่ำ — ระบุ pattern ไม่ใช่แค่ list อาการ)

## สาเหตุที่แท้จริง
(ทำไมจุดอ่อนพวกนี้ถึงเกิด — systemic หรือ one-off?)

## Proposed Fixes (ต้อง approve ก่อน execute)
(format: [ ] Priority: HIGH/MED/LOW — คำอธิบายสั้น — ไฟล์หรือ action ที่เกี่ยวข้อง)

## สิ่งที่ทำงานได้ดี (อย่าเปลี่ยน)
(2-3 ข้อ)

ห้ามเกิน 400 คำ"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


# ── Build report ──────────────────────────────────────────────────────────────

def build_report(audit_data: dict, analysis: str) -> str:
    total_issues = sum(
        len(v) for k, v in audit_data.items()
        if isinstance(v, list) and v
    )
    status = "🔴 ต้องแก้ไข" if total_issues >= 5 else "🟡 มีจุดบกพร่องเล็กน้อย" if total_issues >= 2 else "🟢 สุขภาพดี"

    lines = [
        f"---",
        f"week: {YEAR}-W{WEEK:02d}",
        f"date: {TODAY}",
        f"status: {status}",
        f"issues_found: {total_issues}",
        f"---",
        f"",
        f"# Weekly System Audit — {YEAR}-W{WEEK:02d}",
        f"",
        f"**{status}** — ตรวจพบ {total_issues} จุดที่ควรดูแล",
        f"",
        f"---",
        f"",
        f"## Vault Health",
        f"",
        f"### Inbox ค้าง",
    ]
    lines += audit_data["inbox"] or ["  - ✅ ไม่มีไฟล์ค้าง"]
    lines += ["", "### Notes ขนาดใหญ่"]
    lines += audit_data["note_sizes"] or ["  - ✅ ทุก note อยู่ในขนาดที่กำหนด"]
    lines += ["", "### Daily Notes ที่ขาดหาย"]
    lines += audit_data["daily_gaps"] or ["  - ✅ ครบทุกวัน"]

    lines += ["", "---", "", "## Nick System"]
    lines += ["", "### KB Gaps HIGH ที่ยังไม่ได้ทำ"]
    lines += audit_data["kb_gaps"] or ["  - ✅ ไม่มี HIGH gaps ค้าง"]
    lines += ["", "### NAV Log"]
    lines += audit_data["nav"] or ["  - ✅ อัปเดตล่าสุด"]
    lines += ["", "### Git Uncommitted"]
    lines += audit_data["git_status"] or ["  - ✅ สะอาด"]

    lines += ["", "---", "", "## Open Questions จากสัปดาห์ที่แล้ว"]
    if audit_data["open_questions"]:
        for q in audit_data["open_questions"]:
            lines.append(f"  - {q}")
    else:
        lines.append("  - ไม่มี open questions")

    lines += ["", "---", "", "## การวิเคราะห์จุดอ่อน (AI Synthesis)", ""]
    lines.append(analysis)

    lines += ["", "---", f"*Generated: {TODAY} | Script: scripts/weekly-audit.py*"]
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Weekly Audit — {YEAR}-W{WEEK:02d}")

    audit_data = {
        "inbox": check_inbox(),
        "note_sizes": check_note_sizes(),
        "daily_gaps": check_daily_gaps(),
        "kb_gaps": check_nick_kb_gaps(),
        "nav": check_nav_freshness(),
        "git_status": check_git_status(),
        "open_questions": get_open_questions(),
        "git_log": get_git_log(),
        "outcomes": get_outcomes_summary(),
    }

    print("Running LLM weakness synthesis...")
    analysis = synthesize_weaknesses(audit_data)

    report = build_report(audit_data, analysis)
    AUDIT_FILE.write_text(report, encoding="utf-8")
    print(f"Saved: {AUDIT_FILE}")


if __name__ == "__main__":
    main()
