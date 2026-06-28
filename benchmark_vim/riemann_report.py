from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class RiemannVariantSummary:
    name: str
    objective_type: str
    minimum_eps: float
    pass_fail: str
    interpretation: str


def _load_variant(csv_path: Path, json_path: Path, value_column: str = "I") -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    eps = []
    vals = []
    with csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("experiment", "").endswith("_verdict"):
                continue
            try:
                e = float(row["eps"])
                v = float(row[value_column])
            except (TypeError, ValueError, KeyError):
                continue
            if math.isfinite(e) and math.isfinite(v):
                eps.append(e)
                vals.append(v)
    data = json.loads(json_path.read_text())
    verdicts = [r for r in data["rows"] if r.get("experiment", "").endswith("_verdict")]
    verdict = verdicts[0] if verdicts else {}
    return np.asarray(eps, dtype=float), np.asarray(vals, dtype=float), verdict


def _normalize(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values
    lo = float(np.min(values))
    hi = float(np.max(values))
    if hi <= lo:
        return np.zeros_like(values)
    return (values - lo) / (hi - lo)


def _min_eps(eps: np.ndarray, vals: np.ndarray) -> float:
    if eps.size == 0 or vals.size == 0:
        return float("nan")
    return float(eps[int(np.argmin(vals))])


def _objective_type(name: str) -> str:
    if name == "riemann_sweep":
        return "singularity-based"
    if name in {"riemann_principal_value", "riemann_regularized_log"}:
        return "regularized-singularity"
    if name == "riemann_zero_attraction":
        return "attraction-based"
    return "symmetry-mismatch-based"


def _interpretation(name: str, objective_type: str, minimum_eps: float, pass_fail: str) -> str:
    if name == "riemann_sweep":
        return "Negative control: raw singular ratio remains edge-biased and is dominated by zero-line spikes."
    if objective_type == "regularized-singularity":
        return "Reduces or caps pole influence, but still tracks the edge in this implementation."
    if objective_type == "attraction-based":
        return "Passes by construction for critical-line attraction, but it is a different objective from symmetry-minimality."
    if objective_type == "symmetry-mismatch-based":
        if pass_fail == "PASS":
            return "Best match for a symmetry-minimality test without rewarding singularity avoidance."
        return "Symmetry-aware in design, but did not minimize as expected."
    return "Unclassified variant."


def build_riemann_family_report(output_dir: Path) -> Path:
    variants = [
        ("riemann_sweep", "csv/riemann_sweep.csv", "json/riemann_sweep.json", "I2"),
        ("riemann_principal_value", "csv/riemann_principal_value.csv", "json/riemann_principal_value.json", "I"),
        ("riemann_regularized_log", "csv/riemann_regularized_log.csv", "json/riemann_regularized_log.json", "I"),
        ("riemann_zero_attraction", "csv/riemann_zero_attraction.csv", "json/riemann_zero_attraction.json", "I"),
        ("riemann_logxi_symmetry_mismatch", "csv/riemann_logxi_symmetry_mismatch.csv", "json/riemann_logxi_symmetry_mismatch.json", "I"),
        ("riemann_zero_density_symmetry_mismatch", "csv/riemann_zero_density_symmetry_mismatch.csv", "json/riemann_zero_density_symmetry_mismatch.json", "I"),
        ("riemann_receiver_width_cost", "csv/riemann_receiver_width_cost.csv", "json/riemann_receiver_width_cost.json", "I"),
    ]

    summaries: list[RiemannVariantSummary] = []
    curve_data: list[tuple[str, str, np.ndarray, np.ndarray, np.ndarray]] = []

    for name, csv_rel, json_rel, value_column in variants:
        csv_path = output_dir / csv_rel
        json_path = output_dir / json_rel
        eps, vals, verdict = _load_variant(csv_path, json_path, value_column=value_column)
        objective_type = _objective_type(name)
        minimum_eps = _min_eps(eps, vals)
        pass_fail = "PASS" if verdict.get("passed") else "FAIL"
        interpretation = _interpretation(name, objective_type, minimum_eps, pass_fail)
        summaries.append(
            RiemannVariantSummary(
                name=name,
                objective_type=objective_type,
                minimum_eps=minimum_eps,
                pass_fail=pass_fail,
                interpretation=interpretation,
            )
        )
        curve_data.append((name, objective_type, eps, vals, _normalize(vals)))

    report_dir = output_dir / "reports"
    plot_dir = report_dir / "plots"
    report_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    # Combined plot: normalized curves on the same axes.
    plt.figure(figsize=(10, 6))
    colors = {
        "singularity-based": "#b91c1c",
        "regularized-singularity": "#d97706",
        "attraction-based": "#2563eb",
        "symmetry-mismatch-based": "#059669",
    }
    for name, objective_type, eps, vals, norm in curve_data:
        if eps.size == 0:
            continue
        plt.plot(eps, norm, label=f"{name} [{objective_type}]", color=colors.get(objective_type))
        min_idx = int(np.argmin(vals))
        plt.scatter([eps[min_idx]], [norm[min_idx]], color=colors.get(objective_type), s=35)
    plt.axvline(0.0, color="black", linestyle="--", linewidth=1, label="eps=0")
    plt.xlabel("eps")
    plt.ylabel("normalized cost")
    plt.title("Riemann Family Comparison")
    plt.legend(fontsize=7, loc="best")
    plt.tight_layout()
    plot_path = plot_dir / "riemann_family_comparison.png"
    plt.savefig(plot_path, dpi=170)
    plt.close()

    md_lines = [
        "# Riemann Family Comparison Report",
        "",
        "Recommendation: use symmetry-mismatch benchmarks for VIM, preserve raw `Xi'/Xi` as a negative control.",
        "",
        "## Table",
        "",
        "| Variant | Objective type | Minimum eps | Pass/fail | Interpretation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in summaries:
        md_lines.append(
            f"| {row.name} | {row.objective_type} | {row.minimum_eps:.6f} | {row.pass_fail} | {row.interpretation} |"
        )
    md_lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `singularity-based` variants measure or regularize the magnitude of `|Xi'/Xi|^2`.",
            "- `regularized-singularity` variants cap or exclude pole influence, but still remain tied to the singular ratio.",
            "- `attraction-based` variants reward proximity to the critical line and are useful as a constructive control.",
            "- `symmetry-mismatch-based` variants test symmetry-minimality without directly rewarding singularity avoidance.",
            "",
            f"Combined plot: `{plot_path}`",
            "",
        ]
    )

    report_path = report_dir / "riemann_family_comparison.md"
    report_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    json_path = report_dir / "riemann_family_comparison.json"
    json_path.write_text(
        json.dumps(
            {
                "recommendation": "use symmetry-mismatch benchmarks for VIM, preserve raw Xi'/Xi benchmark as a negative control",
                "variants": [row.__dict__ for row in summaries],
                "plot": str(plot_path),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return report_path
