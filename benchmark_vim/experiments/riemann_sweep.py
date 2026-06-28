from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import mpmath as mp

from ..analysis import local_minimum_near_zero
from ..results import ResultTable


def _xi(s: complex) -> complex:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def _xi_ratio(s: complex) -> complex:
    value = _xi(s)
    return mp.diff(_xi, s) / value if value != 0 else mp.mpc("inf")


def _window_integral(eps: float, t_min: float, t_max: float, samples: int) -> float:
    ts = np.linspace(t_min, t_max, samples)
    vals = []
    for t in ts:
        s = mp.mpc(0.5 + eps, t)
        ratio = _xi_ratio(s)
        vals.append(float(abs(ratio) ** 2))
    return float(np.trapezoid(vals, ts))


def run_riemann_sweep(output_dir: Path) -> ResultTable:
    eps_values = np.linspace(-0.2, 0.2, 41)
    rows: list[dict[str, float | str]] = []
    for eps in eps_values:
        i2 = _window_integral(float(eps), 0.0, 20.0, 120)
        rows.append({"experiment": "riemann_sweep", "eps": float(eps), "I2": i2})

    plot_path = output_dir / "plots" / "riemann_sweep.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    frame = np.array([[r["eps"], r["I2"]] for r in rows], dtype=float)
    plt.figure(figsize=(8, 5))
    plt.plot(frame[:, 0], frame[:, 1])
    plt.axvline(0.0, color="red", linestyle="--", linewidth=1)
    plt.xlabel("eps")
    plt.ylabel("I2(eps)")
    plt.title("Riemann Critical-Line Sweep")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    plt.close()

    verdict = local_minimum_near_zero(frame[:, 0], frame[:, 1])
    rows.append({"experiment": "riemann_sweep_verdict", "eps": float("nan"), "I2": float("nan"), "passed": verdict.passed, "reason": verdict.reason})

    return ResultTable(name="riemann_sweep", rows=rows)
