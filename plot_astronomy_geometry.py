#!/usr/bin/env python3
"""
Plot candidate ranking and null calibration diagnostics for astronomy geometry scoring.
"""

from __future__ import annotations

import argparse
import csv
import json
import os


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Plot astronomy geometry scoring diagnostics")
    p.add_argument("--csv", default="artifacts/astronomy_candidate_scores.csv", help="Candidate score CSV")
    p.add_argument("--json", default="artifacts/astronomy_overlay_report.json", help="Scoring report JSON")
    p.add_argument("--out", default="artifacts/plots/astronomy_overlay_panels.png", help="Output PNG")
    return p.parse_args()


def load_scores(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(
                {
                    "rank": int(row["rank"]),
                    "event_id": row["event_id"],
                    "date": row["date"],
                    "score": float(row["score"]),
                }
            )
    rows.sort(key=lambda x: x["rank"])
    return rows


def main() -> int:
    args = parse_args()

    rows = load_scores(args.csv)
    with open(args.json, "r", encoding="utf-8") as f:
        report = json.load(f)

    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        print("ERROR: plotting requires matplotlib. Install with: pip install matplotlib")
        print(f"Missing module: {exc}")
        return 1

    top = rows[: min(8, len(rows))]
    labels = [f"{r['event_id']}\n{r['date']}" for r in top]
    vals = [r["score"] for r in top]

    null = report.get("null_calibration", {})
    q025 = null.get("null_q025", 0.0)
    q975 = null.get("null_q975", 0.0)
    best = report.get("best_candidate", {})
    best_score = best.get("score", 0.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    ax1.bar(range(len(top)), vals, color="#4C78A8")
    ax1.set_xticks(range(len(top)), labels=labels, rotation=35, ha="right")
    ax1.set_ylabel("Score (lower is better)")
    ax1.set_title("Top Candidate Event Scores")
    if vals:
        ax1.axhline(vals[0], color="black", linestyle="--", linewidth=0.9, label="Best score")
        ax1.legend(fontsize=8)

    ax2.axhspan(q025, q975, alpha=0.2, color="gray", label="Null 95% band")
    ax2.axhline(best_score, color="red", linewidth=2.0, label="Best candidate score")
    ax2.set_xlim(0, 1)
    ax2.set_xticks([])
    ax2.set_ylabel("Score")
    ax2.set_title("Best Score vs Null Band")
    ax2.legend(fontsize=8)

    fig.suptitle("Astronomy Geometry Matching Diagnostics")
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    fig.savefig(args.out, dpi=180)
    plt.close(fig)

    print("=" * 80)
    print("ASTRONOMY OVERLAY PANELS GENERATED")
    print("=" * 80)
    print(f"Output: {args.out}")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
