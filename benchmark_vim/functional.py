from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np


@dataclass(frozen=True)
class CandidateFunctional:
    """Callable wrapper for candidate information functionals."""

    name: str
    score_fn: Callable[[Iterable[float]], float]

    def score(self, values: Iterable[float]) -> float:
        return float(self.score_fn(values))


def default_functional() -> CandidateFunctional:
    return CandidateFunctional(name="entropy_spread_minus_concentration", score_fn=_entropy_spread_minus_concentration)


def _as_finite_abs_array(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    return np.abs(arr)


def _entropy(arr: np.ndarray) -> float:
    if arr.size == 0:
        return 0.0
    total = arr.sum()
    if total == 0:
        return 0.0
    p = arr / total
    mask = p > 0
    return -float(np.sum(p[mask] * np.log(p[mask])))


def _resolution(arr: np.ndarray) -> float:
    if arr.size == 0:
        return 0.0
    if arr.size == 1:
        return float(np.abs(arr[0]))
    return float(np.sum(np.abs(np.diff(np.sort(arr)))))


def _symmetry_penalty(arr: np.ndarray) -> float:
    if arr.size < 2:
        return float(np.abs(arr).sum())
    sorted_arr = np.sort(arr)
    half = sorted_arr.size // 2
    if half == 0:
        return float(np.abs(sorted_arr).sum())
    left = sorted_arr[:half]
    right = sorted_arr[-half:][::-1]
    return float(np.mean(np.abs(left - right)))


def _entropy_spread_minus_concentration(values: Iterable[float]) -> float:
    arr = _as_finite_abs_array(values)
    if arr.size == 0:
        return 0.0
    total = arr.sum()
    if total == 0:
        return 0.0
    p = arr / total
    entropy = _entropy(arr)
    concentration = float(np.sum(p**2))
    spread = float(np.var(arr))
    return entropy + spread - concentration


def spectral_entropy(values: Iterable[float]) -> float:
    return _entropy(_as_finite_abs_array(values))


def resolution_cost(values: Iterable[float]) -> float:
    arr = _as_finite_abs_array(values)
    return _resolution(arr) + float(np.sqrt(np.mean(np.square(arr - np.mean(arr))))) if arr.size else 0.0


def symmetry_pair_penalty(values: Iterable[float]) -> float:
    return _symmetry_penalty(_as_finite_abs_array(values))


def entropy_plus_resolution(values: Iterable[float]) -> float:
    arr = _as_finite_abs_array(values)
    return _entropy(arr) + _resolution(arr)


def composite_score(values: Iterable[float], a: float, b: float, c: float) -> float:
    arr = _as_finite_abs_array(values)
    return (
        a * spectral_entropy(arr)
        + b * resolution_cost(arr)
        + c * symmetry_pair_penalty(arr)
    )


def make_composite_functional(a: float, b: float, c: float) -> CandidateFunctional:
    name = f"composite_a{a:.3f}_b{b:.3f}_c{c:.3f}"
    return CandidateFunctional(name=name, score_fn=lambda values: composite_score(values, a, b, c))


def discrete_entropy(values: Iterable[float]) -> float:
    return _entropy(_as_finite_abs_array(values))


def geometric_cost(values: Iterable[float]) -> float:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(arr - np.mean(arr)))))


def compression_cost(values: Iterable[float]) -> float:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return 0.0
    return float(np.sum(np.abs(np.diff(arr)))) if arr.size > 1 else float(np.abs(arr[0]))
