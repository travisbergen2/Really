# TestRail Run Matrix

## Project Split

- `rpcs1.dev` is the website QA project.
- `rpcs1` is the AI benchmark project.
- RH and YM remain separate benchmark categories inside `rpcs1`.

## Naming Convention

- Website runs: `rpcs1.dev - <phase> - <date>`
- Benchmark plans: `RPCS1 Wave <n> - <comparison> - <date>`
- Benchmark runs:
  - `Baseline - GPT - <date>`
  - `RPCS1 - GPT - <date>`
  - future RH/YM runs should use the same date-stamped pattern

## Current Objects

### `rpcs1.dev`

- Project id: `3`
- Section ids:
  - `43` Smoke
  - `54` Landing Page
  - `55` Conversion Funnel
  - `56` Lead Capture
  - `57` Mobile UX
  - `58` Performance
  - `59` Accessibility
  - `60` SEO / Metadata
  - `61` Analytics / Tracking
  - `62` Regression
- Run id:
  - `24` `rpcs1.dev - first-pass QA - 2026-06-28`

### `rpcs1`

- Project id: `2`
- Milestone id:
  - `9` `RPCS1 Wave 2 - Comparative Benchmark`
- Plan id:
  - `21` `RPCS1 Wave 2 - Baseline vs RPCS1 - 2026-06-28`
- Runs:
  - `22` `Baseline - GPT - 2026-06-28`
  - `23` `RPCS1 - GPT - 2026-06-28`
- Benchmark sections:
  - `44` RPCS1 Core Reasoning
  - `45` RPCS1 Comparisons & Metrics
  - `46` RPCS1 Platform / Navigation
  - `47` RPCS1 Documentation / Search
  - `48` RPCS1 Responsive / Visual
  - `49` RPCS1 API / Integration
  - `50` RPCS1 Negative Controls
  - `51` RPCS1 Symmetry Mismatch
  - `52` RH Research
  - `53` YM Research

## Run Matrix Summary

| Track | Purpose | Container | Current Status |
|---|---|---:|---|
| `rpcs1.dev` | Website QA | Run `24` | First-pass results recorded |
| `rpcs1` | RPCS1 vs baseline benchmark | Plan `21` | Runs created, no results yet |

## Separation Rule

- Do not mix website QA results into the benchmark project.
- Do not mix RH/YM research cases into the website project.
- Keep raw controls and symmetry-mismatch tests in the benchmark project only.
