from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import json
import numpy as np
import pandas as pd


@dataclass
class ResultTable:
    name: str
    rows: list[dict[str, Any]]

    def to_csv(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(self.rows).to_csv(path, index=False)

    def to_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        def _default(obj: Any) -> Any:
            if isinstance(obj, (np.floating, np.integer)):
                return obj.item()
            if isinstance(obj, np.bool_):
                return bool(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        path.write_text(json.dumps({"name": self.name, "rows": self.rows}, indent=2, default=_default), encoding="utf-8")
