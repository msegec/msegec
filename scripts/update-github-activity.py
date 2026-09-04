#!/usr/bin/env python3

import argparse
import html
import json
import subprocess
from datetime import date, datetime
from pathlib import Path


QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      restrictedContributionsCount
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""

LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

STYLE = """
  <style>
    :root { color-scheme: light dark; }
    .card { fill: #ffffff; stroke: #d0d7de; }
    .title { fill: #1f2328; font: 700 VAR_TITLEpx -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }
    .subtitle { fill: #59636e; font: 500 VAR_SUBTITLEpx -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }
    .label { fill: #59636e; font: 500 VAR_LABELpx -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }
    rect[data-level="0"] { fill: #eff2f5; }
    rect[data-level="1"] { fill: #aceebb; }
    rect[data-level="2"] { fill: #4ac26b; }
    rect[data-level="3"] { fill: #209c50; }
    rect[data-level="4"] { fill: #116329; }
    @media (prefers-color-scheme: dark) {
      .card { fill: #0d1117; stroke: #30363d; }
      .title { fill: #f0f6fc; }
      .subtitle, .label { fill: #9198a1; }
      rect[data-level="0"] { fill: #151b23; }
      rect[data-level="1"] { fill: #033a16; }
      rect[data-level="2"] { fill: #196c2e; }
      rect[data-level="3"] { fill: #2ea043; }
      rect[data-level="4"] { fill: #56d364; }
    }
  </style>
"""


def load_profile(login: str) -> dict:
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={login}"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    return payload["data"]["user"]


def format_number(value: int) -> str:
    return f"{value:,}"


def format_date(value: date, abbreviated: bool = False) -> str:
    month = value.strftime("%b" if abbreviated else "%B")
    return f"{value.day} {month} {value.year}"


def current_streak(days: list[dict]) -> int:
    streak = 0
    for day in reversed(days):
        if day["contributionCount"] == 0:
            break
        streak += 1
    return streak


def month_labels(weeks: list[dict], x_start: int, pitch: int) -> list[tuple[int, str]]:
    labels = []
    previous = None
    for index, week in enumerate(weeks):
        dates = [
            datetime.strptime(day["date"], "%Y-%m-%d").date()
            for day in week["contributionDays"]
        ]
        candidate = next((value for value in dates if value.day <= 7), None)
        if candidate is None or candidate.month == previous:
            continue
        labels.append((x_start + index * pitch, candidate.strftime("%b")))
        previous = candidate.month
    return labels


