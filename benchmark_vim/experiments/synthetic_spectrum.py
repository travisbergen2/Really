from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..functional import CandidateFunctional, geometric_cost, discrete_entropy, compression_cost
from ..analysis import prefers_zero_gap
from ..results import ResultTable


def _massless_spectrum(n: int = 64, scale: float = 1.0) -> np.ndarray:
    k = np.arange(1, n + 1, dtype=float)
    return scale / k


def _gapped_spectrum(delta: float, n: int = 64, scale: float = 1.0) -> np.ndarray:
    k = np.arange(0, n, dtype=float)
    return delta + scale * (k + 1.0)


def run_synthetic_spectrum(functional: CandidateFunctional, output_dir: Path) -> ResultTable:
    csv_rows: list[dict[str, float | str]] = []
    deltas = np.linspace(0.0, 3.0, 31)

    massless_scores = []
    gapped_scores = []
    for delta in deltas:
        gap = _gapped_spectrum(delta)
        massless = _massless_spectrum()
        massless_score = functional.score(massless)
        gapped_score = functional.score(gap)
        massless_scores.append(massless_score)
        gapped_scores.append(gapped_score)

        csv_rows.append(
            {
                "experiment": "synthetic_spectrum",
                "delta": float(delta),
                "massless_score": massless_score,
                "gapped_score": gapped_score,
                "massless_entropy": discrete_entropy(massless),
                "gapped_entropy": discrete_entropy(gap),
                "massless_geom_cost": geometric_cost(massless),
                "gapped_geom_cost": geometric_cost(gap),
                "massless_compression_cost": compression_cost(massless),
                "gapped_compression_cost": compression_cost(gap),
            }
        )

    plot_path = output_dir / "plots" / "synthetic_spectrum.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    frame = np.array([[r["delta"], r["massless_score"], r["gapped_score"]] for r in csv_rows], dtype=float)

    plt.figure(figsize=(8, 5))
    plt.plot(frame[:, 0], frame[:, 1], label="massless")
    plt.plot(frame[:, 0], frame[:, 2], label="gapped")
    plt.xlabel("Delta")
    plt.ylabel("Functional score")
    plt.title("Synthetic Massless vs Gapped Spectrum")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    plt.close()

    verdict = prefers_zero_gap(deltas, massless_scores, gapped_scores)
    csv_rows.append(
        {
            "experiment": "synthetic_spectrum_verdict",
            "delta": float("nan"),
            "massless_score": float("nan"),
            "gapped_score": float("nan"),
            "massless_entropy": float("nan"),
            "gapped_entropy": float("nan"),
            "massless_geom_cost": float("nan"),
            "gapped_geom_cost": float("nan"),
            "massless_compression_cost": float("nan"),
            "gapped_compression_cost": float("nan"),
            "passed": verdict.passed,
            "reason": verdict.reason,
        }
    )

    return ResultTable(name="synthetic_spectrum", rows=csv_rows)
