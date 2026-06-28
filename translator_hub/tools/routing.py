from __future__ import annotations

from typing import Any

from ..router import route_to_model as _route_to_model


def route_to_model(
    task_type: str,
    objective: str | None = None,
    target_audience: str = "plain",
    latency_priority: str = "balanced",
    cost_priority: str = "balanced",
    allow_multi_model: bool = False,
) -> dict[str, Any]:
    return _route_to_model(
        task_type=task_type,
        objective=objective,
        target_audience=target_audience,
        latency_priority=latency_priority,
        cost_priority=cost_priority,
        allow_multi_model=allow_multi_model,
    )
