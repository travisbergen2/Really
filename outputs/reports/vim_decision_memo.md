# VIM Decision Memo

## What Was Tested

The benchmark engine evaluated candidate Information Complexity objectives across four core tasks:

- Synthetic massless vs gapped spectrum
- Riemann critical-line sweep
- Off-line synthetic pair test
- Known-system sanity check

It also compared a family of Riemann variants, including:

- Raw `|Xi'/Xi|^2`
- Principal-value and log-regularized singularity variants
- Zero-attraction variants
- Symmetry-mismatch variants

## What Passed

- `resolution_cost` and `symmetry_pair_penalty` each passed 3 of 4 core benchmarks.
- Several composite coefficients reached 3 of 4 passes, but none reached 4 of 4.
- The Riemann symmetry-mismatch variants passed cleanly with `eps = 0`.

## What Failed

- No single candidate objective passed all four core benchmarks.
- The raw Riemann benchmark and the singularity-regularized Riemann variants remained edge-biased.
- The off-line pair test and the Riemann sweep were the main failure drivers for most non-Riemann objectives.

## What the Failures Mean

The failures do not show that VIM is invalid. They show that the current candidate objectives are not yet a single robust objective across all benchmarks.

The Riemann results are especially informative:

- Raw `|Xi'/Xi|^2` is dominated by singular spikes near known zeros.
- Regularizing or excluding poles reduces the singularity but does not by itself produce a symmetry-minimal objective.
- The symmetry-mismatch formulations behave more cleanly and are better aligned with the intended test.

The benchmark engine can now discriminate between candidate objectives rather than producing undifferentiated scores.

## Best Current Candidate Objective Family

The best current Riemann family for VIM-style testing is the symmetry-mismatch family:

- `riemann_logxi_symmetry_mismatch`
- `riemann_zero_density_symmetry_mismatch`
- `riemann_receiver_width_cost`

These variants minimize at `eps = 0` without relying on raw singularity magnitude.

## Why Raw `Xi'/Xi` Is Kept as a Negative Control

The raw `|Xi'/Xi|^2` benchmark is useful as a negative control because it exposes a failure mode:

- it is strongly affected by singularity blow-up at known zeros
- it remains edge-biased after simple regularization
- it is a valid comparison baseline, but not a good primary objective for symmetry-minimality testing

Keeping it ensures the benchmark can detect when a candidate objective is just avoiding poles rather than expressing the intended structure.

## Next Recommended Experiment

Run a finer symmetry-mismatch study with:

- a wider `t` window
- multiple smoothing widths
- held-out zero sets or perturbed zero-density fields

That is the best next step for testing whether the symmetry-mismatch family generalizes, while preserving the raw Riemann benchmark as a negative control.

