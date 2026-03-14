#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""update_timetable_md.py

Generate/overwrite js-school-study/Timetable.md with today's timetable.

Data source:
- /home/ubuntu/.openclaw/workspace/timetable (schedule.py)

This script is safe to run repeatedly.
"""

from __future__ import annotations

import os
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "Timetable.md"

# Where the `timetable` project lives.
# - In GitHub Actions: set TIMETABLE_DIR=./_timetable (or similar)
# - Locally (OpenClaw workspace): default to /home/ubuntu/.openclaw/workspace/timetable
# - Fallback: a sibling `timetable/` next to this repo
TIMETABLE_DIR = Path(
    (Path(__file__).resolve().parents[2] / "timetable")
    if (Path(__file__).resolve().parents[2] / "timetable").exists()
    else "/home/ubuntu/.openclaw/workspace/timetable"
)
TIMETABLE_DIR = Path(os.environ.get("TIMETABLE_DIR", str(TIMETABLE_DIR)))
SCHEDULE_PY = TIMETABLE_DIR / "schedule.py"

TZ = ZoneInfo("Asia/Shanghai")

# NOTE: Avoid HTML comments markers: some mobile renderers show them literally.
# We always overwrite the whole file, so markers are unnecessary.


def run_query(q: str) -> str:
    p = subprocess.run(
        ["python3", str(SCHEDULE_PY), q],
        cwd=str(TIMETABLE_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip() or f"schedule.py exited {p.returncode}")
    return p.stdout.strip()


def run_today() -> str:
    return run_query("today")


def parse_courses(out: str) -> tuple[str, list[tuple[str, str, str]]]:
    """解析 schedule.py 输出，返回 (header, [(时间, 课程, 地点), ...])"""
    raw_lines = out.splitlines()
    header = raw_lines[0] if raw_lines else ""
    courses: list[tuple[str, str, str]] = []
    for line in raw_lines[1:]:
        line = line.strip().lstrip("- ").strip()
        if "｜" in line:
            parts = [p.strip() for p in line.split("｜")]
            time = parts[0] if len(parts) > 0 else ""
            name = parts[1] if len(parts) > 1 else ""
            place = parts[2] if len(parts) > 2 else ""
            courses.append((time, name, place))
    return header, courses


WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def fmt_day(d: date) -> str:
    return d.isoformat()


TIME_RE = re.compile(r"(\d{2}:\d{2})")


def short_time(t: str) -> str:
    m = TIME_RE.search(t)
    return m.group(1) if m else t.strip()


def shorten_name(name: str, limit: int = 8) -> str:
    name = name.strip()
    return name if len(name) <= limit else name[:limit] + "…"


def generate_week_lines(monday: date) -> list[str]:
    """Generate week details WITHOUT any expand/collapse.

    Best practice for mobile text:
    - One day per bullet
    - Each class on its own line (indented)
    - Avoid overly long single lines
    """

    lines: list[str] = []
    for i in range(7):
        d = monday + timedelta(days=i)
        _h, courses = parse_courses(run_query(fmt_day(d)))

        day_label = f"{WEEKDAY_CN[d.weekday()]} {d.strftime('%m-%d')}"
        if not courses:
            lines.append(f"- {day_label}：无课")
            continue

        lines.append(f"- {day_label}：{len(courses)}节")
        for t, n, p in courses:
            p_part = f"｜{p}" if p else ""
            lines.append(f"  - {t}｜{n}{p_part}")

    lines.append("")
    return lines


def generate_block() -> str:
    now = datetime.now(TZ)
    now_str = now.strftime("%Y-%m-%d %H:%M")

    # Today
    out_today = run_today()
    header_today, courses_today = parse_courses(out_today)

    lines: list[str] = []
    lines.append(f"更新时间：**{now_str}**（北京时间）")
    lines.append("")

    lines.append(f"## 今日课表（{header_today}）")
    lines.append("")

    # Highlight block (quote) for mobile
    if not courses_today:
        lines.append("> 今日：**无课**")
    else:
        first_time, first_name, first_place = courses_today[0]
        fp = f"（{first_place}）" if first_place else ""
        lines.append(f"> 今日：**{len(courses_today)} 节课**")
        lines.append(f"> 第一节：{short_time(first_time)} {first_name}{fp}")
    lines.append("")

    # Details
    if not courses_today:
        lines.append("- 无课")
    else:
        for time, name, place in courses_today:
            place_part = f"｜{place}" if place else ""
            lines.append(f"- {time}｜{name}{place_part}")
    lines.append("")

    # This week (Mon-Sun) based on Beijing time
    today = now.date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    lines.append(f"## 本周课表（{monday.isoformat()} ~ {sunday.isoformat()}）")
    lines.append("")

    # Highlight block for week overview
    # Summarize days that have classes
    week_summary = []
    for i in range(7):
        d = monday + timedelta(days=i)
        _h, cs = parse_courses(run_query(fmt_day(d)))
        if cs:
            week_summary.append(f"{WEEKDAY_CN[d.weekday()]}{d.strftime('%m-%d')}({len(cs)})")
    if week_summary:
        lines.append("> 有课：" + "、".join(week_summary))
    else:
        lines.append("> 本周：**全周无课**")
    lines.append("")

    lines.extend(generate_week_lines(monday))

    return "\n".join(lines).rstrip() + "\n"


def update_file() -> None:
    block = generate_block()

    # Always write the full file (no hidden markers).
    replaced = (
        "# 课程表\n\n"
        "> 自动更新，请勿手工编辑\n\n"
        "## 周课表（每周更新）\n\n"
        "![week-grid](assets/week-grid.svg)\n\n"
        "---\n\n"
        "## 今日/本周（文字版，每天更新）\n\n"
        + block
        + "\n"
    )

    OUT.write_text(replaced, encoding="utf-8")


def main() -> int:
    update_file()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
