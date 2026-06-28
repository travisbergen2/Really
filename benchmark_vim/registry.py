from __future__ import annotations

from collections.abc import Mapping

from .functional import (
    CandidateFunctional,
    default_functional,
    entropy_plus_resolution,
    resolution_cost,
    spectral_entropy,
    symmetry_pair_penalty,
)


def candidate_functionals() -> dict[str, CandidateFunctional]:
    registry = {
        "entropy_spread_minus_concentration": default_functional(),
        "spectral_entropy": CandidateFunctional("spectral_entropy", spectral_entropy),
        "resolution_cost": CandidateFunctional("resolution_cost", resolution_cost),
        "symmetry_pair_penalty": CandidateFunctional("symmetry_pair_penalty", symmetry_pair_penalty),
        "entropy_plus_resolution": CandidateFunctional("entropy_plus_resolution", entropy_plus_resolution),
    }
    return registry


def get_candidate_functional(name: str) -> CandidateFunctional:
    registry = candidate_functionals()
    if name not in registry:
        raise KeyError(f"Unknown candidate functional: {name}")
    return registry[name]

