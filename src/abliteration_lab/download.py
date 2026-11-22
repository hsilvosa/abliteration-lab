"""Download model weights and datasets from the Hugging Face Hub.

Design:
- dry run by default: prints the plan, sizes and free disk space; `--yes` downloads;
- files that already exist with the expected size are skipped;
- each model directory gets a `manifest.json` with repo, revision, file sizes and
  the LFS sha256 reported by the Hub, so `--verify` can check integrity later;
- no identity is sent: only the optional HF_TOKEN from the environment.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import DatasetSpec, ModelSpec
from .paths import DATA_DIR, models_dir

GB = 1e9
SAFETY_MARGIN_GB = 20.0


@dataclass
class RemoteFile:
    name: str
    size: int
    sha256: str | None


def _api():
    from huggingface_hub import HfApi

    return HfApi(token=os.environ.get("HF_TOKEN") or None)


def remote_files(spec: ModelSpec, with_optional: bool) -> tuple[str, list[RemoteFile]]:
    """Resolve the files to fetch for `spec` and return (revision sha, files)."""
    info = _api().model_info(spec.repo, files_metadata=True)
    siblings = {s.rfilename: s for s in info.siblings or []}
    wanted = list(spec.files) + (list(spec.optional) if with_optional else [])
    names: list[str] = []
    if spec.format == "gguf":
        missing = [w for w in wanted if w not in siblings]
        if missing:
            raise FileNotFoundError(f"{spec.repo}: files not found on the Hub: {missing}")
        names = wanted
    else:
        names = [n for n in siblings if any(fnmatch.fnmatch(n, p) for p in wanted)]
        if not any(n.endswith(".safetensors") for n in names):
            raise FileNotFoundError(f"{spec.repo}: no safetensors match {wanted}")
    out = []
    for n in sorted(names):
        s = siblings[n]
        sha = s.lfs.sha256 if getattr(s, "lfs", None) else None
        out.append(RemoteFile(n, int(s.size or 0), sha))
    return info.sha, out


def free_gb(path: Path) -> float:
    probe = path
    while not probe.exists():
        probe = probe.parent
    return shutil.disk_usage(probe).free / GB


def _is_complete(path: Path, size: int) -> bool:
    return path.exists() and (size == 0 or path.stat().st_size == size)


def plan(specs: list[ModelSpec], with_optional: bool) -> list[tuple[ModelSpec, str, list[RemoteFile]]]:
    return [(s, *remote_files(s, with_optional)) for s in specs]


def print_plan(items: list[tuple[ModelSpec, str, list[RemoteFile]]]) -> float:
    root = models_dir()
    todo_bytes = 0
    print(f"Models dir: {root}")
    for spec, rev, files in items:
        print(f"\n[{spec.group}] {spec.id}  ({spec.repo} @ {rev[:10]})")
        for f in files:
            dest = spec.local_dir / f.name
            done = _is_complete(dest, f.size)
            todo_bytes += 0 if done else f.size
            state = "present" if done else "to download"
            print(f"  {f.size / GB:7.2f} GB  {f.name}  [{state}]")
    need = todo_bytes / GB
    free = free_gb(root)
    print(f"\nTo download: {need:.2f} GB | free on target: {free:.1f} GB | margin kept: {SAFETY_MARGIN_GB:.0f} GB")
    return need


def download_models(specs: list[ModelSpec], with_optional: bool = False, yes: bool = False) -> None:
    from huggingface_hub import hf_hub_download

    items = plan(specs, with_optional)
    need = print_plan(items)
    if not yes:
        print("\nDry run. Re-run with --yes to download.")
        return
    free = free_gb(models_dir())
    if need + SAFETY_MARGIN_GB > free:
        raise SystemExit(f"Not enough space: need {need:.1f} GB + margin, free {free:.1f} GB")

    token = os.environ.get("HF_TOKEN") or None
    for spec, rev, files in items:
        spec.local_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            dest = spec.local_dir / f.name
            if _is_complete(dest, f.size):
                continue
            print(f"Downloading {spec.repo}/{f.name} ({f.size / GB:.2f} GB)")
            hf_hub_download(
                repo_id=spec.repo,
                filename=f.name,
                revision=rev,
                local_dir=spec.local_dir,
                token=token,
            )
            if not _is_complete(dest, f.size):
                raise RuntimeError(f"size mismatch after download: {dest}")
        write_manifest(spec, rev, files)
    print("Done.")


def write_manifest(spec: ModelSpec, revision: str, files: list[RemoteFile]) -> None:
    manifest = {
        "id": spec.id,
        "repo": spec.repo,
        "revision": revision,
        "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": [{"name": f.name, "size": f.size, "sha256": f.sha256} for f in files],
    }
    (spec.local_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def sha256_file(path: Path, chunk: int = 16 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def verify_models(specs: list[ModelSpec]) -> bool:
    """Hash local files and compare with the sha256 stored in each manifest."""
    ok = True
    for spec in specs:
        mf = spec.local_dir / "manifest.json"
        if not mf.exists():
            print(f"{spec.id}: no manifest (not downloaded)")
            ok = False
            continue
        for f in json.loads(mf.read_text(encoding="utf-8"))["files"]:
            path = spec.local_dir / f["name"]
            if not path.exists():
                print(f"{spec.id}: missing {f['name']}")
                ok = False
            elif f["sha256"] and sha256_file(path) != f["sha256"]:
                print(f"{spec.id}: HASH MISMATCH {f['name']}")
                ok = False
            else:
                print(f"{spec.id}: ok {f['name']}")
    return ok


def download_datasets(specs: list[DatasetSpec], yes: bool = False) -> None:
    from huggingface_hub import hf_hub_download

    for d in specs:
        for name in d.files:
            dest = DATA_DIR / d.id / name
            state = "present" if dest.exists() else "to download"
            print(f"{d.id}: {d.repo}/{name} [{state}]")
            if yes and not dest.exists():
                hf_hub_download(
                    repo_id=d.repo,
                    filename=name,
                    repo_type="dataset",
                    local_dir=DATA_DIR / d.id,
                    token=os.environ.get("HF_TOKEN") or None,
                )
    if not yes:
        print("Dry run. Re-run with --yes to download.")