def render_svg(profile: dict, mobile: bool) -> str:
    collection = profile["contributionsCollection"]
    calendar = collection["contributionCalendar"]
    weeks = calendar["weeks"]
    days = [day for week in weeks for day in week["contributionDays"]]
    total = calendar["totalContributions"]
    snapshot = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()

    if mobile:
        width, height = 420, 190
        x_start, y_start, pitch, cell = 40, 88, 7, 6
        title_x, title_y, title_size = 20, 30, 21
        subtitle_x, subtitle_y, subtitle_size = 20, 53, 11
        label_size = 9
    else:
        width, height = 920, 250
        x_start, y_start, pitch, cell = 96, 108, 14, 11
        title_x, title_y, title_size = 34, 43, 24
        subtitle_x, subtitle_y, subtitle_size = 34, 69, 13
        label_size = 12

    style = (
        STYLE.replace("VAR_TITLE", str(title_size))
        .replace("VAR_SUBTITLE", str(subtitle_size))
        .replace("VAR_LABEL", str(label_size))
    )
    title = f"{format_number(total)} contributions in the past year"
    description = f"GitHub contribution calendar through {format_date(snapshot)}. Private work is included only as aggregate counts."
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">{html.escape(title)}</title>',
        f'  <desc id="desc">{html.escape(description)}</desc>',
        style,
        f'  <rect class="card" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12"/>',
        f'  <text x="{title_x}" y="{title_y}" class="title">{html.escape(title)}</text>',
    ]

    if mobile:
        output.extend(
            [
                f'  <text x="{subtitle_x}" y="{subtitle_y}" class="subtitle">Private work appears as counts only. Updated {format_date(snapshot, True)}.</text>',
            ]
        )
    else:
        output.extend(
            [
                f'  <text x="{subtitle_x}" y="{subtitle_y}" class="subtitle">Private work is included as counts only. Updated {format_date(snapshot, True)}.</text>',
            ]
        )

    month_y = y_start - 14 if mobile else y_start - 15
    for x, label in month_labels(weeks, x_start, pitch):
        if x > width - (25 if mobile else 35):
            continue
        output.append(f'  <text x="{x}" y="{month_y}" class="label">{label}</text>')

    for label, weekday in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        y = y_start + weekday * pitch + cell
        output.append(
            f'  <text x="{10 if mobile else 34}" y="{y}" class="label">{label}</text>'
        )

    for week_index, week in enumerate(weeks):
        for day in week["contributionDays"]:
            x = x_start + week_index * pitch
            y = y_start + day["weekday"] * pitch
            count = day["contributionCount"]
            noun = "contribution" if count == 1 else "contributions"
            level = LEVELS[day["contributionLevel"]]
            output.append(
                f'  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" data-level="{level}"><title>{day["date"]}: {count} {noun}</title></rect>'
            )

    legend_y = y_start + 7 * pitch + (13 if mobile else 18)
    legend_x = width - (180 if mobile else 254)
    output.append(
        f'  <text x="{legend_x}" y="{legend_y + cell}" class="label">Less</text>'
    )
    for level in range(5):
        x = legend_x + (34 if mobile else 40) + level * (cell + (5 if mobile else 7))
        output.append(
            f'  <rect x="{x}" y="{legend_y}" width="{cell}" height="{cell}" rx="2" data-level="{level}"/>'
        )
    output.append(
        f'  <text x="{legend_x + (102 if mobile else 135)}" y="{legend_y + cell}" class="label">More</text>'
    )
    output.append("</svg>")
    return "\n".join(output) + "\n"


def update_readme(path: Path, profile: dict) -> None:
    collection = profile["contributionsCollection"]
    calendar = collection["contributionCalendar"]
    days = [day for week in calendar["weeks"] for day in week["contributionDays"]]
    total = calendar["totalContributions"]
    active_days = sum(day["contributionCount"] > 0 for day in days)
    restricted = collection["restrictedContributionsCount"]
    commits = collection["totalCommitContributions"]
    pull_requests = collection["totalPullRequestContributions"]
    streak = current_streak(days)
    snapshot = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()
    start = "<!-- activity:start -->"
    end = "<!-- activity:end -->"
    block = f"""{start}
**{format_number(total)} contributions** across **{active_days} active days**, with a **{streak}-day current streak**. **{format_number(restricted)} private contributions** appear only as aggregate counts. Public activity includes **{format_number(commits)} commits** and **{format_number(pull_requests)} pull requests**.

<picture>
  <source media="(max-width: 600px)" srcset="assets/github-activity-mobile.svg">
  <img src="assets/github-activity.svg" alt="GitHub contribution calendar for the 12 months to {format_date(snapshot)}">
</picture>

<sub>Snapshot: {format_date(snapshot)}. Private repository, client, host and deployment details are omitted.</sub>
{end}"""
    current = path.read_text()
    before, separator, remainder = current.partition(start)
    if not separator:
        raise RuntimeError(f"Missing {start} in {path}")
    _, separator, after = remainder.partition(end)
    if not separator:
        raise RuntimeError(f"Missing {end} in {path}")
    path.write_text(before + block + after)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh the profile activity summary and responsive SVGs."
    )
    parser.add_argument("--login", default="msegec")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    profile = load_profile(args.login)
    assets = root / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "github-activity.svg").write_text(render_svg(profile, mobile=False))
    (assets / "github-activity-mobile.svg").write_text(render_svg(profile, mobile=True))
    update_readme(root / "README.md", profile)


if __name__ == "__main__":
    main()
