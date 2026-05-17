#!/usr/bin/env python3
"""
Create publication-ready spectral and null-distribution visualizations from
lag_spectrum_compare outputs.

Inputs:
- Long CSV from lag_spectrum_compare.py
- Summary JSON from lag_spectrum_compare.py

Outputs (PNG files):
1) Comparative lag spectra with null bands (Voynich + controls)
2) Family-aggregated lag spectra (mean +/- sd)
3) Null histograms for target lags (Voynich observed vs null samples)
"""

from __future__ import annotations

import argparse
import cmath
import csv
import json
import os
from collections import defaultdict
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot lag spectra and null distributions")
    parser.add_argument("--csv", default="artifacts/lag_spectrum_compare.csv", help="Long-format CSV from lag_spectrum_compare.py")
    parser.add_argument("--json", default="artifacts/lag_spectrum_compare.json", help="Summary JSON from lag_spectrum_compare.py")
    parser.add_argument("--outdir", default="artifacts/plots", help="Output plot directory")
    parser.add_argument(
        "--top-controls",
        type=int,
        default=0,
        help="Max non-Voynich corpus lines in comparative plot (0 = all)",
    )
    return parser.parse_args()


def load_csv(path: str):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(
                {
                    "label": row["label"],
                    "family": row["family"],
                    "lag": int(row["lag"]),
                    "observed": float(row["observed"]),
                    "null_mean": float(row["null_mean"]),
                    "null_q025": float(row["null_q025"]),
                    "null_q975": float(row["null_q975"]),
                    "z_score": float(row["z_score"]),
                }
            )
    return rows


def plot_comparative(rows, summary, outpath, top_controls=8):
    import matplotlib.pyplot as plt

    by_label = defaultdict(list)
    for r in rows:
        by_label[r["label"]].append(r)

    for label in by_label:
        by_label[label].sort(key=lambda x: x["lag"])

    # Identify nearest controls from summary if available
    nearest = [c["label"] for c in summary.get("corpora", []) if c.get("label") != "voynich"]
    if top_controls > 0 and len(nearest) > top_controls:
        nearest = nearest[:top_controls]

    plt.figure(figsize=(12, 7))

    # Plot Voynich with null band
    vrows = by_label.get("voynich", [])
    if vrows:
        lags = [r["lag"] for r in vrows]
        obs = [r["observed"] for r in vrows]
        ql = [r["null_q025"] for r in vrows]
        qh = [r["null_q975"] for r in vrows]
        plt.fill_between(lags, ql, qh, alpha=0.2, color="black", label="Voynich null 95% band")
        plt.plot(lags, obs, color="black", linewidth=2.5, label="Voynich observed")

    # Plot selected controls lightly
    plotted = 0
    for label, vals in by_label.items():
        if label == "voynich":
            continue
        if nearest and top_controls > 0 and label not in nearest:
            continue
        lags = [r["lag"] for r in vals]
        obs = [r["observed"] for r in vals]
        plt.plot(lags, obs, linewidth=1.0, alpha=0.55, label=f"{label} ({vals[0]['family']})")
        plotted += 1
        if top_controls > 0 and plotted >= top_controls:
            break

    plt.axhline(0.0, linestyle="--", linewidth=0.8, color="gray")
    plt.title("Comparative Character-Lag Spectra (Observed vs Voynich Null Band)")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation deviation")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()


def plot_family_aggregate(rows, outpath):
    import matplotlib.pyplot as plt

    by_family_lag = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["family"] == "voynich":
            continue
        by_family_lag[r["family"]][r["lag"]].append(r["observed"])

    plt.figure(figsize=(12, 7))
    for family, lag_map in sorted(by_family_lag.items()):
        lags = sorted(lag_map.keys())
        mu = [mean(lag_map[lag]) for lag in lags]
        sd = []
        n_by_lag = []
        for lag in lags:
            vals = lag_map[lag]
            m = mean(vals)
            var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1) if len(vals) > 1 else 0.0
            sd.append(var ** 0.5)
            n_by_lag.append(max(1, len(vals)))

        # 95% confidence band on family mean (normal approximation)
        low = [m - 1.96 * (s / (n ** 0.5)) for m, s, n in zip(mu, sd, n_by_lag)]
        high = [m + 1.96 * (s / (n ** 0.5)) for m, s, n in zip(mu, sd, n_by_lag)]

        plt.plot(lags, mu, linewidth=1.8, label=family)
        plt.fill_between(lags, low, high, alpha=0.15)

    # Voynich overlay
    vrows = sorted([r for r in rows if r["label"] == "voynich"], key=lambda x: x["lag"])
    if vrows:
        plt.plot([r["lag"] for r in vrows], [r["observed"] for r in vrows], color="black", linewidth=2.8, label="voynich")

    plt.axhline(0.0, linestyle="--", linewidth=0.8, color="gray")
    plt.title("Family-Aggregated Lag Spectra (Controls) with Voynich Overlay")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation deviation")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()


