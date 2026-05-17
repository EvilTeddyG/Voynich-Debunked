#!/usr/bin/env python3
"""
Cross-validation scaffold for Voynich character-transition modeling.

Goal: Train a character-bigram model on a folio subset and evaluate held-out
folios, reporting held-out cross-entropy/perplexity and comparison vs unigram
baseline.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Folio-level cross-validation for bigram model")
    parser.add_argument("--input", default="data/takahashi_eva.txt", help="Transcript path")
    parser.add_argument("--holdout-frac", type=float, default=0.2, help="Fraction of folios held out")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--alpha", type=float, default=0.5, help="Laplace smoothing alpha")
    parser.add_argument("--repeats", type=int, default=20, help="Number of repeated random holdouts")
    parser.add_argument("--json-out", default=None, help="Optional JSON output path")
    return parser.parse_args()


def parse_folio_id(header: str) -> str:
    # Example header token: f1r.P.1 -> folio id f1r
    token = header.split(".")[0]
    return token


def load_folio_chars(path: str) -> dict[str, list[str]]:
    by_folio: dict[str, list[str]] = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("<f"):
                continue
            m = re.match(r"<([^>]+)>", line)
            if not m:
                continue
            header = m.group(1)
            folio = parse_folio_id(header)
            content = line.split(">", 1)[1]
            clean = re.sub(r"[^a-zA-Z]", "", content)
            chars = [c for c in clean if c.isalpha()]
            by_folio[folio].extend(chars)
    return by_folio


def build_models(chars: list[str], alpha: float):
    vocab = sorted(set(chars))
    v = len(vocab)
    if v == 0:
        return {}, {}, vocab

    unigram = Counter(chars)
    bigram = Counter((chars[i], chars[i + 1]) for i in range(len(chars) - 1))
    left_totals = Counter(chars[i] for i in range(len(chars) - 1))

    # Convert to probability tables with smoothing
    p_uni = {}
    denom_uni = len(chars) + alpha * v
    for c in vocab:
        p_uni[c] = (unigram[c] + alpha) / denom_uni

    p_bi = defaultdict(dict)
    for c1 in vocab:
        denom = left_totals[c1] + alpha * v
        for c2 in vocab:
            p_bi[c1][c2] = (bigram[(c1, c2)] + alpha) / denom if denom > 0 else 1.0 / v

    return p_uni, p_bi, vocab


def cross_entropy_unigram(test_chars: list[str], p_uni: dict[str, float], unk_prob: float) -> float:
    if not test_chars:
        return 0.0
    loss = 0.0
    for c in test_chars:
        p = p_uni.get(c, unk_prob)
        loss += -math.log2(p)
    return loss / len(test_chars)


def cross_entropy_bigram(test_chars: list[str], p_bi, vocab: list[str], unk_prob: float) -> float:
    if len(test_chars) < 2:
        return 0.0
    loss = 0.0
    n = 0
    for i in range(len(test_chars) - 1):
        c1, c2 = test_chars[i], test_chars[i + 1]
        p = p_bi.get(c1, {}).get(c2, unk_prob if vocab else 1e-9)
        loss += -math.log2(p)
        n += 1
    return loss / n if n else 0.0


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = max(0, min(len(sorted_vals) - 1, int(round((p / 100.0) * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def main() -> int:
    args = parse_args()
    random.seed(args.seed)

    by_folio = load_folio_chars(args.input)
    folios = sorted(by_folio.keys())
    if len(folios) < 2:
        print("ERROR: not enough folios parsed for cross-validation")
        return 1

    holdout_n = max(1, int(round(len(folios) * args.holdout_frac)))

    run_rows = []
    ce_uni_list = []
    ce_bi_list = []
    delta_list = []

    for r in range(args.repeats):
        holdout = set(random.sample(folios, holdout_n))
        train = [f for f in folios if f not in holdout]

        train_chars = [c for f in train for c in by_folio[f]]
        test_chars = [c for f in holdout for c in by_folio[f]]

        p_uni, p_bi, vocab = build_models(train_chars, args.alpha)
        v = max(1, len(vocab))
        unk_prob = 1.0 / (len(train_chars) + args.alpha * v)

        ce_uni = cross_entropy_unigram(test_chars, p_uni, unk_prob)
        ce_bi = cross_entropy_bigram(test_chars, p_bi, vocab, unk_prob)
        delta = ce_uni - ce_bi

        ce_uni_list.append(ce_uni)
        ce_bi_list.append(ce_bi)
        delta_list.append(delta)

        run_rows.append(
            {
                "run": r + 1,
                "train_folios": train,
                "holdout_folios": sorted(holdout),
                "train_chars": len(train_chars),
                "holdout_chars": len(test_chars),
                "cross_entropy_unigram": ce_uni,
                "cross_entropy_bigram": ce_bi,
                "improvement_bits_per_char": delta,
            }
        )

    ce_uni_mean = sum(ce_uni_list) / len(ce_uni_list)
    ce_bi_mean = sum(ce_bi_list) / len(ce_bi_list)
    delta_mean = sum(delta_list) / len(delta_list)

    ce_uni_sorted = sorted(ce_uni_list)
    ce_bi_sorted = sorted(ce_bi_list)
    delta_sorted = sorted(delta_list)

    print("=" * 80)
    print("FOLIO HOLD-OUT CROSS-VALIDATION")
    print("=" * 80)
    print(f"Input: {args.input}")
    print(f"Folios total: {len(folios)} | holdout per run: {holdout_n} | repeats: {args.repeats}")
    print()
    print(
        "Unigram holdout cross-entropy: "
        f"mean={ce_uni_mean:.4f}, 95% range=[{percentile(ce_uni_sorted, 2.5):.4f}, {percentile(ce_uni_sorted, 97.5):.4f}]"
    )
    print(
        "Bigram  holdout cross-entropy: "
        f"mean={ce_bi_mean:.4f}, 95% range=[{percentile(ce_bi_sorted, 2.5):.4f}, {percentile(ce_bi_sorted, 97.5):.4f}]"
    )
    print(
        "Improvement (uni - bi): "
        f"mean={delta_mean:+.4f} bits/char, 95% range=[{percentile(delta_sorted, 2.5):+.4f}, {percentile(delta_sorted, 97.5):+.4f}]"
    )
    ppl_uni = 2 ** ce_uni_mean if ce_uni_mean > 0 else 1.0
    ppl_bi = 2 ** ce_bi_mean if ce_bi_mean > 0 else 1.0
    print(f"Perplexity (means): unigram={ppl_uni:.4f}, bigram={ppl_bi:.4f}")
    print("=" * 80)

    results = {
        "input_file": args.input,
        "seed": args.seed,
        "alpha": args.alpha,
        "folios_total": len(folios),
        "repeats": args.repeats,
        "holdout_frac": args.holdout_frac,
        "holdout_per_run": holdout_n,
        "metrics": {
            "cross_entropy_unigram_mean": ce_uni_mean,
            "cross_entropy_unigram_q025": percentile(ce_uni_sorted, 2.5),
            "cross_entropy_unigram_q975": percentile(ce_uni_sorted, 97.5),
            "cross_entropy_bigram_mean": ce_bi_mean,
            "cross_entropy_bigram_q025": percentile(ce_bi_sorted, 2.5),
            "cross_entropy_bigram_q975": percentile(ce_bi_sorted, 97.5),
            "perplexity_unigram": ppl_uni,
            "perplexity_bigram": ppl_bi,
            "improvement_bits_per_char_mean": delta_mean,
            "improvement_bits_per_char_q025": percentile(delta_sorted, 2.5),
            "improvement_bits_per_char_q975": percentile(delta_sorted, 97.5),
        },
        "runs": run_rows,
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"JSON results written to: {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
