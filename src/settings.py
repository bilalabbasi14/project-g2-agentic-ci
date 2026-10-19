"""Loads config.yaml (or the file named by the G2_CONFIG environment variable)."""
import os
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config.yaml"


def load_config(path=None):
    path = Path(path or os.environ.get("G2_CONFIG") or DEFAULT_CONFIG)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def repo_path(rel):
    """Resolve a repo-relative path from the config."""
    p = Path(rel)
    return p if p.is_absolute() else REPO_ROOT / p
