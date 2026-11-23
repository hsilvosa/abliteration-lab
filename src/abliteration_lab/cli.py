"""Command line entry point: `abl <command>`."""

from __future__ import annotations

import argparse
import sys

from .config import GROUPS, ModelSpec, load_datasets, load_registry


def _select(args) -> list[ModelSpec]:
    reg = load_registry()
    groups = args.group or (None if args.model else ["core"])
    specs = reg.select(groups=groups, ids=args.model)
    if not specs:
        raise SystemExit("no models selected")
    return specs


def cmd_list(args) -> None:
    reg = load_registry()
    print(f"{'id':38} {'group':9} {'role':12} {'quant':10} {'GB':>6}  baseline")
    for m in reg.models:
        print(f"{m.id:38} {m.group:9} {m.role:12} {m.quant or '-':10} {m.size_gb:6.2f}  {m.baseline or '-'}")


def cmd_download(args) -> None:
    from .download import download_models, verify_models

    specs = _select(args)
    if args.verify:
        sys.exit(0 if verify_models(specs) else 1)
    download_models(specs, with_optional=args.with_optional, yes=args.yes)


def cmd_datasets(args) -> None:
    from .download import download_datasets

    download_datasets(load_datasets(), yes=args.yes)


def cmd_eval(args) -> None:
    from .eval_gguf import TASKS, evaluate_model

    tasks = args.task or list(TASKS)
    if args.own:
        specs = [ModelSpec(id=args.own, group="own", role="abliterated", format="gguf", repo="local", files=(args.file,))]
    else:
        specs = [s for s in _select(args) if s.format == "gguf"]
    for spec in specs:
        evaluate_model(spec, tasks, thinking=args.thinking, limit=args.limit)


def cmd_judge(args) -> None:
    from .judge import run

    ids = args.model or [m.id for m in load_registry().select(groups=["core"])]
    run(args.judge, ids, thinking=args.thinking)


def cmd_report(_args) -> None:
    from .report import write_report

    write_report()


def cmd_abliterate(args) -> None:
    from .abliterate.pipeline import run

    run(dry_run=args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="abl", description="Abliteration lab")
    sub = p.add_subparsers(dest="command", required=True)

    def add_selection(sp):
        sp.add_argument("--group", action="append", choices=GROUPS, help="model group (repeatable); default: core")
        sp.add_argument("--model", action="append", help="model id (repeatable)")

    sub.add_parser("list", help="show the model registry").set_defaults(func=cmd_list)

    d = sub.add_parser("download", help="download model files to the models dir (dry run unless --yes)")
    add_selection(d)
    d.add_argument("--with-optional", action="store_true", help="also fetch vision projectors / MTP drafters")
    d.add_argument("--yes", action="store_true", help="actually download")
    d.add_argument("--verify", action="store_true", help="hash local files against manifests")
    d.set_defaults(func=cmd_download)

    ds = sub.add_parser("datasets", help="download prompt and benchmark datasets (dry run unless --yes)")
    ds.add_argument("--yes", action="store_true")
    ds.set_defaults(func=cmd_datasets)

    e = sub.add_parser("eval", help="evaluate GGUF models through llama-server")
    add_selection(e)
    e.add_argument("--task", action="append", choices=["refusal", "over_refusal", "mmlu", "harmless_quality"])
    e.add_argument("--thinking", choices=["on", "off"], help="override configs/eval.toml")
    e.add_argument("--limit", type=int, help="first N items per task (smoke test)")
    e.add_argument("--own", help="evaluate an own model: id under <models_dir>/own/")
    e.add_argument("--file", help="GGUF file name inside <models_dir>/own/<id>/ (with --own)")
    e.set_defaults(func=cmd_eval)

    j = sub.add_parser("judge", help="classify saved refusal/over_refusal replies with a local LLM judge")
    j.add_argument("--judge", default="qwen3-14b-base", help="registry id of the judge model")
    j.add_argument("--model", action="append", help="model id whose outputs are judged (default: core)")
    j.add_argument("--thinking", default="off", choices=["on", "off"])
    j.set_defaults(func=cmd_judge)

    sub.add_parser("report", help="aggregate results/raw into results/summary.{csv,md}").set_defaults(func=cmd_report)

    a = sub.add_parser("abliterate", help="run our own abliteration (configs/abliterate.toml)")
    a.add_argument("--dry-run", action="store_true", help="resolve inputs without loading the model")
    a.set_defaults(func=cmd_abliterate)
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if getattr(args, "own", None) and not getattr(args, "file", None):
        raise SystemExit("--own requires --file")
    args.func(args)


if __name__ == "__main__":
    main()
