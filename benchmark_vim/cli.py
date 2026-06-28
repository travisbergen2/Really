from __future__ import annotations

import argparse
import json
from pathlib import Path

from .comparison import run_comparative_benchmark
from .grid_search import run_coefficient_grid
from .diagnostics import run_riemann_diagnostics
from .executive_summary import build_executive_summary
from .riemann_report import build_riemann_family_report
from .riemann_variants import (
    run_riemann_logxi_symmetry_mismatch,
    run_riemann_receiver_width_cost,
    run_riemann_principal_value,
    run_riemann_regularized_log,
    run_riemann_zero_attraction,
    run_riemann_zero_density_symmetry_mismatch,
)
from .experiments import (
    run_offline_pair_test,
    run_riemann_sweep,
    run_sanity_check,
    run_synthetic_spectrum,
)
from .registry import candidate_functionals
from .presets import comparison_presets
from .functional import default_functional


def _write_summary(output_dir: Path, summary: dict[str, object]) -> None:
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "json" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the VIM benchmark suite")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    functional = default_functional()
    summaries = []

    synthetic = run_synthetic_spectrum(functional, output_dir)
    synthetic.to_csv(output_dir / "csv" / "synthetic_spectrum.csv")
    synthetic.to_json(output_dir / "json" / "synthetic_spectrum.json")
    summaries.append({"name": synthetic.name, "rows": len(synthetic.rows)})

    riemann = run_riemann_sweep(output_dir)
    riemann.to_csv(output_dir / "csv" / "riemann_sweep.csv")
    riemann.to_json(output_dir / "json" / "riemann_sweep.json")
    summaries.append({"name": riemann.name, "rows": len(riemann.rows)})

    riemann_pv = run_riemann_principal_value(output_dir)
    riemann_pv.to_csv(output_dir / "csv" / "riemann_principal_value.csv")
    riemann_pv.to_json(output_dir / "json" / "riemann_principal_value.json")
    summaries.append({"name": riemann_pv.name, "rows": len(riemann_pv.rows)})

    riemann_zero = run_riemann_zero_attraction(output_dir)
    riemann_zero.to_csv(output_dir / "csv" / "riemann_zero_attraction.csv")
    riemann_zero.to_json(output_dir / "json" / "riemann_zero_attraction.json")
    summaries.append({"name": riemann_zero.name, "rows": len(riemann_zero.rows)})

    riemann_log = run_riemann_regularized_log(output_dir)
    riemann_log.to_csv(output_dir / "csv" / "riemann_regularized_log.csv")
    riemann_log.to_json(output_dir / "json" / "riemann_regularized_log.json")
    summaries.append({"name": riemann_log.name, "rows": len(riemann_log.rows)})

    riemann_logxi = run_riemann_logxi_symmetry_mismatch(output_dir)
    riemann_logxi.to_csv(output_dir / "csv" / "riemann_logxi_symmetry_mismatch.csv")
    riemann_logxi.to_json(output_dir / "json" / "riemann_logxi_symmetry_mismatch.json")
    summaries.append({"name": riemann_logxi.name, "rows": len(riemann_logxi.rows)})

    riemann_zero_density = run_riemann_zero_density_symmetry_mismatch(output_dir)
    riemann_zero_density.to_csv(output_dir / "csv" / "riemann_zero_density_symmetry_mismatch.csv")
    riemann_zero_density.to_json(output_dir / "json" / "riemann_zero_density_symmetry_mismatch.json")
    summaries.append({"name": riemann_zero_density.name, "rows": len(riemann_zero_density.rows)})

    riemann_receiver_width = run_riemann_receiver_width_cost(output_dir)
    riemann_receiver_width.to_csv(output_dir / "csv" / "riemann_receiver_width_cost.csv")
    riemann_receiver_width.to_json(output_dir / "json" / "riemann_receiver_width_cost.json")
    summaries.append({"name": riemann_receiver_width.name, "rows": len(riemann_receiver_width.rows)})

    pair = run_offline_pair_test(functional, output_dir)
    pair.to_csv(output_dir / "csv" / "offline_pair_test.csv")
    pair.to_json(output_dir / "json" / "offline_pair_test.json")
    summaries.append({"name": pair.name, "rows": len(pair.rows)})

    sanity = run_sanity_check(functional, output_dir)
    sanity.to_csv(output_dir / "csv" / "sanity_check.csv")
    sanity.to_json(output_dir / "json" / "sanity_check.json")
    summaries.append({"name": sanity.name, "rows": len(sanity.rows)})

    comparison_summary, comparison_curves = run_comparative_benchmark(
        output_dir,
        comparison_presets(),
        candidate_functionals(),
    )
    summaries.append({"name": comparison_summary.name, "rows": len(comparison_summary.rows)})
    summaries.append({"name": comparison_curves.name, "rows": len(comparison_curves.rows)})

    grid_summary = run_coefficient_grid(output_dir, comparison_presets())
    summaries.append({"name": grid_summary.name, "rows": len(grid_summary.rows)})

    riemann_diag = run_riemann_diagnostics(output_dir)
    summaries.append({"name": "riemann_diagnostics", "rows": 1})

    riemann_report = build_riemann_family_report(output_dir)
    summaries.append({"name": "riemann_family_comparison_report", "rows": 1})

    executive_summary = build_executive_summary(output_dir)
    summaries.append({"name": "vim_benchmark_executive_summary", "rows": 1})

    _write_summary(
        output_dir,
        {
            "functional": functional.name,
            "experiments": summaries,
            "comparison_functionals": list(candidate_functionals().keys()),
            "grid_step": 0.25,
            "riemann_diagnostics": riemann_diag,
            "riemann_variants": [
                "riemann_principal_value",
                "riemann_zero_attraction",
                "riemann_regularized_log",
                "riemann_logxi_symmetry_mismatch",
                "riemann_zero_density_symmetry_mismatch",
                "riemann_receiver_width_cost",
            ],
            "riemann_family_report": str(riemann_report),
            "executive_summary": str(executive_summary),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
