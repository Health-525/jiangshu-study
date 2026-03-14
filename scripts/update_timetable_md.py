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


def generate_block() -> str:
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    out = run_today()

    lines: list[str] = []
    lines.append(f"更新时间：**{now}**（北京时间）")
    lines.append("")

    # Put the raw output into a collapsible section for mobile readability.
    lines.append("## 今日课表")
    lines.append("")

    # Quick hint line for mobile scanning.
    if "今天没有课" in out:
        lines.append("- 结论：**今天没有课**")
        lines.append("")

    lines.append("<details>")
    lines.append("<summary>展开查看原始明细</summary>")
    lines.append("")
    lines.append("```text")
    lines.append(out)
    lines.append("```")
    lines.append("</details>")
    lines.append("")

    lines.append("---")
    lines.append("快捷查询：在飞书对我说 `今天课表` / `明天课表` / `课表 2026-03-20` / `今天下午课表`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_file() -> None:
    block = generate_block()

    # Always write the full file to avoid stale manual lines.
    replaced = (
        "# Timetable（自动更新）\n\n"
        "> 说明：该文件由脚本自动生成/覆盖。请勿手工编辑。\n\n"
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
