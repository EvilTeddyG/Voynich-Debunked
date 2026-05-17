#!/usr/bin/env python3
"""
Lag-spectrum comparison across Voynich and labeled control corpora.

Generates null-calibrated lag spectra (1..max_lag) for each corpus and outputs:
- long-format CSV (easy plotting)
- summary JSON (peak ranks, target-lag stats)

This is intended to support scrutiny of periodicity claims (e.g., 5/6-char lags,
13-word-related lag structures) against family-conditioned controls.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import re
from collections import Counter
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Null-calibrated lag spectra for Voynich + controls")
    parser.add_argument("--voynich", default="data/takahashi_eva.txt", help="Voynich transcript path")
    parser.add_argument("--manifest", default="data/baselines/manifest_template.csv", help="Control manifest CSV")
    parser.add_argument("--max-lag", type=int, default=60, help="Maximum lag for spectra")
    parser.add_argument("--target-lags", nargs="+", type=int, default=[5, 6, 12, 13], help="Lags to summarize")
    parser.add_argument("--permutations", type=int, default=200, help="Null permutations per corpus")
    parser.add_argument(
        "--store-null-profiles",
        action="store_true",
        help="Store full null lag profiles per corpus in JSON (larger file; needed for PSD null confidence bands)",
    )
    parser.add_argument(
        "--store-null-targets",
        action="store_true",
        help="Store null sample arrays for target lags in JSON (larger file, enables histogram plots)",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--csv-out", default="artifacts/lag_spectrum_compare.csv", help="Output long CSV")
    parser.add_argument("--json-out", default="artifacts/lag_spectrum_compare.json", help="Output summary JSON")
    return parser.parse_args()


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = max(0, min(len(sorted_vals) - 1, int(round((p / 100.0) * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def stddev(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))


def resolve_path(base_manifest: str, rel_or_abs: str) -> str:
    if os.path.isabs(rel_or_abs):
        return rel_or_abs
    return os.path.normpath(os.path.join(os.path.dirname(base_manifest), rel_or_abs))


def read_manifest(path: str) -> list[dict[str, str]]:
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            if row.get("label") and row.get("path") and row.get("family"):
                rows.append(row)
    return rows


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


def chars_from_lines(lines: list[str]) -> list[str]:
    words = []
    for line in lines:
        toks = [re.sub(r"[^a-zA-Z]", "", w).strip() for w in re.split(r"[\s.-]", line)]
        words.extend([w for w in toks if w])
    return [c for w in words for c in w if c.isalpha()]


def lag_profile(chars: list[str], max_lag: int) -> dict[int, float]:
    n = len(chars)
    if n == 0:
        return {lag: 0.0 for lag in range(1, max_lag + 1)}
    probs = Counter(chars)
    expected = sum((v / n) ** 2 for v in probs.values())

    out = {}
    for lag in range(1, max_lag + 1):
        if lag >= n:
            out[lag] = 0.0
            continue
        comp = n - lag
        matches = 0
        for i in range(comp):
            if chars[i] == chars[i + lag]:
                matches += 1
        observed = matches / comp if comp else 0.0
        out[lag] = observed - expected
    return out


def rank_lag(profile: dict[int, float], lag: int) -> int:
    ranked = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    for i, (k, _) in enumerate(ranked, start=1):
        if k == lag:
            return i
    return len(ranked) + 1


def main() -> int:
    args = parse_args()
    random.seed(args.seed)

    corpora = [{"label": "voynich", "family": "voynich", "path": args.voynich, "voynich_mode": True}]
    for row in read_manifest(args.manifest):
        p = resolve_path(args.manifest, row["path"])
        if os.path.exists(p):
            corpora.append({"label": row["label"], "family": row["family"], "path": p, "voynich_mode": False})

    if len(corpora) <= 1:
        print("ERROR: no control corpora resolved")
        return 1

    long_rows = []
    summary = {"max_lag": args.max_lag, "target_lags": args.target_lags, "corpora": []}

    for c in corpora:
        lines = extract_lines(c["path"], c["voynich_mode"])
        chars = chars_from_lines(lines)
        obs = lag_profile(chars, args.max_lag)

        # Null distributions for each lag
        null_by_lag = {lag: [] for lag in range(1, args.max_lag + 1)}
        null_profiles = []
        for _ in range(args.permutations):
            s = chars[:]
            random.shuffle(s)
            prof = lag_profile(s, args.max_lag)
            if args.store_null_profiles:
                null_profiles.append([prof[lag] for lag in range(1, args.max_lag + 1)])
            for lag, v in prof.items():
                null_by_lag[lag].append(v)

        target_stats = {}
        target_null_samples = {}
        for lag in args.target_lags:
            vals = null_by_lag.get(lag, [])
            vals_sorted = sorted(vals)
            nm = mean(vals) if vals else 0.0
            ns = stddev(vals)
            ov = obs.get(lag, 0.0)
            p = (sum(1 for x in vals if x >= ov) + 1) / (len(vals) + 1) if vals else 1.0
            z = (ov - nm) / ns if ns > 0 else 0.0
            target_stats[str(lag)] = {
                "observed": ov,
                "null_mean": nm,
                "null_sd": ns,
                "null_q025": percentile(vals_sorted, 2.5),
                "null_q975": percentile(vals_sorted, 97.5),
                "p_value_ge": p,
                "z_score": z,
                "rank": rank_lag(obs, lag),
            }
            if args.store_null_targets:
                target_null_samples[str(lag)] = vals

        # Long rows for plotting
        for lag in range(1, args.max_lag + 1):
            vals = null_by_lag[lag]
            vals_sorted = sorted(vals)
            nm = mean(vals) if vals else 0.0
            ns = stddev(vals)
            ov = obs[lag]
            z = (ov - nm) / ns if ns > 0 else 0.0
            long_rows.append(
                {
                    "label": c["label"],
                    "family": c["family"],
                    "lag": lag,
                    "observed": ov,
                    "null_mean": nm,
                    "null_q025": percentile(vals_sorted, 2.5),
                    "null_q975": percentile(vals_sorted, 97.5),
                    "z_score": z,
                }
            )

        summary["corpora"].append(
            {
                "label": c["label"],
                "family": c["family"],
                "path": c["path"],
                "char_count": len(chars),
                "observed_profile": [obs[lag] for lag in range(1, args.max_lag + 1)],
                "target_lag_stats": target_stats,
                "target_lag_null_samples": target_null_samples if args.store_null_targets else None,
                "null_profiles": null_profiles if args.store_null_profiles else None,
                "peak_lag": max(obs, key=lambda k: obs[k]),
                "peak_value": max(obs.values()) if obs else 0.0,
            }
        )

    os.makedirs(os.path.dirname(args.csv_out), exist_ok=True)
    with open(args.csv_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["label", "family", "lag", "observed", "null_mean", "null_q025", "null_q975", "z_score"])
        w.writeheader()
        w.writerows(long_rows)

    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 80)
    print("LAG SPECTRUM COMPARISON COMPLETE")
    print("=" * 80)
    print(f"Corpora: {len(corpora)}")
    print(f"CSV: {args.csv_out}")
    print(f"JSON: {args.json_out}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
