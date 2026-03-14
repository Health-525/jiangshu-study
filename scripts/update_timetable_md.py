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

START = "<!-- AUTO-GENERATED:START -->"
END = "<!-- AUTO-GENERATED:END -->"


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


def generate_week_table(monday: date) -> list[str]:
    """Generate a single table for Mon-Sun.

    Columns: 周/日期 | 课程（按时间顺序换行） | 地点（对应换行）
    """

    rows: list[tuple[str, str, str]] = []
    for i in range(7):
        d = monday + timedelta(days=i)
        out = run_query(fmt_day(d))
        _header, courses = parse_courses(out)

        day_label = f"{WEEKDAY_CN[d.weekday()]} {d.strftime('%m-%d')}"
        if not courses:
            rows.append((day_label, "无课", "—"))
            continue

        # Multiline cells: use <br> for GitHub/Markdown mobile readability
        course_lines = []
        place_lines = []
        for time, name, place in courses:
            course_lines.append(f"{time} {name}".strip())
            place_lines.append(place or "")

        rows.append((day_label, "<br>".join(course_lines), "<br>".join(place_lines) or "—"))

    lines: list[str] = []
    lines.append("| 日期 | 课程 | 地点 |")
    lines.append("|------|------|------|")
    for day_label, ccell, pcell in rows:
        lines.append(f"| {day_label} | {ccell} | {pcell} |")
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
    if not courses_today:
        lines.append("- 无课")
    else:
        lines.append("| 时间 | 课程 | 地点 |")
        lines.append("|------|------|------|")
        for time, name, place in courses_today:
            lines.append(f"| {time} | {name} | {place} |")
    lines.append("")

    # This week (Mon-Sun) based on Beijing time
    today = now.date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    lines.append(f"## 本周课表（{monday.isoformat()} ~ {sunday.isoformat()}）")
    lines.append("")
    lines.extend(generate_week_table(monday))

    return "\n".join(lines).rstrip() + "\n"


def update_file() -> None:
    block = generate_block()

    # Always write the full file to avoid stale manual lines.
    replaced = (
        "# 课程表\n\n"
        "> 自动更新，请勿手工编辑\n\n"
        + START
        + "\n\n"
        + block
        + "\n"
        + END
        + "\n"
    )

    OUT.write_text(replaced, encoding="utf-8")


def main() -> int:
    update_file()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