def plot_voynich_null_hist(summary, outpath_prefix):
    import matplotlib.pyplot as plt

    voynich = None
    for c in summary.get("corpora", []):
        if c.get("label") == "voynich":
            voynich = c
            break

    if not voynich:
        return []

    stats = voynich.get("target_lag_stats", {})
    null_samples = voynich.get("target_lag_null_samples") or {}

    generated = []
    for lag, lag_stats in sorted(stats.items(), key=lambda kv: int(kv[0])):
        samples = null_samples.get(lag)
        if not samples:
            continue
        obs = lag_stats["observed"]
        p = lag_stats["p_value_ge"]
        z = lag_stats["z_score"]

        outpath = f"{outpath_prefix}_lag{lag}.png"
        plt.figure(figsize=(8, 5))
        plt.hist(samples, bins=40, alpha=0.75)
        plt.axvline(obs, color="red", linewidth=2.0, label=f"observed={obs:+.5f}")
        plt.title(f"Voynich Null Distribution at Lag {lag} (p={p:.4g}, z={z:+.3f})")
        plt.xlabel("Autocorrelation deviation")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(outpath, dpi=180)
        plt.close()
        generated.append(outpath)

    return generated


def periodogram(series):
    # Simple DFT-based periodogram for short lag series.
    n = len(series)
    if n < 4:
        return [], []

    # Remove DC component
    m = mean(series)
    x = [v - m for v in series]

    freqs = []
    power = []
    max_k = n // 2
    for k in range(1, max_k + 1):
        s = 0j
        for t, xt in enumerate(x):
            angle = -2.0j * cmath.pi * k * t / n
            s += xt * cmath.exp(angle)
        p = (s.real * s.real + s.imag * s.imag) / n
        freqs.append(k / n)
        power.append(p)
    return freqs, power


def plot_periodogram(summary, outpath):
    import matplotlib.pyplot as plt

    corpora = summary.get("corpora", [])
    if not corpora:
        return False

    plt.figure(figsize=(12, 7))

    for c in corpora:
        label = c.get("label", "unknown")
        family = c.get("family", "unknown")
        obs_profile = c.get("observed_profile") or []
        if not obs_profile:
            continue

        f_obs, p_obs = periodogram(obs_profile)
        if label == "voynich":
            # Optional null PSD confidence band if null profiles were stored.
            null_profiles = c.get("null_profiles") or []
            if null_profiles:
                null_psd = []
                for prof in null_profiles:
                    _, p = periodogram(prof)
                    null_psd.append(p)

                if null_psd:
                    m = len(null_psd[0])
                    q025 = []
                    q975 = []
                    for i in range(m):
                        vals = sorted(row[i] for row in null_psd)
                        q025.append(vals[max(0, int(round(0.025 * (len(vals) - 1))))])
                        q975.append(vals[max(0, int(round(0.975 * (len(vals) - 1))))])
                    plt.fill_between(f_obs, q025, q975, color="black", alpha=0.2, label="Voynich null PSD 95% band")

            plt.plot(f_obs, p_obs, color="black", linewidth=2.8, label="Voynich PSD")
        else:
            plt.plot(f_obs, p_obs, linewidth=1.0, alpha=0.45, label=f"{label} ({family})")

    plt.title("Lag-Spectrum Periodogram (Frequency Domain)")
    plt.xlabel("Frequency (cycles per lag index)")
    plt.ylabel("Power")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()
    return True


def main() -> int:
    args = parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    rows = load_csv(args.csv)
    with open(args.json, "r", encoding="utf-8") as f:
        summary = json.load(f)

    comparative_png = os.path.join(args.outdir, "lag_spectra_comparative.png")
    family_png = os.path.join(args.outdir, "lag_spectra_family_aggregate.png")
    psd_png = os.path.join(args.outdir, "lag_spectra_periodogram.png")

    try:
        plot_comparative(rows, summary, comparative_png, top_controls=args.top_controls)
        plot_family_aggregate(rows, family_png)
        has_psd = plot_periodogram(summary, psd_png)
        hist_paths = plot_voynich_null_hist(summary, os.path.join(args.outdir, "voynich_null_hist"))
    except ModuleNotFoundError as exc:
        print("ERROR: plotting requires matplotlib. Install with: pip install matplotlib")
        print(f"Missing module: {exc}")
        return 1

    print("=" * 80)
    print("LAG SPECTRUM PLOTS GENERATED")
    print("=" * 80)
    print(f"Comparative plot: {comparative_png}")
    print(f"Family aggregate plot: {family_png}")
    if has_psd:
        print(f"Periodogram plot: {psd_png}")
    if hist_paths:
        print("Null histogram plots:")
        for p in hist_paths:
            print(f"  - {p}")
    else:
        print("No null histogram plots were generated.")
        print("Tip: re-run lag_spectrum_compare.py with --store-null-targets")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
