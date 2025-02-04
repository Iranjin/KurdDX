from __future__ import annotations

import json
import os
from typing import Any


class Config:
    def __init__(self, path: str, indent: int = 4):
        self.path = path
        self.indent = indent
        self.config: dict[str, Any] | None = None

    def load(self) -> Config:
        if not os.path.exists(self.path):
            e = FileNotFoundError(f"Config file not found: {self.path}")
            e.filename = os.path.basename(self.path)
            e.filename2 = self.path
            raise e
        with open(self.path, "r") as f:
            self.config = json.load(f)
        return self

    def save(self) -> Config:
        if self.config is None:
            raise ValueError("Config is not loaded")
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=self.indent)
        return self

    def get(self, key: str, default: Any = None) -> Any:
        if self.config is None:
            raise ValueError("Config is not loaded")
        if key not in self.config:
            return default
        return self.config[key]

    def set(self, key: str, value: Any) -> Config:
        if self.config is None:
            raise ValueError("Config is not loaded")
        self.config[key] = value
        self.save()
        return self

    def remove(self, key: str) -> Config:
        if self.config is None:
            raise ValueError("Config is not loaded")
        if key not in self.config:
            raise KeyError(f"Key '{key}' not found")
        del self.config[key]
        self.save()
        return self

    def exists(self, key: str) -> bool:
        if self.config is None:
            raise ValueError("Config is not loaded")
        return key in self.config

    def __getitem__(self, key: str) -> Any:
        return self.get(key, raise_error=True)

    def __setitem__(self, key: str, value: Any):
        self.set(key, value)

    def __delitem__(self, key: str):
        self.remove(key)

    def __contains__(self, key: str) -> bool:
        return self.exists(key)

    def __iter__(self):
        if self.config is None:
            raise ValueError("Config is not loaded")
        return iter(self.config)

    def __len__(self) -> int:
        if self.config is None:
            raise ValueError("Config is not loaded")
        return len(self.config)
