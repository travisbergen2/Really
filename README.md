# VIM Benchmark Engine

Local numerical falsification harness for candidate Information Complexity functionals `I(H)`.

Goal:
- Test whether a candidate functional prefers known minimal or stable configurations.
- Treat failure as useful data.
- Do not attempt to prove RH or Yang-Mills.

## What this repo contains

- `benchmark_vim/functional.py`: abstract functional interface plus a few toy score helpers
- `benchmark_vim/experiments/`: four experiment modules
- `benchmark_vim/cli.py`: runs the benchmark suite and writes CSV / JSON / plots
- `translator_hub/`: the AI-human translation layer, routing core, memory, persona packs, and MCP transport
- `outputs/`: generated artifacts

## Experiments

1. Synthetic Massless vs Gapped Spectrum
2. Riemann Critical-Line Sweep
3. Off-Line Synthetic Pair Test
4. Known-System Sanity Check

## Pass / Fail Criteria

The benchmark does not claim mathematical proof. It only reports whether a candidate functional behaves consistently with the expected minimum.

- Massless vs Gapped Spectrum
  - Pass if the score is minimized near `Delta = 0` when the candidate is supposed to prefer massless structure.
  - Fail if the score is strictly lower for a non-zero gap and the effect is stable under sweeps.
- Riemann Critical-Line Sweep
  - Pass if `eps = 0` is a local minimum for `I2(eps)` over the selected window.
  - Fail if the minimum is consistently displaced away from `eps = 0`.
- Off-Line Synthetic Pair Test
  - Pass if displacement increases information cost.
  - Fail if displacement decreases cost.
- Known-System Sanity Check
  - Pass if the same functional rewards compression/minimality in PCA / Fourier toy data.
  - Fail if it prefers inflated representations.

## Output layout

Generated results are written under:

- `outputs/csv/`
- `outputs/plots/`
- `outputs/json/`
- `outputs/comparison/`
- `outputs/grid/`
- `outputs/templates/`

## TestRail Import Template

Use the files in `outputs/templates/` when importing real benchmark outputs into TestRail.

- `outputs/templates/testrail_ai_eval_result_template.csv`
- `outputs/templates/testrail_ai_eval_result_template.md`

The template matches the current AI Evaluation configuration in this TestRail instance:

- `status_id`
- `comment`
- `quality_rating` as a JSON object with the configured categories

Keep the same quality categories across baseline and RPCS1 uploads. Do not invent new scoring dimensions per run.

## Comparative Mode

The benchmark engine can run multiple candidate `I(H)` functionals against the same experiment presets and report:

- the minimizer selected by each functional
- the expected minimizer for that experiment
- a pass/fail verdict based on whether they match
- a shared-axis comparison plot for visual inspection

Important:

- Failed candidates are evidence, not errors.
- A failure means the functional did not align with the benchmark objective for that experiment.
- The benchmark is designed to preserve and surface failures rather than hide them.

The coefficient-grid mode searches a single fixed composite functional across all four benchmarks:

```text
I = a * spectral_entropy + b * resolution_cost + c * symmetry_pair_penalty
```

The same coefficients are used everywhere. No experiment-specific tuning is applied.

## Riemann Variant Families

The Riemann benchmarks are organized into three objective families:

- `singularity-based`: raw `|Xi'/Xi|^2`, principal-value exclusion, regularized log
- `attraction-based`: zero-attraction
- `symmetry-mismatch-based`: logXi symmetry mismatch, zero-density symmetry mismatch, receiver-width cost

The symmetry-mismatch family is the preferred direction when the goal is to test symmetry-minimality without directly rewarding singular spikes.

## Run

```bash
python -m benchmark_vim.cli --output outputs
```

If `scipy` is not installed, the Riemann experiment falls back to `mpmath`-only numerics.

## Translator Hub

The translation layer is now a separate package in this repo and can be run in two ways:

- Demo CLI:

```bash
python -m translator_hub.server manifest
python -m translator_hub.server interpret "your message here"
python -m translator_hub.server route technical --objective "draft a spec"
```

- MCP stdio server:

```bash
python -m translator_hub.server serve
```

- Local browser UI:

```bash
python -m translator_hub.server web
```

Then open `http://127.0.0.1:8787`.

This code should live on GitHub once you want collaboration, versioned releases, or external integration. It is already structured like a reusable product module, so GitHub is the right home for it.
