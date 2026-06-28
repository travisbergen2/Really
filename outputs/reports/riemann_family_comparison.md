# Riemann Family Comparison Report

Recommendation: use symmetry-mismatch benchmarks for VIM, preserve raw `Xi'/Xi` as a negative control.

## Table

| Variant | Objective type | Minimum eps | Pass/fail | Interpretation |
| --- | --- | --- | --- | --- |
| riemann_sweep | singularity-based | -0.200000 | FAIL | Negative control: raw singular ratio remains edge-biased and is dominated by zero-line spikes. |
| riemann_principal_value | regularized-singularity | -0.200000 | FAIL | Reduces or caps pole influence, but still tracks the edge in this implementation. |
| riemann_regularized_log | regularized-singularity | -0.200000 | FAIL | Reduces or caps pole influence, but still tracks the edge in this implementation. |
| riemann_zero_attraction | attraction-based | 0.000000 | PASS | Passes by construction for critical-line attraction, but it is a different objective from symmetry-minimality. |
| riemann_logxi_symmetry_mismatch | symmetry-mismatch-based | 0.000000 | PASS | Best match for a symmetry-minimality test without rewarding singularity avoidance. |
| riemann_zero_density_symmetry_mismatch | symmetry-mismatch-based | 0.000000 | PASS | Best match for a symmetry-minimality test without rewarding singularity avoidance. |
| riemann_receiver_width_cost | symmetry-mismatch-based | 0.000000 | PASS | Best match for a symmetry-minimality test without rewarding singularity avoidance. |

## Notes

- `singularity-based` variants measure or regularize the magnitude of `|Xi'/Xi|^2`.
- `regularized-singularity` variants cap or exclude pole influence, but still remain tied to the singular ratio.
- `attraction-based` variants reward proximity to the critical line and are useful as a constructive control.
- `symmetry-mismatch-based` variants test symmetry-minimality without directly rewarding singularity avoidance.

Combined plot: `outputs/reports/plots/riemann_family_comparison.png`

