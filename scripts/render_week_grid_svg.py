#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""render_week_grid_svg.py

Render a weekly grid timetable as SVG (Mon-Sun columns, periods rows).
Output: assets/week-grid.svg

Data source: timetable repo (schedule.json + schedule.py)
Environment:
- TIMETABLE_DIR: path to timetable repo
- OUTPUT: output svg path (default: assets/week-grid.svg)

We parse timetable/data/schedule.json directly to reliably build the grid.
"""

from __future__ import annotations

import json
import os
import html
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "assets"
DEFAULT_OUT = ASSETS_DIR / "week-grid.svg"

_guess = (Path(__file__).resolve().parents[2] / "timetable")
TIMETABLE_DIR = Path(_guess if _guess.exists() else "/home/ubuntu/.openclaw/workspace/timetable")
TIMETABLE_DIR = Path(os.environ.get("TIMETABLE_DIR", str(TIMETABLE_DIR)))
SCHEDULE_JSON = TIMETABLE_DIR / "data" / "schedule.json"


@dataclass
class Course:
    title: str
    weekday: int  # 1=Mon
    periods: list[int]
    location: str
    weeks: str


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def parse_week_spec(spec: str) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out


def get_week_index(d: date, week1_monday: date) -> int:
    return (d - week1_monday).days // 7 + 1


def load_schedule() -> dict:
    return json.loads(SCHEDULE_JSON.read_text(encoding="utf-8"))


def main() -> int:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(os.environ.get("OUTPUT", str(DEFAULT_OUT)))

    data = load_schedule()
    meta = data.get("meta", {})
    week1_monday = date.fromisoformat(meta.get("week1_monday"))

    now = datetime.now(TZ)
    today = now.date()
    monday = today - timedelta(days=today.weekday())
    week_idx = get_week_index(monday, week1_monday)

    period_times: dict[str, str] = data.get("periodTimes", {})
    courses_raw = data.get("courses", [])

    courses: list[Course] = []
    for c in courses_raw:
        courses.append(
            Course(
                title=c.get("title", ""),
                weekday=int(c.get("weekday")),
                periods=[int(x) for x in c.get("periods", [])],
                location=c.get("location", ""),
                weeks=c.get("weeks", ""),
            )
        )

    # Build events for this teaching week
    events = []  # (weekday 1-7, p_start, p_end, label)
    for c in courses:
        if week_idx not in parse_week_spec(c.weeks):
            continue
        if not c.periods:
            continue
        ps, pe = min(c.periods), max(c.periods)
        label = f"{c.title}\n{c.location}".strip()
        events.append((c.weekday, ps, pe, label))

    # SVG layout
    W, H = 1200, 1600
    pad = 40
    header_h = 120
    left_w = 180
    grid_w = W - pad * 2 - left_w
    grid_h = H - pad * 2 - header_h

    col_w = grid_w / 7
    row_h = grid_h / 10

    bg = "#0b1220"
    card = "#101a2f"
    grid = "#23304f"
    text = "#e5e7eb"
    mut = "#93a4c7"
    block = "#2563eb"

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{bg}"/>')
    parts.append(f'<rect x="{pad}" y="{pad}" width="{W-2*pad}" height="{H-2*pad}" rx="28" fill="{card}" stroke="#1f2a44"/>')

    title = f"周课表｜第{week_idx}周（{monday.isoformat()}~{(monday+timedelta(days=6)).isoformat()}）"
    parts.append(f'<text x="{pad+28}" y="{pad+58}" fill="{text}" font-size="34" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">{esc(title)}</text>')
    parts.append(f'<text x="{pad+28}" y="{pad+92}" fill="{mut}" font-size="20" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">更新 {now.strftime("%Y-%m-%d %H:%M")}（北京）</text>')

    gx = pad + 28 + left_w
    gy = pad + header_h

    # Column headers
    for i in range(7):
        d = monday + timedelta(days=i)
        label = f"{['一','二','三','四','五','六','日'][i]}\n{d.strftime('%m-%d')}"
        x = gx + i * col_w
        parts.append(f'<text x="{x + col_w/2}" y="{gy-50}" fill="{text}" font-size="20" font-weight="700" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">周{esc(label.splitlines()[0])}</text>')
        parts.append(f'<text x="{x + col_w/2}" y="{gy-26}" fill="{mut}" font-size="16" font-weight="400" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">{esc(label.splitlines()[1])}</text>')

    # Rows (period labels)
    for p in range(1, 11):
        y = gy + (p - 1) * row_h
        parts.append(f'<line x1="{gx}" y1="{y}" x2="{gx+grid_w}" y2="{y}" stroke="{grid}"/>')
        t = period_times.get(str(p), "")
        parts.append(f'<text x="{pad+56}" y="{y + row_h/2 - 6}" fill="{text}" font-size="18" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">第{p}节</text>')
        parts.append(f'<text x="{pad+56}" y="{y + row_h/2 + 18}" fill="{mut}" font-size="14" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">{esc(t)}</text>')

    # Vertical lines
    for i in range(8):
        x = gx + i * col_w
        parts.append(f'<line x1="{x}" y1="{gy}" x2="{x}" y2="{gy+grid_h}" stroke="{grid}"/>')

    # Blocks
    for wd, ps, pe, label in events:
        col = wd - 1
        x = gx + col * col_w + 8
        y = gy + (ps - 1) * row_h + 8
        h = (pe - ps + 1) * row_h - 16
        w = col_w - 16
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{block}" opacity="0.95"/>')

        # Text (wrap with <tspan>), try to fit inside block.
        title_full = label.split("\n", 1)[0].strip()
        loc_full = (label.split("\n", 1)[1].strip() if "\n" in label else "")

        def wrap(s: str, max_chars: int) -> list[str]:
            s = s.strip()
            if not s:
                return []
            out = []
            cur = ""
            for ch in s:
                cur += ch
                if len(cur) >= max_chars:
                    out.append(cur)
                    cur = ""
            if cur:
                out.append(cur)
            return out[:3]

        title_lines = wrap(title_full, 9)
        loc_lines = wrap(loc_full, 12)

        tx = x + 14
        ty = y + 30
        parts.append(
            f'<text x="{tx}" y="{ty}" fill="#ffffff" font-size="18" font-weight="800" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">'
            + "".join([f'<tspan x="{tx}" dy="{0 if i==0 else 22}">{esc(line)}</tspan>' for i, line in enumerate(title_lines)])
            + "</text>"
        )

        if loc_lines:
            lty = ty + 22 * max(1, len(title_lines)) + 6
            parts.append(
                f'<text x="{tx}" y="{lty}" fill="#dbeafe" font-size="14" font-weight="600" '
                f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial">'
                + "".join([f'<tspan x="{tx}" dy="{0 if i==0 else 18}">{esc(line)}</tspan>' for i, line in enumerate(loc_lines)])
                + "</text>"
            )

    parts.append("</svg>")
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
