# VIM Benchmark Executive Summary

## Single-Functional Verdicts

| Functional | Pass count | Fail count | Passed experiments | Failed experiments |
| --- | --- | --- | --- | --- |
| resolution_cost | 3 | 1 | offline_pair_test, sanity_check, synthetic_spectrum | riemann_sweep |
| symmetry_pair_penalty | 3 | 1 | offline_pair_test, sanity_check, synthetic_spectrum | riemann_sweep |
| entropy_plus_resolution | 2 | 2 | sanity_check, synthetic_spectrum | offline_pair_test, riemann_sweep |
| entropy_spread_minus_concentration | 2 | 2 | sanity_check, synthetic_spectrum | offline_pair_test, riemann_sweep |
| spectral_entropy | 2 | 2 | riemann_sweep, synthetic_spectrum | offline_pair_test, sanity_check |

## Composite Grid Verdicts

| a | b | c | pass_count | failed_experiments |
| --- | --- | --- | --- | --- |
| 0.0 | 0.0 | 1.0 | 3 | riemann_sweep |
| 0.0 | 0.25 | 0.75 | 3 | riemann_sweep |
| 0.0 | 0.5 | 0.5 | 3 | riemann_sweep |
| 0.0 | 0.75 | 0.25 | 3 | riemann_sweep |
| 0.0 | 1.0 | 0.0 | 3 | riemann_sweep |

## Riemann-Family Comparison

Recommendation: use symmetry-mismatch benchmarks for VIM, preserve raw Xi'/Xi benchmark as a negative control

| Variant | Objective | Minimum eps | Pass/fail |
| --- | --- | --- | --- |
| riemann_sweep | singularity-based | -0.200000 | FAIL |
| riemann_principal_value | regularized-singularity | -0.200000 | FAIL |
| riemann_regularized_log | regularized-singularity | -0.200000 | FAIL |
| riemann_zero_attraction | attraction-based | 0.000000 | PASS |
| riemann_logxi_symmetry_mismatch | symmetry-mismatch-based | 0.000000 | PASS |
| riemann_zero_density_symmetry_mismatch | symmetry-mismatch-based | 0.000000 | PASS |
| riemann_receiver_width_cost | symmetry-mismatch-based | 0.000000 | PASS |

## Best Candidate Families

- Best single functional: `resolution_cost` with `3/4` passes.
- Best composite grid candidate: `a=0.0, b=0.0, c=1.0` with `3/4` passes.
- Best Riemann family for symmetry-minimality: `riemann_logxi_symmetry_mismatch`, `riemann_zero_density_symmetry_mismatch`, and `riemann_receiver_width_cost`.

## Known Failures

- resolution_cost: riemann_sweep
- symmetry_pair_penalty: riemann_sweep
- entropy_plus_resolution: offline_pair_test, riemann_sweep
- entropy_spread_minus_concentration: offline_pair_test, riemann_sweep
- spectral_entropy: offline_pair_test, sanity_check

## Next Experiments

- Refine the symmetry-mismatch family with a wider t-window and multiple sigma/width settings.
- Run a finer coefficient grid around the current best composite candidates.
- Add a held-out benchmark set to test whether the best candidates generalize beyond the current four tasks.
- Preserve raw Xi'/Xi as a negative control and continue using symmetry-mismatch benchmarks for VIM.

## Conclusion

The benchmark stack currently favors symmetry-mismatch objectives for Riemann-style testing, while the raw `Xi'/Xi` family remains the correct negative control.
