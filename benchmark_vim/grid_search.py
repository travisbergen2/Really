from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import json
import matplotlib.pyplot as plt
import numpy as np

from .analysis import Verdict
from .functional import entropy_plus_resolution, resolution_cost, spectral_entropy, symmetry_pair_penalty
from .presets import ComparisonPreset
from .results import ResultTable


@dataclass(frozen=True)
class GridRow:
    a: float
    b: float
    c: float
    pass_count: int
    failed_experiments: str


def coefficient_grid(step: float = 0.25) -> list[tuple[float, float, float]]:
    if step <= 0:
        raise ValueError("step must be positive")
    steps = int(round(1.0 / step))
    if not np.isclose(steps * step, 1.0):
        raise ValueError("step must evenly divide 1.0")
    triples: list[tuple[float, float, float]] = []
    for i in range(steps + 1):
        for j in range(steps + 1 - i):
            k = steps - i - j
            a = i * step
            b = j * step
            c = k * step
            triples.append((float(a), float(b), float(c)))
    return triples


def _evaluate_minimizer(xs: Iterable[float], ys: Iterable[float], expected_minimizer: float, tol: float = 1e-12) -> Verdict:
    arr_x = np.asarray(list(xs), dtype=float)
    arr_y = np.asarray(list(ys), dtype=float)
    if arr_x.size == 0 or arr_x.size != arr_y.size:
        return Verdict(False, "invalid comparison input")
    idx = int(np.argmin(arr_y))
    minimizer = float(arr_x[idx])
    if abs(minimizer - expected_minimizer) <= tol:
        return Verdict(True, f"minimizer at {minimizer:.6f}")
    return Verdict(False, f"minimizer at {minimizer:.6f}, expected {expected_minimizer:.6f}")


def _default_failed_experiments(per_experiment: dict[str, bool]) -> str:
    failed = [name for name, passed in per_experiment.items() if not passed]
    return ";".join(failed) if failed else ""


def run_coefficient_grid(
    output_dir: Path,
    presets: dict[str, ComparisonPreset],
    step: float = 0.25,
) -> ResultTable:
    rows: list[dict[str, object]] = []
    markdown_lines: list[str] = []
    all_pass_rows: list[dict[str, object]] = []

    grid_dir = output_dir / "grid"
    plot_dir = output_dir / "plots" / "grid"
    grid_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    cached_base_scores: dict[str, dict[str, np.ndarray]] = {}

    for a, b, c in coefficient_grid(step):
        per_experiment_pass: dict[str, bool] = {}
        per_experiment_minimizer: dict[str, float] = {}
        per_experiment_reason: dict[str, str] = {}

        for experiment, preset in presets.items():
            xs = preset.sweep_values
            if experiment not in cached_base_scores:
                base_scores = {
                    "spectral_entropy": [],
                    "resolution_cost": [],
                    "symmetry_pair_penalty": [],
                }
                for x in xs:
                    series = preset.series_builder(float(x))
                    base_scores["spectral_entropy"].append(float(spectral_entropy(series)))
                    base_scores["resolution_cost"].append(float(resolution_cost(series)))
                    base_scores["symmetry_pair_penalty"].append(float(symmetry_pair_penalty(series)))
                cached_base_scores[experiment] = {k: np.asarray(v, dtype=float) for k, v in base_scores.items()}
            cached = cached_base_scores[experiment]
            arr_y = (
                a * cached["spectral_entropy"]
                + b * cached["resolution_cost"]
                + c * cached["symmetry_pair_penalty"]
            )
            idx = int(np.argmin(arr_y))
            minimizer = float(xs[idx])
            verdict = _evaluate_minimizer(xs, arr_y, preset.expected_minimizer)
            per_experiment_pass[experiment] = verdict.passed
            per_experiment_minimizer[experiment] = minimizer
            per_experiment_reason[experiment] = verdict.reason

        pass_count = sum(1 for passed in per_experiment_pass.values() if passed)
        failed_experiments = _default_failed_experiments(per_experiment_pass)
        row: dict[str, object] = {
            "a": a,
            "b": b,
            "c": c,
            "pass_count": pass_count,
            "failed_experiments": failed_experiments,
        }
        for experiment in presets:
            row[f"{experiment}_minimizer"] = per_experiment_minimizer[experiment]
            row[f"{experiment}_pass_fail"] = "PASS" if per_experiment_pass[experiment] else "FAIL"
            row[f"{experiment}_reason"] = per_experiment_reason[experiment]
        rows.append(row)

        if pass_count == len(presets):
            all_pass_rows.append(row)

    rows.sort(key=lambda r: (-int(r["pass_count"]), float(r["a"]), float(r["b"]), float(r["c"])))
    best_rows = rows[:5]

    summary_table = ResultTable(name="coefficient_grid_leaderboard", rows=rows)
    summary_table.to_csv(grid_dir / "leaderboard.csv")
    summary_table.to_json(grid_dir / "leaderboard.json")

    # Markdown export for quick scanning.
    md = ["# Coefficient Grid Leaderboard", ""]
    md.append(f"Grid step: `{step}`")
    md.append("")
    if all_pass_rows:
        md.append("## All-pass candidates")
        md.append("")
        for r in all_pass_rows:
            md.append(f"- `a={r['a']:.3f}`, `b={r['b']:.3f}`, `c={r['c']:.3f}`")
        md.append("")
    else:
        md.append("## All-pass candidates")
        md.append("")
        md.append("None found.")
        md.append("")
    md.append("## Best non-overfit candidates")
    md.append("")
    header = ["a", "b", "c", "pass_count", "failed_experiments"] + [f"{name}_minimizer" for name in presets]
    md.append("| " + " | ".join(header) + " |")
    md.append("| " + " | ".join(["---"] * len(header)) + " |")
    for r in best_rows:
        values = [
            f"{float(r['a']):.3f}",
            f"{float(r['b']):.3f}",
            f"{float(r['c']):.3f}",
            str(int(r["pass_count"])),
            str(r["failed_experiments"]),
        ] + [f"{float(r[f'{name}_minimizer']):.6f}" for name in presets]
        md.append("| " + " | ".join(values) + " |")
    (grid_dir / "leaderboard.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Simple plot of pass count across the simplex.
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    xs = [float(r["a"]) for r in rows]
    ys = [float(r["b"]) for r in rows]
    colors = [float(r["pass_count"]) for r in rows]
    sc = ax.scatter(xs, ys, c=colors, cmap="viridis", s=120, edgecolor="black")
    ax.set_xlabel("a")
    ax.set_ylabel("b")
    ax.set_title("Coefficient grid pass count")
    fig.colorbar(sc, ax=ax, label="pass_count")
    fig.tight_layout()
    fig.savefig(plot_dir / "pass_count_simplex.png", dpi=160)
    plt.close(fig)

    return summary_table
