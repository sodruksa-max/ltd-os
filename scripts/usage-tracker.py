"""
usage-tracker.py — อ่าน git log → classify command usage → เขียน vault/_memory/USAGE_LOG.md
รันอัตโนมัติจาก daily-brief.sh ก่อน Claude ทำ brief
"""

import subprocess
import re
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG_OUT = REPO / "vault/_memory/USAGE_LOG.md"

TODAY = date.today()
LOOKBACK_DAYS = 60  # ดู git log ย้อนหลัง 60 วัน


# pattern → (command_name, expected_frequency_days, gap_warn_days)
COMMIT_PATTERNS = [
    (r"notes: daily brief",          "/daily-brief",         1,  2),
    (r"notes: pre-market",           "/pre-market",          1,  4),
    (r"notes: post-market",          "/post-market",         1,  4),
    (r"notes: market-log",           "/market-log",          1,  4),
    (r"notes: weekly-market",        "/weekly-market",       7,  10),
    (r"memory: weekly-calibration",  "/weekly-calibration",  14, 18),
    (r"notes: weekly-learnings",     "/weekly-learnings",    7,  10),
    (r"vault: stock-content",        "/stock-content",       14, 21),
    (r"vault: stock-research",       "/stock-research",      14, 21),
    (r"vault: research-idea",        "/research-idea",       14, 21),
    (r"notes: paper-survey",         "/paper-survey",        30, 45),
    (r"notes: import-notebooklm",    "/import-notebooklm",  30, 45),
    (r"nick.*weekly",                "/nick-weekly",         7,  10),
]

# ตรวจจากไฟล์ใน vault (fallback ถ้า commit message ไม่ตรง pattern)
FILE_PATTERNS = [
    ("vault/20_investment/_journal/*-premarket.md",  "/pre-market",   1,  4),
    ("vault/20_investment/_journal/*-review.md",     "/post-market",  1,  4),
    ("vault/20_investment/nick/weekly/*_weekly-rec.md", "/nick-weekly", 7, 10),
    ("vault/20_investment/_journal/*-weekly-market.md", "/weekly-market", 7, 10),
]


def git_log(days: int) -> list[dict]:
    """คืน list ของ commits ใน N วันย้อนหลัง"""
    since = (TODAY - timedelta(days=days)).isoformat()
    result = subprocess.run(
        ["git", "log", f"--since={since}", "--pretty=format:%H|%ad|%s", "--date=short"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        if "|" not in line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "date": parts[1], "msg": parts[2]})
    return commits


def latest_file_date(pattern: str) -> date | None:
    """หา modification date ของไฟล์ล่าสุดที่ match pattern"""
    files = sorted(REPO.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        return None
    mtime = files[0].stat().st_mtime
    return datetime.fromtimestamp(mtime).date()


def count_in_window(commits: list[dict], pattern: str, days: int) -> int:
    cutoff = TODAY - timedelta(days=days)
    rx = re.compile(pattern, re.IGNORECASE)
    return sum(
        1 for c in commits
        if rx.search(c["msg"]) and date.fromisoformat(c["date"]) >= cutoff
    )


def build_stats(commits: list[dict]) -> dict:
    stats = {}

    # จาก commit messages
    for pattern, cmd, freq, warn in COMMIT_PATTERNS:
        rx = re.compile(pattern, re.IGNORECASE)
        matches = [c for c in commits if rx.search(c["msg"])]
        last_date = date.fromisoformat(matches[0]["date"]) if matches else None
        count_30 = count_in_window(commits, pattern, 30)
        stats[cmd] = {
            "last": last_date,
            "count_30": count_30,
            "freq": freq,
            "warn": warn,
            "source": "git",
        }

    # fallback จากไฟล์ (ถ้า git ไม่เจอ หรือ file date ใหม่กว่า)
    for pattern, cmd, freq, warn in FILE_PATTERNS:
        file_date = latest_file_date(pattern)
        if file_date and (stats.get(cmd, {}).get("last") or date.min) < file_date:
            existing = stats.get(cmd, {"count_30": 0, "freq": freq, "warn": warn})
            existing["last"] = file_date
            existing["source"] = "file"
            stats[cmd] = existing

    return stats


def gap_label(last: date | None, warn_days: int) -> str:
    if last is None:
        return "❓ never"
    days_ago = (TODAY - last).days
    if days_ago > warn_days:
        return f"⚠️ {days_ago}d"
    return "✅"


def write_log(stats: dict) -> None:
    # เรียงตาม priority: ⚠️ ก่อน
    rows = []
    for cmd, s in sorted(stats.items()):
        last = s["last"]
        days_ago = (TODAY - last).days if last else None
        label = gap_label(last, s["warn"])
        rows.append((label, cmd, last, days_ago, s["count_30"], s["freq"], s["warn"]))

    rows.sort(key=lambda r: (0 if "⚠️" in r[0] else (1 if "❓" in r[0] else 2), r[1]))

    gaps = [r for r in rows if "⚠️" in r[0] or "❓" in r[0]]

    lines = [
        "---",
        "type: usage-log",
        f"updated: {TODAY}",
        "source: scripts/usage-tracker.py",
        "---",
        "",
        "# Usage Log",
        f"*Auto-generated {TODAY} — อ่านโดย /daily-brief เพื่อ surface gaps*",
        "",
        "## Command Activity (30 วันล่าสุด)",
        "",
        "| Command | ใช้ล่าสุด | วันที่ผ่านไป | Count 30d | Gap |",
        "|---|---|---|---|---|",
    ]

    for label, cmd, last, days_ago, count_30, freq, warn in rows:
        last_str = last.isoformat() if last else "—"
        days_str = str(days_ago) if days_ago is not None else "—"
        lines.append(f"| {cmd} | {last_str} | {days_str} | {count_30} | {label} |")

    lines += ["", "## Gaps — ต้องการความสนใจ", ""]
    if gaps:
        for label, cmd, last, days_ago, count_30, freq, warn in gaps:
            if last is None:
                lines.append(f"- **{cmd}** — ยังไม่เคยใช้")
            else:
                lines.append(
                    f"- **{cmd}** — ไม่ได้ใช้ {days_ago} วัน "
                    f"(ควรทุก {freq} วัน, warn ที่ {warn} วัน)"
                )
    else:
        lines.append("_ไม่มี gap — ใช้งานครบทุก workflow ✅_")

    lines += ["", "---", f"*Lookback: {LOOKBACK_DAYS} วัน | Generated: {TODAY}*"]

    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Usage log: {LOG_OUT}")
    if gaps:
        print(f"Gaps found: {len(gaps)}")
        for _, cmd, _, days_ago, *_ in gaps:
            print(f"  {cmd}: {days_ago}d ago" if days_ago else f"  {cmd}: never")


def main():
    print(f"Reading git log ({LOOKBACK_DAYS}d)...")
    commits = git_log(LOOKBACK_DAYS)
    print(f"  {len(commits)} commits found")
    stats = build_stats(commits)
    write_log(stats)


if __name__ == "__main__":
    main()
