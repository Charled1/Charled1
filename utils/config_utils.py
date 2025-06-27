"""Simple YAML configuration loader."""

from dataclasses import dataclass
from typing import Any, Dict
import yaml


@dataclass
class ConfigManager:
    path: str = "config.yaml"

    def load(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
