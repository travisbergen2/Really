# ⚠️ Superseded / Split — this repo is frozen

This repository has been split (2026-07-01, RPCS-1 consolidation). Its two halves now live at:

| What | Where it went |
|---|---|
| **Product** — translation layer, routing, persona/memory, MCP | [rpcs1-sdk](https://github.com/travisbergen2/rpcs1-sdk) (live at [rpcs1.dev](https://rpcs1.dev)). The Python `translator_hub/` here was ported — via the rpcs1-hub TS prototype — into `@rpcs1/core` and has since been improved (receiver-profile awareness, naming fixes). Nothing in `translator_hub/`, `api/`, or `web/` is current. |
| **Research** — `benchmark_vim/` + `outputs/` + `scripts/` | [imm-vim-benchmark](https://github.com/travisbergen2/imm-vim-benchmark) — verbatim copy, every text file sha256-verified byte-identical. Plot PNGs remain only here (the transfer path was not binary-safe) and are regenerable via `python -m benchmark_vim.cli`. |

No further development happens here. Original README preserved below.

---

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

The translation layer is a multi-module product with versioned manifest, routing logic, persistent memory/persona data, and an MCP transport layer.

### Features

- **Multi-Model Routing**: Intelligently route requests based on task type and audience.
- **Memory & Personas**: Persistent storage for observations and unique AI personality vectors.
- **MCP Support**: Real Model Context Protocol transport for tool registration and discovery.
- **Next.js Web UI**: A modern interface for interacting with the hub.
- **Vercel Ready**: Optimized for deployment on Vercel with Python serverless functions.

### Run

- Demo CLI:
  ```bash
  python -m translator_hub.server manifest
  python -m translator_hub.server interpret "your message here"
  ```

- MCP stdio server:
  ```bash
  python -m translator_hub.server serve
  ```

- Next.js Web UI (Local):
  ```bash
  cd web && npm install && npm run dev
  ```

### Integrated SDK

The `rpcs1-sdk` is integrated into this repository for direct access to RPCS-1 core functionalities.

