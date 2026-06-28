# TestRail AI Evaluation Import Template

Use this template to upload real benchmark outputs into the `rpcs1` AI Evaluation runs.

## Required shape

The current TestRail instance expects:

- `status_id`
- `comment`
- `quality_rating` as a JSON object

The `quality_rating` object must include these categories, because they are configured on this instance:

- `response_consistency`
- `functional_correctness`
- `actionability`
- `factual_accuracy`
- `reasoning_coherence`
- `relevance_to_user_intent`

## CSV columns

- `case_id`: TestRail case id
- `status_id`: usually `2` for blocked scaffold rows or `1` / `5` for final pass/fail results
- `comment`: evaluator notes
- `quality_rating`: JSON object string
- `custom_ai_input`: prompt or task input
- `custom_ai_output`: model output
- `custom_ai_traces`: trace URL or artifact link
- `custom_ai_latency`: latency in seconds or milliseconds, as a string
- `defects`: optional defect ids

## Example row

```csv
case_id,status_id,comment,quality_rating,custom_ai_input,custom_ai_output,custom_ai_traces,custom_ai_latency,defects
107,2,Replace with actual scoring,"{"response_consistency":3,"functional_correctness":3,"actionability":3,"factual_accuracy":3,"reasoning_coherence":3,"relevance_to_user_intent":3}",prompt here,output here,https://trace.example/run/1,1.24,
```

## Upload rule

Keep the same quality categories across baseline and RPCS1. Do not invent new rating dimensions per run.
