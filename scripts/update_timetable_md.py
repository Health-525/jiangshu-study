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
from datetime import datetime
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


def run_today() -> str:
    p = subprocess.run(
        ["python3", str(SCHEDULE_PY), "today"],
        cwd=str(TIMETABLE_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip() or f"schedule.py exited {p.returncode}")
    return p.stdout.strip()


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


def generate_block() -> str:
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    out = run_today()
    header, courses = parse_courses(out)

    lines: list[str] = []
    lines.append(f"更新时间：**{now}**（北京时间）")
    lines.append("")
    lines.append(f"## 今日课表（{header}）")
    lines.append("")

    if not courses:
        lines.append("**今天没有课 🎉**")
    else:
        lines.append("| 时间 | 课程 | 地点 |")
        lines.append("|------|------|------|")
        for time, name, place in courses:
            lines.append(f"| {time} | {name} | {place} |")

    lines.append("")

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
