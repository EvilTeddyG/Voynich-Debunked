#!/usr/bin/env python3
"""
Permutation/Bootstrap significance tests for key Voynich anomaly claims.

Tests included:
1) Bootstrap CI for H1 (conditional character entropy)
2) Permutation null for 13-word phrase-distance peak (3-gram repeats)
3) Permutation null for character autocorrelation lags (default: 5, 6)

This script does not prove any historical interpretation. It quantifies whether
observed signals are unusual under simple shuffled null models.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bootstrap and permutation significance tests")
    parser.add_argument("--input", default="data/takahashi_eva.txt", help="Transcript path")
    parser.add_argument("--min-ngram", type=int, default=3, help="N-gram length for distance test")
    parser.add_argument("--target-distance", type=int, default=13, help="Distance to test in phrase repeats")
    parser.add_argument("--lags", nargs="+", type=int, default=[5, 6], help="Character lags for autocorrelation tests")
    parser.add_argument("--bootstrap", type=int, default=300, help="Bootstrap replicates")
    parser.add_argument("--permutations", type=int, default=300, help="Permutation replicates")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--json-out", default=None, help="Optional JSON output path")
    return parser.parse_args()


def load_words_and_chars(path: str) -> tuple[list[str], list[str]]:
    words: list[str] = []
    chars: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("<f"):
                continue
            parts = line.split(">", 1)
            if len(parts) < 2:
                continue
            content = re.sub(r"[*!=]", "", parts[1]).strip()
            line_words = [re.sub(r"[^a-zA-Z]", "", w).strip() for w in re.split(r"[\s.-]", content)]
            line_words = [w for w in line_words if w]
            words.extend(line_words)
            chars.extend([c for c in "".join(line_words) if c.isalpha()])
    return words, chars


def conditional_entropy(chars: list[str]) -> float:
    if len(chars) < 2:
        return 0.0
    bigram_counts: Counter[tuple[str, str]] = Counter()
    cond_totals: Counter[str] = Counter()
    for i in range(len(chars) - 1):
        c1 = chars[i]
        c2 = chars[i + 1]
        bigram_counts[(c1, c2)] += 1
        cond_totals[c1] += 1

    h1 = 0.0
    total_bigrams = len(chars) - 1
    for (c1, c2), n in bigram_counts.items():
        p_bigram = n / total_bigrams
        p_cond = n / cond_totals[c1]
        h1 -= p_bigram * math.log2(p_cond)
    return h1


def repeated_distance_count(words: list[str], ngram_len: int, target_distance: int) -> int:
    positions: defaultdict[tuple[str, ...], list[int]] = defaultdict(list)
    for i in range(len(words) - ngram_len + 1):
        positions[tuple(words[i : i + ngram_len])].append(i)

    count = 0
    for pos in positions.values():
        if len(pos) < 2:
            continue
        for j in range(len(pos) - 1):
            if pos[j + 1] - pos[j] == target_distance:
                count += 1
    return count


def autocorr_score(chars: list[str], lag: int) -> float:
    if lag <= 0 or lag >= len(chars):
        return 0.0
    counts = Counter(chars)
    n = len(chars)
    expected = sum((v / n) ** 2 for v in counts.values())

    matches = 0
    comparisons = n - lag
    for i in range(comparisons):
        if chars[i] == chars[i + lag]:
            matches += 1
    observed = matches / comparisons if comparisons else 0.0
    return observed - expected


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = max(0, min(len(sorted_vals) - 1, int(round((p / 100.0) * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def stddev(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    var = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
    return math.sqrt(var)


def main() -> int:
    args = parse_args()
    random.seed(args.seed)

    words, chars = load_words_and_chars(args.input)
    if not words or not chars:
        print("ERROR: no analyzable transcript data found")
        return 1

    observed_h1 = conditional_entropy(chars)
    observed_d13 = repeated_distance_count(words, args.min_ngram, args.target_distance)
    observed_lag_scores = {lag: autocorr_score(chars, lag) for lag in args.lags}

    # Bootstrap H1
    h1_boot: list[float] = []
    for _ in range(args.bootstrap):
        sample = [chars[random.randrange(len(chars))] for _ in range(len(chars))]
        h1_boot.append(conditional_entropy(sample))
    h1_boot_sorted = sorted(h1_boot)

    # Permutation tests
    d13_perm: list[int] = []
    lag_perm: dict[int, list[float]] = {lag: [] for lag in args.lags}

    for _ in range(args.permutations):
        perm_words = words[:]
        random.shuffle(perm_words)
        d13_perm.append(repeated_distance_count(perm_words, args.min_ngram, args.target_distance))

        perm_chars = chars[:]
        random.shuffle(perm_chars)
        for lag in args.lags:
            lag_perm[lag].append(autocorr_score(perm_chars, lag))

    d13_p = (sum(1 for x in d13_perm if x >= observed_d13) + 1) / (len(d13_perm) + 1)
    lag_p = {
        lag: (sum(1 for x in scores if x >= observed_lag_scores[lag]) + 1) / (len(scores) + 1)
        for lag, scores in lag_perm.items()
    }

    d13_mean = mean(d13_perm)
    d13_sd = stddev([float(x) for x in d13_perm])
    d13_z = ((observed_d13 - d13_mean) / d13_sd) if d13_sd > 0 else 0.0

    lag_stats = {}
    for lag, scores in lag_perm.items():
        s_mean = mean(scores)
        s_sd = stddev(scores)
        lag_stats[lag] = {
            "mean": s_mean,
            "sd": s_sd,
            "z": ((observed_lag_scores[lag] - s_mean) / s_sd) if s_sd > 0 else 0.0,
            "q025": percentile(sorted(scores), 2.5),
            "q975": percentile(sorted(scores), 97.5),
        }

    print("=" * 80)
    print("SIGNIFICANCE TEST SUMMARY")
    print("=" * 80)
    print(f"Input: {args.input}")
    print(f"Tokens: {len(words):,} | Characters: {len(chars):,}")
    print()
    print("H1 bootstrap")
    print(f"  observed H1: {observed_h1:.4f}")
    print(f"  bootstrap mean: {mean(h1_boot):.4f}")
    print(f"  bootstrap 95% CI: [{percentile(h1_boot_sorted, 2.5):.4f}, {percentile(h1_boot_sorted, 97.5):.4f}]")
    print()
    print(f"Distance-{args.target_distance} phrase repeat permutation test")
    print(f"  observed count: {observed_d13}")
    print(f"  null mean: {d13_mean:.2f}")
    print(f"  null 95% range: [{percentile(sorted([float(x) for x in d13_perm]), 2.5):.2f}, {percentile(sorted([float(x) for x in d13_perm]), 97.5):.2f}]")
    print(f"  effect z-score: {d13_z:+.4f}")
    print(f"  p-value (>= observed): {d13_p:.6f}")
    print()
    print("Lag autocorrelation permutation tests")
    for lag in args.lags:
        print(
            "  lag "
            f"{lag}: observed={observed_lag_scores[lag]:+.6f}, "
            f"null_mean={lag_stats[lag]['mean']:+.6f}, "
            f"null_95=[{lag_stats[lag]['q025']:+.6f}, {lag_stats[lag]['q975']:+.6f}], "
            f"z={lag_stats[lag]['z']:+.4f}, p={lag_p[lag]:.6f}"
        )
    print("=" * 80)

    results = {
        "input_file": args.input,
        "counts": {"tokens": len(words), "chars": len(chars)},
        "h1_bootstrap": {
            "observed": observed_h1,
            "mean": mean(h1_boot),
            "ci95": [percentile(h1_boot_sorted, 2.5), percentile(h1_boot_sorted, 97.5)],
            "replicates": args.bootstrap,
        },
        "distance_test": {
            "ngram_len": args.min_ngram,
            "target_distance": args.target_distance,
            "observed": observed_d13,
            "null_mean": d13_mean,
            "null_sd": d13_sd,
            "null_q025": percentile(sorted([float(x) for x in d13_perm]), 2.5),
            "null_q975": percentile(sorted([float(x) for x in d13_perm]), 97.5),
            "z_score": d13_z,
            "p_value_ge": d13_p,
            "replicates": args.permutations,
        },
        "lag_tests": {
            str(lag): {
                "observed": observed_lag_scores[lag],
                "null_mean": lag_stats[lag]["mean"],
                "null_sd": lag_stats[lag]["sd"],
                "null_q025": lag_stats[lag]["q025"],
                "null_q975": lag_stats[lag]["q975"],
                "z_score": lag_stats[lag]["z"],
                "p_value_ge": lag_p[lag],
            }
            for lag in args.lags
        },
        "seed": args.seed,
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"JSON results written to: {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
