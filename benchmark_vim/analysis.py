from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Verdict:
    passed: bool
    reason: str


def _index_of_nearest(values: Sequence[float], target: float = 0.0) -> int:
    arr = np.asarray(values, dtype=float)
    return int(np.argmin(np.abs(arr - target)))


def local_minimum_near_zero(xs: Sequence[float], ys: Sequence[float]) -> Verdict:
    arr_x = np.asarray(xs, dtype=float)
    arr_y = np.asarray(ys, dtype=float)
    if arr_x.size == 0 or arr_y.size == 0 or arr_x.size != arr_y.size:
        return Verdict(False, "invalid input")
    idx = _index_of_nearest(arr_x, 0.0)
    left = arr_y[max(0, idx - 3) : idx]
    right = arr_y[idx + 1 : idx + 4]
    center = arr_y[idx]
    neighborhood = np.concatenate([left, right])
    if neighborhood.size == 0:
        return Verdict(False, "insufficient data")
    if center <= float(np.min(neighborhood)) + 1e-12:
        return Verdict(True, "zero is a local minimum")
    best_idx = int(np.argmin(arr_y))
    return Verdict(False, f"minimum shifted to eps={arr_x[best_idx]:.6f}")


def prefers_zero_gap(deltas: Sequence[float], massless_scores: Sequence[float], gapped_scores: Sequence[float]) -> Verdict:
    arr_d = np.asarray(deltas, dtype=float)
    arr_m = np.asarray(massless_scores, dtype=float)
    arr_g = np.asarray(gapped_scores, dtype=float)
    if arr_d.size == 0 or arr_d.size != arr_m.size or arr_d.size != arr_g.size:
        return Verdict(False, "invalid input")
    best_gap_idx = int(np.argmin(arr_g))
    if abs(arr_d[best_gap_idx]) < 1e-12:
        return Verdict(True, "gap minimum occurs at zero")
    return Verdict(False, f"gap minimum occurs at delta={arr_d[best_gap_idx]:.6f}")


def displacement_increases_cost(deltas: Sequence[float], costs: Sequence[float]) -> Verdict:
    arr_d = np.asarray(deltas, dtype=float)
    arr_c = np.asarray(costs, dtype=float)
    if arr_d.size == 0 or arr_d.size != arr_c.size:
        return Verdict(False, "invalid input")
    idx0 = _index_of_nearest(arr_d, 0.0)
    if arr_c[idx0] <= float(np.min(arr_c)) + 1e-12:
        return Verdict(True, "zero displacement is minimal")
    best_idx = int(np.argmin(arr_c))
    return Verdict(False, f"minimum shifted to eps={arr_d[best_idx]:.6f}")
