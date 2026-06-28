from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
from collections import defaultdict


@dataclass(frozen=True)
class FunctionalScorecard:
    functional_name: str
    pass_count: int
    fail_count: int
    passed_experiments: list[str]
    failed_experiments: list[str]


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _load_comparison_scorecards(output_dir: Path) -> list[FunctionalScorecard]:
    rows = _load_csv_rows(output_dir / "comparison" / "summary.csv")
    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"pass": [], "fail": []})
    for row in rows:
        name = row["functional_name"]
        experiment = row["experiment"]
        if row["pass_fail"] == "PASS":
            grouped[name]["pass"].append(experiment)
        else:
            grouped[name]["fail"].append(experiment)
    scorecards = []
    for name, buckets in grouped.items():
        scorecards.append(
            FunctionalScorecard(
                functional_name=name,
                pass_count=len(buckets["pass"]),
                fail_count=len(buckets["fail"]),
                passed_experiments=sorted(buckets["pass"]),
                failed_experiments=sorted(buckets["fail"]),
            )
        )
    scorecards.sort(key=lambda r: (-r.pass_count, r.fail_count, r.functional_name))
    return scorecards


def _load_grid_rows(output_dir: Path) -> list[dict[str, str]]:
    return _load_csv_rows(output_dir / "grid" / "leaderboard.csv")


def _load_riemann_family_report(output_dir: Path) -> dict[str, object]:
    return json.loads((output_dir / "reports" / "riemann_family_comparison.json").read_text())


def build_executive_summary(output_dir: Path) -> Path:
    report_dir = output_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    scorecards = _load_comparison_scorecards(output_dir)
    grid_rows = _load_grid_rows(output_dir)
    riemann_report = _load_riemann_family_report(output_dir)

    best_single = scorecards[0] if scorecards else None
    best_grid = grid_rows[0] if grid_rows else None
    riemann_variants = riemann_report.get("variants", [])

    known_failures = []
    for card in scorecards:
        if card.failed_experiments:
            known_failures.append(f"{card.functional_name}: {', '.join(card.failed_experiments)}")

    next_experiments = [
        "Refine the symmetry-mismatch family with a wider t-window and multiple sigma/width settings.",
        "Run a finer coefficient grid around the current best composite candidates.",
        "Add a held-out benchmark set to test whether the best candidates generalize beyond the current four tasks.",
        "Preserve raw Xi'/Xi as a negative control and continue using symmetry-mismatch benchmarks for VIM.",
    ]

    md_lines = [
        "# VIM Benchmark Executive Summary",
        "",
        "## Single-Functional Verdicts",
        "",
        "| Functional | Pass count | Fail count | Passed experiments | Failed experiments |",
        "| --- | --- | --- | --- | --- |",
    ]
    for card in scorecards:
        md_lines.append(
            f"| {card.functional_name} | {card.pass_count} | {card.fail_count} | {', '.join(card.passed_experiments)} | {', '.join(card.failed_experiments)} |"
        )

    md_lines.extend(
        [
            "",
            "## Composite Grid Verdicts",
            "",
            "| a | b | c | pass_count | failed_experiments |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in grid_rows[:5]:
        md_lines.append(
            f"| {row['a']} | {row['b']} | {row['c']} | {row['pass_count']} | {row['failed_experiments']} |"
        )

    md_lines.extend(
        [
            "",
            "## Riemann-Family Comparison",
            "",
            f"Recommendation: {riemann_report.get('recommendation', '')}",
            "",
            "| Variant | Objective | Minimum eps | Pass/fail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for variant in riemann_variants:
        md_lines.append(
            f"| {variant['name']} | {variant['objective_type']} | {variant['minimum_eps']:.6f} | {variant['pass_fail']} |"
        )

    md_lines.extend(
        [
            "",
            "## Best Candidate Families",
            "",
        ]
    )
    if best_single:
        md_lines.append(
            f"- Best single functional: `{best_single.functional_name}` with `{best_single.pass_count}/4` passes."
        )
    if best_grid:
        md_lines.append(
            f"- Best composite grid candidate: `a={best_grid['a']}, b={best_grid['b']}, c={best_grid['c']}` with `{best_grid['pass_count']}/4` passes."
        )
    md_lines.extend(
        [
            "- Best Riemann family for symmetry-minimality: `riemann_logxi_symmetry_mismatch`, `riemann_zero_density_symmetry_mismatch`, and `riemann_receiver_width_cost`.",
            "",
            "## Known Failures",
            "",
        ]
    )
    if known_failures:
        for item in known_failures:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("- None recorded.")

    md_lines.extend(
        [
            "",
            "## Next Experiments",
            "",
        ]
    )
    for item in next_experiments:
        md_lines.append(f"- {item}")

    md_lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "The benchmark stack currently favors symmetry-mismatch objectives for Riemann-style testing, while the raw `Xi'/Xi` family remains the correct negative control.",
        ]
    )

    md_path = report_dir / "vim_benchmark_executive_summary.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    json_path = report_dir / "vim_benchmark_executive_summary.json"
    json_path.write_text(
        json.dumps(
            {
                "single_functional_verdicts": [
                    {
                        "functional_name": card.functional_name,
                        "pass_count": card.pass_count,
                        "fail_count": card.fail_count,
                        "passed_experiments": card.passed_experiments,
                        "failed_experiments": card.failed_experiments,
                    }
                    for card in scorecards
                ],
                "composite_grid_verdicts": grid_rows[:5],
                "riemann_family_comparison": riemann_report,
                "best_candidate_families": {
                    "best_single_functional": scorecards[0].functional_name if scorecards else None,
                    "best_grid_candidate": grid_rows[0] if grid_rows else None,
                    "best_riemann_family": [
                        "riemann_logxi_symmetry_mismatch",
                        "riemann_zero_density_symmetry_mismatch",
                        "riemann_receiver_width_cost",
                    ],
                },
                "known_failures": known_failures,
                "next_experiments": next_experiments,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return md_path

