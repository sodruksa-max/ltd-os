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


def generate_recommendations(stats: dict) -> list[str]:
    """สร้าง proactive recommendations จาก context จริงใน vault"""
    recs = []

    # --- Rule 1: thesis ที่ยังไม่มี research doc ---
    tracker = REPO / "vault/Knowledge/THESIS_TRACKER.md"
    if tracker.exists():
        content = tracker.read_text(encoding="utf-8", errors="replace")
        thesis_blocks = re.findall(
            r"### (T\d+ — [^\n]+)\n\*\*Tickers:\*\* ([^\n]+)", content
        )
        for thesis_name, tickers_raw in thesis_blocks:
            tickers = [t.strip() for t in tickers_raw.split(",")]
            # ตรวจว่ามี research doc ใน vault/20_investment/ หรือ vault/10_research/
            has_doc = any(
                list(REPO.glob(f"vault/20_investment/{t}-*.md")) +
                list(REPO.glob(f"vault/10_research/*{t.lower()}*.md"))
                for t in tickers
            )
            if not has_doc:
                pick = tickers[0]
                recs.append(
                    f"**{thesis_name}** ยังไม่มี research doc เลย → "
                    f"`/stock-content {pick}` เพื่อเริ่มสร้าง KB"
                )

    # --- Rule 2: nick kill condition alert ยังไม่ได้ตามผล ---
    alerts_dir = REPO / "vault/20_investment/nick/alerts"
    if alerts_dir.exists():
        recent = sorted(alerts_dir.glob("*-alert.md"),
                        key=lambda f: f.stat().st_mtime, reverse=True)
        if recent:
            alert_date = datetime.fromtimestamp(recent[0].stat().st_mtime).date()
            nick_last = stats.get("/nick-weekly", {}).get("last")
            if nick_last is None or nick_last < alert_date:
                tickers_in_alert = re.findall(r"\*\*([A-Z]+)\*\*", recent[0].read_text(encoding="utf-8", errors="replace"))
                tickers_str = ", ".join(tickers_in_alert[:3]) if tickers_in_alert else "holdings"
                recs.append(
                    f"**Kill condition alert** ({tickers_str}) ยังไม่ได้รีวิว → "
                    f"`/nick-weekly` เพื่อตรวจสถานะ positions"
                )

    # --- Rule 3: มี research notes แต่ไม่เคยรัน /challenge ---
    research_files = list(REPO.glob("vault/20_investment/*.md"))
    challenge_ever = stats.get("/challenge", {}).get("last") is not None
    # ตรวจจาก git log pattern แยก (challenge ไม่มีใน COMMIT_PATTERNS)
    if not challenge_ever:
        result = subprocess.run(
            ["git", "log", "--since=60 days ago", "--pretty=format:%s", "--grep=challenge"],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        challenge_ever = bool(result.stdout.strip())
    if research_files and not challenge_ever:
        newest = max(research_files, key=lambda f: f.stat().st_mtime)
        recs.append(
            f"**มี {len(research_files)} research notes** แต่ยังไม่เคย stress-test → "
            f"`/challenge {newest.relative_to(REPO)}` ก่อนตัดสินใจลงทุน"
        )

    # --- Rule 4: มี content platforms แต่ยังไม่เคยสร้าง content ---
    research_ideas = stats.get("/research-idea", {}).get("last")
    content_files = list(REPO.glob("vault/30_content/drafts/*.md"))
    if research_ideas is None and not content_files:
        # ดูว่ามี thesis ที่ชัดพอจะทำ content
        recs.append(
            "**ยังไม่เคยสร้าง content** จาก thesis ที่มี → "
            "`/research-idea 'AI capex supercycle' --output: yt` "
            "เพื่อ test pipeline Minnie→Reese→Rae ครั้งแรก"
        )

    # --- Rule 5: thesis tickers ไม่อยู่ใน watchlist ---
    watchlist_path = REPO / "config/watchlist.txt"
    if tracker.exists() and watchlist_path.exists():
        watchlist = set(
            l.strip() for l in watchlist_path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")
        )
        all_thesis_tickers = set(re.findall(r"\b([A-Z]{2,5})\b", content))
        missing = all_thesis_tickers - watchlist - {"AND", "OR", "NOT", "THE", "FOR", "IPO", "SEC",
                                                     "ROI", "FCF", "TTM", "EPS", "ARR", "NRR", "YOY",
                                                     "ETF", "OTC", "DOGE", "NASA", "NATO", "USDA",
                                                     "MOC", "TAM", "SBC", "CTA", "KPI", "API",
                                                     "AI", "ML", "US", "UK", "EU", "FY", "QQ"}
        # กรองเฉพาะ ticker ที่ดูเหมือนจริง (2-5 ตัวอักษร, อยู่ใน THESIS_TRACKER tickers section)
        thesis_tickers_only = set()
        for _, tickers_raw in thesis_blocks if 'thesis_blocks' in dir() else []:
            for t in tickers_raw.split(","):
                thesis_tickers_only.add(t.strip())
        real_missing = thesis_tickers_only - watchlist
        if real_missing:
            sample = sorted(real_missing)[:5]
            recs.append(
                f"**{len(real_missing)} thesis tickers ไม่อยู่ใน watchlist** → "
                f"screener จะไม่จับ: {', '.join(sample)}"
                + (f" และอีก {len(real_missing)-5} ตัว" if len(real_missing) > 5 else "")
            )

    # --- Rule 6: /council ยังไม่เคยใช้ แต่มีหลาย thesis ---
    council_result = subprocess.run(
        ["git", "log", "--since=60 days ago", "--pretty=format:%s", "--grep=council"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    council_used = bool(council_result.stdout.strip())
    num_theses = len(thesis_blocks) if 'thesis_blocks' in dir() else 0
    if not council_used and num_theses >= 3:
        recs.append(
            f"**มี {num_theses} active theses แต่ยังไม่เคยใช้ `/council`** → "
            "เหมาะสำหรับ high-stakes decisions เช่น เลือก thesis ไหนลงทุนก่อน หรือ sizing strategy"
        )

    # --- Rule 7: paper-survey ไม่เคยใช้ แต่มี thesis ที่ academic backing จะช่วยได้ ---
    paper_last = stats.get("/paper-survey", {}).get("last")
    if paper_last is None and num_theses > 0:
        recs.append(
            "**ยังไม่เคยใช้ `/paper-survey`** → "
            "หา academic papers มาเสริม thesis เช่น "
            "`/paper-survey momentum trading AI stocks` "
            "ช่วยให้ kill conditions มีหลักฐานรองรับมากขึ้น"
        )

    # คืนแค่ top 4 (priority: kill alert > research gap > thesis gap > discovery)
    return recs[:4]


def write_log(stats: dict, recs: list[str]) -> None:
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
        "## Proactive Recommendations",
        "",
    ]

    if recs:
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {rec}")
    else:
        lines.append("_ไม่มี recommendation วันนี้ — workflow ครอบคลุมดีแล้ว ✅_")

    lines += [
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

    lines += ["", "## Gaps", ""]
    if gaps:
        for label, cmd, last, days_ago, count_30, freq, warn in gaps:
            if last is None:
                lines.append(f"- **{cmd}** — ยังไม่เคยใช้")
            else:
                lines.append(
                    f"- **{cmd}** — ไม่ได้ใช้ {days_ago} วัน "
                    f"(ควรทุก {freq} วัน)"
                )
    else:
        lines.append("_ไม่มี gap ✅_")

    lines += ["", "---", f"*Lookback: {LOOKBACK_DAYS} วัน | Generated: {TODAY}*"]

    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Usage log: {LOG_OUT}")
    print(f"Recommendations: {len(recs)} | Gaps: {len(gaps)}")


def main():
    print(f"Reading git log ({LOOKBACK_DAYS}d)...")
    commits = git_log(LOOKBACK_DAYS)
    print(f"  {len(commits)} commits found")
    stats = build_stats(commits)
    recs = generate_recommendations(stats)
    write_log(stats, recs)


if __name__ == "__main__":
    main()
