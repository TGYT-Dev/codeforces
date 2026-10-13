#!/usr/bin/env python3
"""Usage: ratingGraph.py HANDLE [out.png]

Every run records the current rating in rating_history.json (created next
to this script) so future graphs include the days between contests. The
graph covers only the past month, with daily date labels along the
bottom and real Codeforces rank titles on their bands; it ends with a
dot at the current day connected back to the last contest.
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

# gruvbox
bg, fg, gray, yellow = "#1d2021", "#ebdbb2", "#928374", "#fabd2f"
bands = [
    (0, 1200, "#928374", "Newbie"),
    (1200, 1400, "#b8bb26", "Pupil"),
    (1400, 1600, "#8ec07c", "Specialist"),
    (1600, 1900, "#83a598", "Expert"),
    (1900, 2100, "#d3869b", "Candidate Master"),
    (2100, 2300, "#fe8019", "Master"),
    (2300, 2400, "#fe8019", "International Master"),
    (2400, 2600, "#fb4934", "Grandmaster"),
    (2600, 3000, "#fb4934", "International Grandmaster"),
    (3000, 4000, "#fb4934", "Legendary Grandmaster"),
]


def rankTitle(rating):
    for start, end, _, name in bands:
        if start <= rating < end:
            return name
    return bands[-1][3]

HISTORY_FILE = Path(__file__).resolve().parent / "rating_history.json"
WINDOW = timedelta(days=30)


def fetchRatings(handle):
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)
    if data["status"] != "OK":
        sys.exit(data.get("comment", "Codeforces API error"))
    if not data["result"]:
        sys.exit("No rated contests yet")
    return sorted(
        (datetime.fromtimestamp(entry["ratingUpdateTimeSeconds"], timezone.utc), entry["newRating"])
        for entry in data["result"]
    )


def loadHistory():
    try:
        return json.loads(HISTORY_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def saveSnapshot(handle, rating, now):
    history = loadHistory()
    days = history.setdefault(handle.lower(), {})
    days[now.strftime("%Y-%m-%d")] = rating  # one snapshot per day, latest wins
    HISTORY_FILE.write_text(json.dumps(history, indent=2, sort_keys=True))


def trackedPoints(handle):
    return [
        (datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc, hour=12), rating)
        for day, rating in loadHistory().get(handle.lower(), {}).items()
    ]


def drawGraph(handle, contests, tracked, now, outPath):
    current, peak = contests[-1][1], max(r for _, r in contests)
    windowStart = now - WINDOW

    shownContests = [p for p in contests if p[0] >= windowStart]
    lastContest = contests[-1]
    if lastContest[0] < windowStart:  # keep it so the line always reaches the current day
        shownContests.insert(0, lastContest)
    shownTracked = [p for p in tracked if p[0] >= windowStart and p[0].date() < now.date()]
    line = sorted(shownContests + shownTracked + [(now, current)])

    visible = [p for p in line if p[0] >= windowStart]
    low = max(0, (min(r for _, r in visible) - 100) // 100 * 100)
    high = (max(r for _, r in visible) + 100) // 100 * 100 + 100

    fig, ax = plt.subplots(figsize=(8, 3.4), dpi=150)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    for start, end, color, name in bands:
        if start < high and end > low:
            ax.axhspan(max(start, low), min(end, high), color=color, alpha=0.22, lw=0)

    # real Codeforces rank titles beside their bands
    trans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    marks = []
    for start, end, color, name in bands:
        v0, v1 = max(start, low), min(end, high)
        if v1 - v0 >= 40:
            marks.append([(v0 + v1) / 2, name, color])
    gap = max(30, (high - low) * 0.06)
    for i in range(1, len(marks)):  # nudge apart if bands are thin
        if marks[i][0] - marks[i - 1][0] < gap:
            marks[i][0] = marks[i - 1][0] + gap
    for y, name, color in marks:
        ax.text(0.01, y, name, transform=trans, ha="left", va="center",
                fontsize=7, color=color, family="monospace", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", facecolor=bg, edgecolor="none", alpha=0.8))

    xs, ys = zip(*line)
    ax.plot(xs, ys, color=yellow, lw=1.8, solid_capstyle="round", zorder=3)
    ax.scatter([t for t, _ in shownContests], [r for _, r in shownContests], color=fg, s=12, zorder=4)
    ax.scatter([t for t, _ in shownTracked], [r for _, r in shownTracked], color=fg, s=6, zorder=4)
    ax.scatter([lastContest[0]], [lastContest[1]], color=fg, s=30, zorder=4)
    ax.scatter([now], [current], color=yellow, s=36, zorder=5, edgecolor=bg, linewidth=1.5)

    ax.set_xlim(windowStart - timedelta(days=1), now + timedelta(days=1))
    ax.set_ylim(low, high)
    ax.set_yticks(range(low, high + 1, 100))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.tick_params(colors=gray, labelsize=7, length=0)
    plt.setp(ax.get_xticklabels(), rotation=80, ha="right")
    ax.grid(axis="y", color="#504945", lw=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(
        0.99, 0.96, f"{handle}  {current}  {rankTitle(current)}  (peak {peak})",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=8, color=yellow, family="monospace",
    )

    fig.tight_layout()
    fig.savefig(outPath, facecolor=bg)


if __name__ == "__main__":
    handle = sys.argv[1]
    outPath = sys.argv[2] if len(sys.argv) > 2 else "rating.png"
    now = datetime.now(timezone.utc)
    ratings = fetchRatings(handle)
    saveSnapshot(handle, ratings[-1][1], now)
    drawGraph(handle, ratings, trackedPoints(handle), now, outPath)