from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..analysis import displacement_increases_cost
from ..functional import CandidateFunctional
from ..results import ResultTable


def _synthetic_zero_set(eps: float, count: int = 40) -> np.ndarray:
    k = np.arange(count, dtype=float)
    return np.concatenate([0.5 - eps - 1.0 / (k + 1.0), 0.5 + eps + 1.0 / (k + 1.0)])


def run_offline_pair_test(functional: CandidateFunctional, output_dir: Path) -> ResultTable:
    eps_values = np.linspace(0.0, 0.25, 26)
    rows: list[dict[str, float | str]] = []
    for eps in eps_values:
        zs = _synthetic_zero_set(float(eps))
        rows.append(
            {
                "experiment": "offline_pair_test",
                "eps": float(eps),
                "cost": functional.score(zs),
            }
        )

    plot_path = output_dir / "plots" / "offline_pair_test.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    frame = np.array([[r["eps"], r["cost"]] for r in rows], dtype=float)
    plt.figure(figsize=(8, 5))
    plt.plot(frame[:, 0], frame[:, 1])
    plt.xlabel("eps")
    plt.ylabel("Information cost")
    plt.title("Off-Line Synthetic Pair Test")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    plt.close()

    verdict = displacement_increases_cost(frame[:, 0], frame[:, 1])
    rows.append({"experiment": "offline_pair_test_verdict", "eps": float("nan"), "cost": float("nan"), "passed": verdict.passed, "reason": verdict.reason})

    return ResultTable(name="offline_pair_test", rows=rows)
