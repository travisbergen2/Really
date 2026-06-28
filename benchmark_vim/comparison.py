from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from .analysis import Verdict
from .functional import CandidateFunctional
from .presets import ComparisonPreset
from .results import ResultTable


@dataclass(frozen=True)
class ComparisonSummary:
    experiment: str
    functional_name: str
    minimizer: float
    expected_minimizer: float
    pass_fail: str
    reason: str


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


def run_comparative_benchmark(
    output_dir: Path,
    presets: dict[str, ComparisonPreset],
    functionals: dict[str, CandidateFunctional],
) -> tuple[ResultTable, ResultTable]:
    comparison_rows: list[dict[str, object]] = []
    curve_rows: list[dict[str, object]] = []

    comparison_dir = output_dir / "comparison"
    plot_dir = output_dir / "plots" / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    for experiment, preset in presets.items():
        x_values = preset.sweep_values
        y_series_by_functional: dict[str, np.ndarray] = {}

        for functional_name, functional in functionals.items():
            y_values = []
            for x in x_values:
                series = preset.series_builder(float(x))
                y_values.append(functional.score(series))
                curve_rows.append(
                    {
                        "experiment": experiment,
                        "functional_name": functional_name,
                        "x_value": float(x),
                        "score": float(y_values[-1]),
                    }
                )
            arr_y = np.asarray(y_values, dtype=float)
            y_series_by_functional[functional_name] = arr_y
            verdict = _evaluate_minimizer(x_values, arr_y, preset.expected_minimizer)
            comparison_rows.append(
                {
                    "experiment": experiment,
                    "functional_name": functional_name,
                    "minimizer": float(x_values[int(np.argmin(arr_y))]),
                    "expected_minimizer": float(preset.expected_minimizer),
                    "pass_fail": "PASS" if verdict.passed else "FAIL",
                    "reason": verdict.reason,
                }
            )

        plt.figure(figsize=(8, 5))
        for functional_name, arr_y in y_series_by_functional.items():
            plt.plot(x_values, arr_y, label=functional_name)
        plt.axvline(preset.expected_minimizer, color="black", linestyle="--", linewidth=1, label="expected minimizer")
        plt.xlabel(preset.x_label)
        plt.ylabel("Functional score")
        plt.title(f"Comparison: {experiment}")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(plot_dir / f"{experiment}.png", dpi=160)
        plt.close()

    summary_table = ResultTable(name="comparison_summary", rows=comparison_rows)
    curve_table = ResultTable(name="comparison_curves", rows=curve_rows)
    summary_table.to_csv(comparison_dir / "summary.csv")
    summary_table.to_json(comparison_dir / "summary.json")
    curve_table.to_csv(comparison_dir / "curves.csv")
    curve_table.to_json(comparison_dir / "curves.json")
    return summary_table, curve_table

