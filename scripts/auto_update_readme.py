#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
TZ = ZoneInfo("Asia/Shanghai")

START = "<!-- AUTO-GENERATED:START -->"
END = "<!-- AUTO-GENERATED:END -->"

COURSE_DIR_RE = re.compile(r"^\\d{2}-")

@dataclass
class CourseInfo:
    name: str
    path: Path
    file_count: int
    subdirs: list[str]


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd), text=True).strip()


def list_courses() -> list[CourseInfo]:
    courses: list[CourseInfo] = []
    for p in sorted([x for x in REPO_ROOT.iterdir() if x.is_dir()]):
        if not COURSE_DIR_RE.match(p.name):
            continue
        # count tracked + untracked files excluding .gitkeep? keep simple: count all files
        file_count = sum(1 for _ in p.rglob('*') if _.is_file())
        subdirs = sorted({x.name for x in p.iterdir() if x.is_dir()})
        courses.append(CourseInfo(name=p.name, path=p, file_count=file_count, subdirs=subdirs))
    return courses


def latest_files(limit: int = 15) -> list[tuple[str, str]]:
    """Return list of (path, mtime_str) for most recently modified files under repo (excluding .git)."""
    files: list[Path] = []
    for p in REPO_ROOT.rglob('*'):
        if not p.is_file():
            continue
        if '.git' in p.parts:
            continue
        # skip README itself and auto-generated script to avoid noise
        files.append(p)

    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    out: list[tuple[str, str]] = []
    for p in files[:limit]:
        dt = datetime.fromtimestamp(p.stat().st_mtime, TZ)
        out.append((str(p.relative_to(REPO_ROOT)), dt.strftime('%Y-%m-%d %H:%M')))
    return out


def generate_block() -> str:
    now = datetime.now(TZ).strftime('%Y-%m-%d %H:%M')
    courses = list_courses()
    latest = latest_files()

    lines: list[str] = []
    lines.append("## 自动索引（每 12 小时更新）")
    lines.append(f"- Last updated (Beijing Time): **{now}**")
    lines.append("")

    lines.append("### 课程目录概览")
    for c in courses:
        subs = ("、".join([f"`{s}/`" for s in c.subdirs]) if c.subdirs else "（暂无子目录）")
        lines.append(f"- `{c.name}/`：{c.file_count} files；子目录：{subs}")

    lines.append("")
    lines.append("### 最近更新（按文件修改时间）")
    for path, t in latest:
        lines.append(f"- {t} — `{path}`")

    lines.append("")
    lines.append("（说明：该段由脚本生成；如需固定结构/排除某些目录，告诉我我来调规则。）")

    return "\n".join(lines).rstrip() + "\n"


def update_readme() -> None:
    content = README.read_text(encoding='utf-8')
    block = generate_block()

    if START in content and END in content:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        replaced = pattern.sub(START + "\n\n" + block + "\n" + END, content)
    else:
        replaced = content.rstrip() + "\n\n" + START + "\n\n" + block + "\n" + END + "\n"

    if replaced != content:
        README.write_text(replaced, encoding='utf-8')


def main():
    update_readme()


if __name__ == '__main__':
    main()
