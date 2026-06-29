from dataclasses import dataclass

@dataclass
class ModelConfig:
    fast_model: str = "gpt-4o-mini"
    deliberate_model: str = "gpt-4o"

@dataclass
class HubConfig:
    models: ModelConfig = ModelConfig()
    memory_path: str = "translator_hub/data/memory.json"
    persona_path: str = "translator_hub/data/personas"
