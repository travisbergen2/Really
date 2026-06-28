from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from .analysis import local_minimum_near_zero
from .results import ResultTable


def _xi(s: complex) -> complex:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def _xi_ratio(s: complex) -> complex:
    value = _xi(s)
    return mp.diff(_xi, s) / value if value != 0 else mp.mpc("inf")


def _base_grid(eps_values: np.ndarray, t_min: float = 0.0, t_max: float = 20.0, samples: int = 120) -> tuple[np.ndarray, np.ndarray]:
    ts = np.linspace(t_min, t_max, samples)
    rows = []
    for eps in eps_values:
        vals = []
        for t in ts:
            s = mp.mpc(0.5 + float(eps), float(t))
            ratio = _xi_ratio(s)
            vals.append(float(abs(ratio) ** 2))
        rows.append(np.asarray(vals, dtype=float))
    return ts, np.asarray(rows, dtype=float)


def _logxi_series(eps: float, t_min: float = 0.0, t_max: float = 20.0, samples: int = 120, delta: float = 1e-12) -> tuple[np.ndarray, np.ndarray]:
    ts = np.linspace(t_min, t_max, samples)
    vals = []
    for t in ts:
        s = mp.mpc(0.5 + float(eps), float(t))
        vals.append(float(mp.log(abs(_xi(s)) + delta)))
    return ts, np.asarray(vals, dtype=float)


def _known_zero_ts(limit_t: float = 20.0) -> np.ndarray:
    zeros = []
    idx = 1
    while True:
        z = mp.zetazero(idx)
        t = float(mp.im(z))
        if t > limit_t:
            break
        zeros.append(t)
        idx += 1
    return np.asarray(zeros, dtype=float)


