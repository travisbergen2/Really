from __future__ import annotations

from typing import Any

PROVIDER_CAPABILITIES = {
    "openai": {
        "roles": ["general reasoning", "intent extraction", "synthesis", "multi-step planning"],
        "strengths": ["ambiguity resolution", "balanced reasoning", "structured output"],
        "tradeoffs": ["can be verbose"],
    },
    "anthropic": {
        "roles": ["technical drafting", "careful analysis", "long-form precision"],
        "strengths": ["rigor", "thoroughness", "exact wording"],
        "tradeoffs": ["higher cost for heavy usage"],
    },
    "google": {
        "roles": ["fast broad knowledge", "concise code help", "triage"],
        "strengths": ["speed", "brevity", "book-smart recall"],
        "tradeoffs": ["may under-elaborate nuanced intent"],
    },
    "grok": {
        "roles": ["marketing", "public-facing phrasing", "social compression"],
        "strengths": ["punchy tone", "public positioning", "short-form clarity"],
        "tradeoffs": ["less ideal for rigorous formal drafting"],
    },
    "local": {
        "roles": ["private drafts", "offline fallback", "low-cost bulk work"],
        "strengths": ["privacy", "cost control", "air-gapped use"],
        "tradeoffs": ["quality depends on installed model"],
    },
}

ROLE_ORDER = {
    "interpretation": ["openai", "anthropic", "google"],
    "technical": ["anthropic", "openai", "google"],
    "analysis": ["anthropic", "openai", "google"],
    "code": ["anthropic", "google", "openai"],
    "marketing": ["grok", "openai", "google"],
    "social": ["grok", "openai", "anthropic"],
    "concise": ["google", "grok", "openai"],
    "memory": ["openai", "anthropic", "local"],
    "persona": ["openai", "grok", "anthropic"],
    "default": ["openai", "anthropic", "google", "grok", "local"],
}


def _normalize_role(task_type: str | None) -> str:
    if not task_type:
        return "default"
    normalized = task_type.strip().lower().replace("-", "_")
    aliases = {
        "reasoning": "interpretation",
        "intent": "interpretation",
        "writing": "technical",
        "research": "analysis",
        "planning": "analysis",
        "style": "persona",
    }
    return aliases.get(normalized, normalized if normalized in ROLE_ORDER else "default")


def route_to_model(
    task_type: str,
    objective: str | None = None,
    target_audience: str = "plain",
    latency_priority: str = "balanced",
    cost_priority: str = "balanced",
    allow_multi_model: bool = False,
) -> dict[str, Any]:
    role = _normalize_role(task_type)
    candidates = list(ROLE_ORDER.get(role, ROLE_ORDER["default"]))

    if target_audience in {"technical", "detailed"} and "anthropic" in candidates:
        candidates = ["anthropic"] + [model for model in candidates if model != "anthropic"]
    elif target_audience in {"concise", "plain"} and "google" in candidates:
        candidates = ["google"] + [model for model in candidates if model != "google"]

    if latency_priority == "high":
        fast_models = ["google", "grok", "local"]
        ordered = [model for model in fast_models if model in candidates]
        ordered.extend(model for model in candidates if model not in ordered)
        candidates = ordered
    elif cost_priority == "high":
        cheap_models = ["local", "google", "openai", "anthropic", "grok"]
        ordered = [model for model in cheap_models if model in candidates]
        ordered.extend(model for model in candidates if model not in ordered)
        candidates = ordered

    primary_model = candidates[0]
    fallback_models = candidates[1:3]
    explanation = [
        f"task_type={task_type}",
        f"target_audience={target_audience}",
        f"primary={primary_model}",
    ]
    if objective:
        explanation.append(f"objective={objective}")

    suggested_roles = PROVIDER_CAPABILITIES[primary_model]["roles"]

    return {
        "primary_model": primary_model,
        "fallback_models": fallback_models,
        "allow_multi_model": allow_multi_model,
        "suggested_roles": suggested_roles,
        "provider_notes": PROVIDER_CAPABILITIES[primary_model],
        "routing_reason": "; ".join(explanation),
    }

