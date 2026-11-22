from pathlib import Path

import pytest

from abliteration_lab.config import Registry, ModelSpec, load_datasets, load_registry, validate_registry


def test_registry_loads_and_pairs_resolve():
    reg = load_registry()
    assert reg.models
    for m in reg.models:
        if m.baseline:
            assert reg.by_id(m.baseline).role == "baseline"


def test_core_group_has_three_way_comparison():
    core = load_registry().select(groups=["core"])
    abliterated = [m for m in core if m.role == "abliterated"]
    assert len(abliterated) >= 3
    assert all(m.baseline for m in abliterated)


def test_models_land_under_models_dir(monkeypatch):
    monkeypatch.setenv("ABL_MODELS_DIR", "X:/somewhere")
    spec = load_registry().by_id("qwen3-14b-base")
    assert spec.main_file == Path("X:/somewhere") / "core" / "qwen3-14b-base" / "Qwen_Qwen3-14B-Q4_K_M.gguf"


def test_duplicate_ids_rejected():
    m = ModelSpec(id="a", group="core", role="baseline", format="gguf", repo="r", files=("f.gguf",))
    with pytest.raises(ValueError):
        validate_registry(Registry([m, m]))


def test_datasets_config():
    ids = {d.id for d in load_datasets()}
    assert {"harmful", "harmless", "xstest", "mmlu"} <= ids