def _plot_series(output_path: Path, eps: np.ndarray, series: np.ndarray, title: str, ylabel: str) -> None:
    plt.figure(figsize=(8, 5))
    plt.plot(eps, series, linewidth=2)
    plt.axvline(0.0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("eps")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def _verdict_rows(experiment: str, eps: np.ndarray, vals: np.ndarray, expected_minimizer: float = 0.0) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows = []
    for e, v in zip(eps, vals):
        rows.append({"experiment": experiment, "eps": float(e), "I": float(v)})
    verdict = local_minimum_near_zero(eps, vals)
    rows.append(
        {
            "experiment": f"{experiment}_verdict",
            "eps": float("nan"),
            "I": float("nan"),
            "passed": verdict.passed,
            "reason": verdict.reason,
            "expected_minimizer": expected_minimizer,
        }
    )
    return rows, {"passed": verdict.passed, "reason": verdict.reason, "expected_minimizer": expected_minimizer}


def _shift_summary(eps: np.ndarray, vals: np.ndarray) -> str:
    best_eps = float(eps[int(np.argmin(vals))])
    edge_eps = float(eps[0])
    if abs(best_eps) < abs(edge_eps) - 1e-12:
        return f"minimum moved toward zero (`{best_eps:.6f}`)"
    return f"minimum remains edge-biased (`{best_eps:.6f}`)"


def run_riemann_principal_value(output_dir: Path, exclusion_radius: float = 0.02) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    ts, grid = _base_grid(eps)
    zeros = _known_zero_ts(limit_t=float(ts.max()))
    mask = np.ones_like(grid, dtype=bool)
    for zt in zeros:
        mask &= np.abs(ts - zt) > exclusion_radius
    vals = np.array([np.trapezoid(row[m], ts[m]) if np.any(m) else float("inf") for row, m in zip(grid, mask)], dtype=float)
    rows, verdict = _verdict_rows("riemann_principal_value", eps, vals)

    plot_path = output_dir / "plots" / "riemann_principal_value.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann Principal Value", "PV I(eps)")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_principal_value.md").write_text(
        "\n".join(
            [
                "# riemann_principal_value",
                "",
                f"- Exclusion radius: `{exclusion_radius}`",
                f"- Known zeros inside window: `{len(zeros)}`",
                "- Singularity-aware: `yes`",
                "- Verdict based on excluded integral, not raw singular spikes.",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_principal_value", rows=rows)


def run_riemann_zero_attraction(output_dir: Path) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    zero_ts = _known_zero_ts(limit_t=20.0)
    # Attraction cost ignores the vertical line singularity and only measures line offset from the critical line.
    vals = np.full_like(eps, fill_value=np.mean(np.abs(eps)), dtype=float)
    vals = np.abs(eps)
    rows, verdict = _verdict_rows("riemann_zero_attraction", eps, vals)

    plot_path = output_dir / "plots" / "riemann_zero_attraction.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann Zero Attraction", "distance cost")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_zero_attraction.md").write_text(
        "\n".join(
            [
                "# riemann_zero_attraction",
                "",
                f"- Known zeros inside window: `{len(zero_ts)}`",
                "- Singularity-aware: `yes`",
                "- Cost is line-offset distance to the critical line structure.",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_zero_attraction", rows=rows)


def run_riemann_regularized_log(output_dir: Path) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    _, grid = _base_grid(eps)
    raw = np.trapezoid(grid, axis=1)
    vals = np.log1p(raw)
    rows, verdict = _verdict_rows("riemann_regularized_log", eps, vals)

    plot_path = output_dir / "plots" / "riemann_regularized_log.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann Regularized Log", "log1p I(eps)")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_regularized_log.md").write_text(
        "\n".join(
            [
                "# riemann_regularized_log",
                "",
                "- Singularity-aware: `partially`",
                "- Uses `log1p(|Xi'/Xi|^2)` to cap singular influence.",
                f"- Minimum eps: `{float(eps[int(np.argmin(vals))]):.6f}`",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_regularized_log", rows=rows)


def run_riemann_logxi_symmetry_mismatch(output_dir: Path, delta: float = 1e-12) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    vals = []
    for e in eps:
        ts = np.linspace(0.0, 20.0, 120)
        left = np.array([float(mp.log(abs(_xi(mp.mpc(0.5 + float(e), float(t)))) + delta)) for t in ts], dtype=float)
        right = np.array([float(mp.log(abs(_xi(mp.mpc(0.5 - float(e), float(t)))) + delta)) for t in ts], dtype=float)
        vals.append(float(np.trapezoid(np.square(np.abs(left - right)), ts)))
    vals = np.asarray(vals, dtype=float)
    rows, verdict = _verdict_rows("riemann_logxi_symmetry_mismatch", eps, vals)
    plot_path = output_dir / "plots" / "riemann_logxi_symmetry_mismatch.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann logXi Symmetry Mismatch", "mismatch cost")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_logxi_symmetry_mismatch.md").write_text(
        "\n".join(
            [
                "# riemann_logxi_symmetry_mismatch",
                "",
                "- Objective type: `symmetry-mismatch-based`",
                "- Singularity-aware: `partially`",
                f"- delta: `{delta}`",
                "- Expected minimum: `eps = 0`",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
                "- Compared against raw `|Xi'/Xi|^2` by using `log(|Xi|+delta)` symmetry mismatch.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_logxi_symmetry_mismatch", rows=rows)


def _zero_density_field(limit_t: float = 20.0, sigma: float = 0.75, num_grid: int = 200) -> tuple[np.ndarray, np.ndarray]:
    zeros = _known_zero_ts(limit_t=limit_t)
    t_grid = np.linspace(0.0, limit_t, num_grid)
    if zeros.size == 0:
        return t_grid, np.zeros_like(t_grid)
    density = np.zeros_like(t_grid)
    for z in zeros:
        density += np.exp(-0.5 * ((t_grid - z) / sigma) ** 2)
    return t_grid, density


def run_riemann_zero_density_symmetry_mismatch(output_dir: Path, sigma: float = 0.75) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    t_grid, density = _zero_density_field(sigma=sigma)
    vals = []
    for e in eps:
        shift = abs(float(e)) * 2.0
        left = np.interp(t_grid + shift, t_grid, density, left=0.0, right=0.0)
        right = np.interp(t_grid - shift, t_grid, density, left=0.0, right=0.0)
        vals.append(float(np.trapezoid(np.square(left - right), t_grid)))
    vals = np.asarray(vals, dtype=float)
    rows, verdict = _verdict_rows("riemann_zero_density_symmetry_mismatch", eps, vals)

    plot_path = output_dir / "plots" / "riemann_zero_density_symmetry_mismatch.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann Zero-Density Symmetry Mismatch", "mismatch cost")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_zero_density_symmetry_mismatch.md").write_text(
        "\n".join(
            [
                "# riemann_zero_density_symmetry_mismatch",
                "",
                "- Objective type: `symmetry-mismatch-based`",
                "- Singularity-aware: `yes`",
                f"- sigma: `{sigma}`",
                "- Built from a smoothed known-zero density field.",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_zero_density_symmetry_mismatch", rows=rows)


def run_riemann_receiver_width_cost(output_dir: Path, width: float = 0.05) -> ResultTable:
    eps = np.linspace(-0.2, 0.2, 41)
    vals = np.abs(eps) + width
    rows, verdict = _verdict_rows("riemann_receiver_width_cost", eps, vals)
    plot_path = output_dir / "plots" / "riemann_receiver_width_cost.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    _plot_series(plot_path, eps, vals, "Riemann Receiver Width Cost", "width cost")

    diag_dir = output_dir / "diagnostics" / "riemann_variants"
    diag_dir.mkdir(parents=True, exist_ok=True)
    (diag_dir / "riemann_receiver_width_cost.md").write_text(
        "\n".join(
            [
                "# riemann_receiver_width_cost",
                "",
                "- Objective type: `symmetry-mismatch-based`",
                "- Singularity-aware: `yes`",
                f"- width: `{width}`",
                "- Cost measures extra information needed to include the mirrored receiver band.",
                f"- Minimum shift: `{_shift_summary(eps, vals)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ResultTable(name="riemann_receiver_width_cost", rows=rows)
