from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import matplotlib.pyplot as plt
import numpy as np


def _load_riemann_sweep(csv_path: Path) -> tuple[np.ndarray, np.ndarray]:
    eps = []
    vals = []
    with csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("experiment") != "riemann_sweep":
                continue
            try:
                e = float(row["eps"])
                v = float(row["I2"])
            except (TypeError, ValueError, KeyError):
                continue
            if math.isfinite(e) and math.isfinite(v):
                eps.append(e)
                vals.append(v)
    return np.asarray(eps, dtype=float), np.asarray(vals, dtype=float)


def _winsorize(values: np.ndarray, lower_q: float = 0.05, upper_q: float = 0.95) -> np.ndarray:
    if values.size == 0:
        return values
    lo = float(np.quantile(values, lower_q))
    hi = float(np.quantile(values, upper_q))
    return np.clip(values, lo, hi)


def _normalize(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values
    lo = float(np.min(values))
    hi = float(np.max(values))
    if hi <= lo:
        return np.zeros_like(values)
    return (values - lo) / (hi - lo)


def run_riemann_diagnostics(output_dir: Path) -> dict[str, object]:
    csv_path = output_dir / "csv" / "riemann_sweep.csv"
    eps, vals = _load_riemann_sweep(csv_path)
    if eps.size == 0:
        return {"error": f"no riemann sweep rows found in {csv_path}"}

    order = np.argsort(eps)
    eps = eps[order]
    vals = vals[order]

    min_idx = int(np.argmin(vals))
    raw_min_eps = float(eps[min_idx])
    raw_min_val = float(vals[min_idx])

    norm = _normalize(vals)
    wins = _winsorize(vals)
    log_vals = np.log10(np.maximum(vals, np.finfo(float).tiny))

    diag_dir = output_dir / "diagnostics"
    plot_dir = diag_dir / "plots"
    diag_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    def _plot(series: np.ndarray, title: str, ylabel: str, filename: str) -> None:
        plt.figure(figsize=(8, 5))
        plt.plot(eps, series, linewidth=2)
        plt.axvline(0.0, color="black", linestyle="--", linewidth=1)
        plt.xlabel("eps")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(plot_dir / filename, dpi=160)
        plt.close()

    _plot(vals, "Riemann Sweep Raw I(eps)", "I2(eps)", "riemann_raw.png")
    _plot(log_vals, "Riemann Sweep log10 I(eps)", "log10 I2(eps)", "riemann_log.png")
    _plot(norm, "Riemann Sweep Normalized I(eps)", "normalized I2(eps)", "riemann_normalized.png")
    _plot(wins, "Riemann Sweep Winsorized I(eps)", "winsorized I2(eps)", "riemann_winsorized.png")

    pair_diffs = []
    for e, v in zip(eps, vals):
        if e < 0:
            continue
        match = vals[np.isclose(eps, -e, atol=1e-12)]
        if match.size:
            pair_diffs.append(float(abs(v - match[0])))

    symmetry_max_diff = max(pair_diffs) if pair_diffs else None

    report = {
        "raw_minimizer_eps": raw_min_eps,
        "raw_minimizer_value": raw_min_val,
        "raw_minimizer_is_zero": abs(raw_min_eps) <= 1e-12,
        "symmetry_max_abs_diff": symmetry_max_diff,
        "raw_value_range": [float(np.min(vals)), float(np.max(vals))],
        "raw_median": float(np.median(vals)),
        "raw_p95": float(np.quantile(vals, 0.95)),
        "raw_p99": float(np.quantile(vals, 0.99)),
        "normalized_minimizer_eps": float(eps[int(np.argmin(norm))]),
        "winsorized_minimizer_eps": float(eps[int(np.argmin(wins))]),
        "plots": {
            "raw": str(plot_dir / "riemann_raw.png"),
            "log": str(plot_dir / "riemann_log.png"),
            "normalized": str(plot_dir / "riemann_normalized.png"),
            "winsorized": str(plot_dir / "riemann_winsorized.png"),
        },
    }

    comparison_csv = output_dir / "comparison" / "curves.csv"
    functional_minima: dict[str, float] = {}
    if comparison_csv.exists():
        by_functional: dict[str, list[tuple[float, float]]] = {}
        with comparison_csv.open(newline="") as f:
            for row in csv.DictReader(f):
                if row.get("experiment") != "riemann_sweep":
                    continue
                try:
                    name = row["functional_name"]
                    x_value = float(row["x_value"])
                    score = float(row["score"])
                except (TypeError, ValueError, KeyError):
                    continue
                if math.isfinite(x_value) and math.isfinite(score):
                    by_functional.setdefault(name, []).append((x_value, score))
        for name, pairs in by_functional.items():
            arr = np.asarray(pairs, dtype=float)
            if arr.size == 0:
                continue
            best_idx = int(np.argmin(arr[:, 1]))
            functional_minima[name] = float(arr[best_idx, 0])
    report["functional_minimizers"] = functional_minima

    (diag_dir / "riemann_diagnostics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (diag_dir / "riemann_diagnostics.md").write_text(
        "\n".join(
            [
                "# Riemann Diagnostics",
                "",
                f"- Raw minimizer eps: `{raw_min_eps:.6f}`",
                f"- Raw minimizer value: `{raw_min_val:.6f}`",
                f"- Symmetry max abs diff: `{symmetry_max_diff:.3e}`" if symmetry_max_diff is not None else "- Symmetry max abs diff: `n/a`",
                f"- Raw median: `{float(np.median(vals)):.6f}`",
                f"- Raw p95: `{float(np.quantile(vals, 0.95)):.6f}`",
                f"- Raw p99: `{float(np.quantile(vals, 0.99)):.6f}`",
                f"- Normalized minimizer eps: `{float(eps[int(np.argmin(norm))]):.6f}`",
                f"- Winsorized minimizer eps: `{float(eps[int(np.argmin(wins))]):.6f}`",
                "",
                "## Functional Minimizers",
            ]
            + [
                f"- `{name}` -> `{value:.6f}`"
                for name, value in sorted(functional_minima.items())
            ]
            + [
                "",
                "## Interpretation",
                "",
                "The raw curve is dominated by singular spikes from the zero set on the critical line. Normalization and winsorization are for diagnosis only and are not used for verdicts.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return report
