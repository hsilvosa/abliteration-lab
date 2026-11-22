"""Filesystem locations used across the project."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "configs"
DATA_DIR = REPO_ROOT / "data" / "raw"
RESULTS_DIR = REPO_ROOT / "results"

DEFAULT_MODELS_DIR = Path(r"D:\models")


def models_dir() -> Path:
    """Root for model weights. Override with the ABL_MODELS_DIR environment variable."""
    return Path(os.environ.get("ABL_MODELS_DIR", str(DEFAULT_MODELS_DIR)))


def model_dir(group: str, model_id: str) -> Path:
    return models_dir() / group / model_id


def own_models_dir() -> Path:
    """Where our own abliterated checkpoints are written."""
    return models_dir() / "own"
