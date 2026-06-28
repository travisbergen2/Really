from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..functional import CandidateFunctional
from ..analysis import Verdict
from ..results import ResultTable


def _pca_like_data(compression: float, n: int = 128) -> np.ndarray:
    x = np.linspace(0.0, 4.0 * np.pi, n)
    signal = np.sin(x) + 0.4 * np.sin(3 * x)
    noise = compression * np.cos(9 * x)
    return signal + noise


def _fourier_basis_data(scale: float, n: int = 128) -> np.ndarray:
    x = np.linspace(0.0, 2.0 * np.pi, n)
    return np.sin(x) + scale * np.sin(15 * x)


def run_sanity_check(functional: CandidateFunctional, output_dir: Path) -> ResultTable:
    rows: list[dict[str, float | str]] = []
    scales = np.linspace(0.0, 1.0, 21)
    for s in scales:
        pca_data = _pca_like_data(float(s))
        fourier_data = _fourier_basis_data(float(s))
        rows.append(
            {
                "experiment": "sanity_check",
                "scale": float(s),
                "pca_cost": functional.score(pca_data),
                "fourier_cost": functional.score(fourier_data),
            }
        )

    plot_path = output_dir / "plots" / "sanity_check.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    frame = np.array([[r["scale"], r["pca_cost"], r["fourier_cost"]] for r in rows], dtype=float)
    plt.figure(figsize=(8, 5))
    plt.plot(frame[:, 0], frame[:, 1], label="pca-like")
    plt.plot(frame[:, 0], frame[:, 2], label="fourier-like")
    plt.xlabel("scale")
    plt.ylabel("Functional score")
    plt.title("Known-System Sanity Check")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    plt.close()

    pca_start = frame[0, 1]
    pca_end = frame[-1, 1]
    fourier_start = frame[0, 2]
    fourier_end = frame[-1, 2]
    passed = pca_end <= pca_start and fourier_end <= fourier_start
    verdict = Verdict(passed, "cost falls as compression increases" if passed else "cost does not consistently fall with compression")
    rows.append({"experiment": "sanity_check_verdict", "scale": float("nan"), "pca_cost": float("nan"), "fourier_cost": float("nan"), "passed": verdict.passed, "reason": verdict.reason})

    return ResultTable(name="sanity_check", rows=rows)
