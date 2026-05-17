#!/usr/bin/env python3
"""
Benchmark Voynich metrics against a directory of comparison corpora.

Each corpus is processed with the same normalization policy and evaluated on:
- character H0
- character H1
- line-position polarization (max concentration over start/mid/end)
- lag autocorrelation scores at specified lags

Input corpus format for fair comparison:
- one line per text line
- plain text allowed
- only alphabetic characters retained for character metrics
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
from collections import Counter, defaultdict
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run metric panel across comparison corpora")
    parser.add_argument("--voynich", default="data/takahashi_eva.txt", help="Voynich transcript path")
    parser.add_argument("--corpora-dir", required=True, help="Directory containing comparison corpora")
    parser.add_argument("--lags", nargs="+", type=int, default=[5, 6, 12, 13], help="Lags for autocorrelation scores")
    parser.add_argument("--min-word-count", type=int, default=20, help="Min word count for polarization stats")
    parser.add_argument("--csv-out", default="artifacts/baseline_benchmark.csv", help="Output CSV path")
    parser.add_argument("--json-out", default=None, help="Optional JSON output path")
    return parser.parse_args()


def extract_lines(path: str, voynich_mode: bool) -> list[str]:
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            if voynich_mode:
                if not raw.startswith("<f"):
                    continue
                parts = raw.split(">", 1)
                if len(parts) < 2:
                    continue
                raw = parts[1]
            lines.append(raw.strip())
    return lines


def normalize_words(line: str) -> list[str]:
    words = [re.sub(r"[^a-zA-Z]", "", w).strip() for w in re.split(r"[\s.-]", line)]
    return [w for w in words if w]


def entropy_h0_h1(chars: list[str]) -> tuple[float, float]:
    if not chars:
        return 0.0, 0.0

    n = len(chars)
    counts = Counter(chars)
    h0 = 0.0
    for c in counts.values():
        p = c / n
        h0 -= p * math.log2(p)

    if n < 2:
        return h0, 0.0

    bi = Counter((chars[i], chars[i + 1]) for i in range(n - 1))
    left = Counter(chars[i] for i in range(n - 1))
    h1 = 0.0
    for (c1, c2), k in bi.items():
        p_bigram = k / (n - 1)
        p_cond = k / left[c1]
        h1 -= p_bigram * math.log2(p_cond)
    return h0, h1


def line_polarization(lines_words: list[list[str]], min_word_count: int) -> float:
    pos = defaultdict(Counter)
    totals = Counter()

    for words in lines_words:
        if len(words) < 3:
            continue
        pos["start"][words[0]] += 1
        pos["end"][words[-1]] += 1
        for w in words[1:-1]:
            pos["mid"][w] += 1
        for w in words:
            totals[w] += 1

    max_ps = []
    for w, total in totals.items():
        if total < min_word_count:
            continue
        p_start = pos["start"][w] / total
        p_mid = pos["mid"][w] / total
        p_end = pos["end"][w] / total
        max_ps.append(max(p_start, p_mid, p_end))

    return mean(max_ps) if max_ps else 0.0


def autocorr_score(chars: list[str], lag: int) -> float:
    if lag <= 0 or lag >= len(chars):
        return 0.0
    counts = Counter(chars)
    n = len(chars)
    expected = sum((v / n) ** 2 for v in counts.values())
    matches = 0
    comp = n - lag
    for i in range(comp):
        if chars[i] == chars[i + lag]:
            matches += 1
    observed = matches / comp if comp else 0.0
    return observed - expected


def compute_metrics(path: str, voynich_mode: bool, lags: list[int], min_word_count: int) -> dict:
    raw_lines = extract_lines(path, voynich_mode)
    lines_words = [normalize_words(line) for line in raw_lines]
    words = [w for line in lines_words for w in line]
    chars = [c for w in words for c in w if c.isalpha()]

    h0, h1 = entropy_h0_h1(chars)
    pol = line_polarization(lines_words, min_word_count)
    lag_scores = {f"lag_{lag}": autocorr_score(chars, lag) for lag in lags}

    out = {
        "file": path,
        "tokens": len(words),
        "chars": len(chars),
        "H0": h0,
        "H1": h1,
        "mean_max_polarization": pol,
    }
    out.update(lag_scores)
    return out


def main() -> int:
    args = parse_args()

    rows = []
    rows.append(
        {
            "label": "voynich",
            **compute_metrics(args.voynich, True, args.lags, args.min_word_count),
        }
    )

    for name in sorted(os.listdir(args.corpora_dir)):
        full = os.path.join(args.corpora_dir, name)
        if not os.path.isfile(full):
            continue
        rows.append(
            {
                "label": os.path.splitext(name)[0],
                **compute_metrics(full, False, args.lags, args.min_word_count),
            }
        )

    os.makedirs(os.path.dirname(args.csv_out), exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(args.csv_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print("=" * 80)
    print("BASELINE BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"Rows written: {len(rows)}")
    print(f"CSV: {args.csv_out}")
    print("Labels:", ", ".join(r["label"] for r in rows))
    print("=" * 80)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
        print(f"JSON: {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
