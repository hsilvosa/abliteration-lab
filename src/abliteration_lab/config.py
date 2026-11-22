"""Load and validate the TOML registries in configs/."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .paths import CONFIG_DIR, model_dir

GROUPS = ("core", "extended", "small", "source")
ROLES = ("abliterated", "baseline", "source")
FORMATS = ("gguf", "hf")


@dataclass(frozen=True)
class ModelSpec:
    id: str
    group: str
    role: str
    format: str
    repo: str
    files: tuple[str, ...]
    optional: tuple[str, ...] = ()
    baseline: str | None = None
    quant: str | None = None
    size_gb: float = 0.0
    license: str = ""
    method: str = ""
    card_claims: str = ""
    moe: bool = False

    @property
    def local_dir(self) -> Path:
        return model_dir(self.group, self.id)

    @property
    def main_file(self) -> Path:
        """Path of the primary GGUF file (first entry of `files`)."""
        if self.format != "gguf":
            raise ValueError(f"{self.id} is not a GGUF model")
        return self.local_dir / self.files[0]


@dataclass(frozen=True)
class DatasetSpec:
    id: str
    repo: str
    files: tuple[str, ...]
    text_column: str
    purpose: str = ""


@dataclass
class Registry:
    models: list[ModelSpec] = field(default_factory=list)

    def by_id(self, model_id: str) -> ModelSpec:
        for m in self.models:
            if m.id == model_id:
                return m
        raise KeyError(f"unknown model id: {model_id}")

    def select(self, groups: list[str] | None = None, ids: list[str] | None = None) -> list[ModelSpec]:
        out = self.models
        if groups:
            out = [m for m in out if m.group in groups]
        if ids:
            missing = set(ids) - {m.id for m in self.models}
            if missing:
                raise KeyError(f"unknown model ids: {sorted(missing)}")
            out = [m for m in out if m.id in ids]
        return out


def _read(path: Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def load_registry(path: Path | None = None) -> Registry:
    raw = _read(path or CONFIG_DIR / "models.toml")
    models = []
    for entry in raw.get("models", []):
        entry = dict(entry)
        entry["files"] = tuple(entry["files"])
        entry["optional"] = tuple(entry.get("optional", ()))
        models.append(ModelSpec(**entry))
    reg = Registry(models)
    validate_registry(reg)
    return reg


def validate_registry(reg: Registry) -> None:
    ids = [m.id for m in reg.models]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate model ids: {sorted(dupes)}")
    for m in reg.models:
        if m.group not in GROUPS:
            raise ValueError(f"{m.id}: bad group {m.group!r}")
        if m.role not in ROLES:
            raise ValueError(f"{m.id}: bad role {m.role!r}")
        if m.format not in FORMATS:
            raise ValueError(f"{m.id}: bad format {m.format!r}")
        if not m.files:
            raise ValueError(f"{m.id}: no files listed")
        if m.baseline is not None:
            base = reg.by_id(m.baseline)
            if base.role != "baseline":
                raise ValueError(f"{m.id}: baseline {m.baseline} has role {base.role}")


def load_datasets(path: Path | None = None) -> list[DatasetSpec]:
    raw = _read(path or CONFIG_DIR / "datasets.toml")
    return [DatasetSpec(**{**d, "files": tuple(d["files"])}) for d in raw.get("datasets", [])]


def load_toml(name: str) -> dict[str, Any]:
    """Load configs/<name>.toml, merged with configs/<name>.local.toml when present."""
    base = _read(CONFIG_DIR / f"{name}.toml")
    local = CONFIG_DIR / f"{name}.local.toml"
    if local.exists():
        base = _deep_merge(base, _read(local))
    return base


def _deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out
