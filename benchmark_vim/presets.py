from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np
import mpmath as mp


@dataclass(frozen=True)
class ComparisonPreset:
    name: str
    x_label: str
    expected_minimizer: float
    sweep_values: np.ndarray
    series_builder: Callable[[float], Iterable[float]]


def _massless_spectrum(n: int = 64, scale: float = 1.0) -> np.ndarray:
    k = np.arange(1, n + 1, dtype=float)
    return scale / k


def _gapped_spectrum(delta: float, n: int = 64, scale: float = 1.0) -> np.ndarray:
    k = np.arange(0, n, dtype=float)
    return delta + scale * (k + 1.0)


def _synthetic_zero_set(eps: float, count: int = 40) -> np.ndarray:
    k = np.arange(count, dtype=float)
    return np.concatenate([0.5 - eps - 1.0 / (k + 1.0), 0.5 + eps + 1.0 / (k + 1.0)])


def _pca_like_data(compression: float, n: int = 128) -> np.ndarray:
    x = np.linspace(0.0, 4.0 * np.pi, n)
    signal = np.sin(x) + 0.4 * np.sin(3 * x)
    noise = compression * np.cos(9 * x)
    return signal + noise


def _fourier_basis_data(scale: float, n: int = 128) -> np.ndarray:
    x = np.linspace(0.0, 2.0 * np.pi, n)
    return np.sin(x) + scale * np.sin(15 * x)


def _xi(s: complex) -> complex:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def _riemann_profile(eps: float, t_min: float = 0.0, t_max: float = 20.0, samples: int = 120) -> np.ndarray:
    ts = np.linspace(t_min, t_max, samples)
    vals = []
    for t in ts:
        s = mp.mpc(0.5 + eps, t)
        value = _xi(s)
        ratio = mp.diff(_xi, s) / value if value != 0 else mp.mpc("inf")
        vals.append(float(abs(ratio) ** 2))
    return np.asarray(vals, dtype=float)


def comparison_presets() -> dict[str, ComparisonPreset]:
    return {
        "synthetic_spectrum": ComparisonPreset(
            name="synthetic_spectrum",
            x_label="Delta",
            expected_minimizer=0.0,
            sweep_values=np.linspace(0.0, 3.0, 31),
            series_builder=lambda delta: _gapped_spectrum(float(delta)),
        ),
        "riemann_sweep": ComparisonPreset(
            name="riemann_sweep",
            x_label="eps",
            expected_minimizer=0.0,
            sweep_values=np.linspace(-0.2, 0.2, 41),
            series_builder=lambda eps: _riemann_profile(float(eps)),
        ),
        "offline_pair_test": ComparisonPreset(
            name="offline_pair_test",
            x_label="eps",
            expected_minimizer=0.0,
            sweep_values=np.linspace(0.0, 0.25, 26),
            series_builder=lambda eps: _synthetic_zero_set(float(eps)),
        ),
        "sanity_check": ComparisonPreset(
            name="sanity_check",
            x_label="scale",
            expected_minimizer=0.0,
            sweep_values=np.linspace(0.0, 1.0, 21),
            series_builder=lambda scale: np.concatenate([_pca_like_data(float(scale)), _fourier_basis_data(float(scale))]),
        ),
    }
