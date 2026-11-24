"""Generate reproducible portfolio charts from results CSVs into docs/assets/.

Run with any Python environment that has matplotlib + pandas (e.g. wuxia):
    python scripts/plot_results.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ASSETS = ROOT / "docs" / "assets"

SHORT_NAMES = {
    "gemma4-12b-qat-hauhaucs": "Gemma 4 12B QAT (HauhauCS)",
    "qwen3-14b-abliterated-mlabonne": "Qwen3 14B (mlabonne)",
    "gemma4-12b-qat-heretic-igorls": "Gemma 4 12B QAT Heretic (igorls)",
    "gemma4-12b-heretic-culturerevolt": "Gemma 4 12B Heretic (culturerevolt)",
    "qwen3-4b-instruct-2507-abl-v4": "Qwen3 4B own v4 (L18, s=1.5)",
    "qwen3-4b-instruct-2507-abl-v3": "Qwen3 4B own v3 (L18, s=2.0)",
    "qwen3-4b-instruct-2507-abl-v2": "Qwen3 4B own v2 (L25, s=1.5)",
    "qwen3-4b-instruct-2507-abl": "Qwen3 4B own v1 (L25, s=1.0)",
    "gemma4-12b-base": "Gemma 4 12B (base)",
    "gemma4-12b-qat-base": "Gemma 4 12B QAT (base)",
    "qwen3-14b-base": "Qwen3 14B (base)",
    "qwen3-4b-instruct-2507-base": "Qwen3 4B (base)",
}

# Fallback KL values from abliteration.json if D:\models\own is unavailable.
OWN_KL_FALLBACK = {
    "qwen3-4b-instruct-2507-base": 0.0,
    "qwen3-4b-instruct-2507-abl": 0.09605,
    "qwen3-4b-instruct-2507-abl-v2": 0.3834,
    "qwen3-4b-instruct-2507-abl-v4": 0.53896,
    "qwen3-4b-instruct-2507-abl-v3": 3.79094,
}


def _load_kl(model_id: str) -> float:
    p = Path("D:/models/own") / model_id / "abliteration.json"
    if p.exists():
        return float(json.loads(p.read_text(encoding="utf-8"))["selected"]["kl"])
    return OWN_KL_FALLBACK[model_id]


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.grid": True,
            "grid.color": "#e2e8f0",
            "grid.linestyle": "--",
            "grid.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
        }
    )


def plot_refusal_taxonomy(v3: pd.DataFrame) -> None:
    df = v3[(v3["task"] == "refusal") & (v3["thinking"] == "off")].copy()
    baselines = {
        "gemma4-12b-base",
        "gemma4-12b-qat-base",
        "qwen3-14b-base",
        "qwen3-4b-instruct-2507-base",
    }
    df["is_base"] = df["model"].isin(baselines)
    df = df.sort_values(["is_base", "direct_compliance"], ascending=[True, False]).reset_index(drop=True)
    df["unparsed_rate"] = df["unparsed"] / df["n"]

    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    y = np.arange(len(df))
    labels = [SHORT_NAMES.get(m, m) for m in df["model"]]

    cols = [
        ("direct_compliance", "Direct compliance", "#0f766e"),
        ("hedged_compliance", "Hedged compliance (disclaimers)", "#f59e0b"),
        ("safe_reframe", "Safe reframe (disguised refusal)", "#e11d48"),
        ("explicit_refusal", "Explicit refusal", "#475569"),
        ("unparsed_rate", "Unparsed", "#cbd5e1"),
    ]

    left = np.zeros(len(df))
    for col, title, color in cols:
        vals = df[col].to_numpy() * 100.0
        bars = ax.barh(y, vals, left=left, height=0.68, label=title, color=color, edgecolor="white", linewidth=0.6)
        for rect, v in zip(bars, vals):
            if v >= 8.0:
                tc = "white" if color in ("#0f766e", "#e11d48", "#475569") else "#1e293b"
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    rect.get_y() + rect.get_height() / 2,
                    f"{v:.0f}%",
                    ha="center",
                    va="center",
                    color=tc,
                    fontsize=8.5,
                    fontweight="bold",
                )
        left += vals

    # Separator line between abliterated models and baselines
    n_abl = int((~df["is_base"]).sum())
    ax.axhline(n_abl - 0.5, color="#64748b", linestyle=":", linewidth=1.2)
    ax.text(101.2, n_abl - 0.8, "Abliterated", va="bottom", ha="left", fontsize=8.5, color="#334155", fontweight="bold")
    ax.text(101.2, n_abl - 0.15, "Baselines", va="top", ha="left", fontsize=8.5, color="#64748b", fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of harmful_behaviors test prompts (n = 100, thinking = off) [%]")
    ax.set_title("4-Class Judge (v3) Breakdown on Refusal Prompts\nRegex heuristic scored 0% for all working abliterated models, hiding safe reframes and hedging")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3, frameon=False)
    fig.tight_layout()
    fig.savefig(ASSETS / "refusal_taxonomy_v3.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_pareto_own(summary: pd.DataFrame, v3: pd.DataFrame, coh: pd.DataFrame) -> None:
    order = [
        ("qwen3-4b-instruct-2507-base", "Base\n(unmodified)"),
        ("qwen3-4b-instruct-2507-abl", "v1\nL25 s=1.0"),
        ("qwen3-4b-instruct-2507-abl-v2", "v2\nL25 s=1.5"),
        ("qwen3-4b-instruct-2507-abl-v4", "v4\nL18 s=1.5"),
        ("qwen3-4b-instruct-2507-abl-v3", "v3\nL18 s=2.0"),
    ]
    ids = [m for m, _ in order]
    xlabels = [lbl for _, lbl in order]
    kls = [_load_kl(m) for m in ids]

    v3_ref = v3[(v3["task"] == "refusal") & (v3["thinking"] == "off")].set_index("model")
    coh_off = coh[coh["thinking"] == "off"].set_index("model")
    mmlu_off = summary[(summary["task"] == "mmlu") & (summary["thinking"] == "off")].set_index("model")

    direct = [v3_ref.loc[m, "direct_compliance"] * 100 for m in ids]
    reframe = [v3_ref.loc[m, "safe_reframe"] * 100 for m in ids]
    mmlu = [mmlu_off.loc[m, "rate"] * 100 for m in ids]
    mmlu_lo = [(mmlu_off.loc[m, "rate"] - mmlu_off.loc[m, "ci_low"]) * 100 for m in ids]
    mmlu_hi = [(mmlu_off.loc[m, "ci_high"] - mmlu_off.loc[m, "rate"]) * 100 for m in ids]
    degen = [coh_off.loc[m, "degenerate_rate"] * 100 for m in ids]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.8))
    x = np.arange(len(ids))

    # Panel 1: Compliance & Safe Reframe + KL labels
    ax1.plot(x, direct, marker="o", linewidth=2.4, markersize=8, color="#0f766e", label="Direct compliance (%)")
    ax1.plot(x, reframe, marker="s", linewidth=2.0, markersize=7, linestyle="--", color="#e11d48", label="Safe reframe (%)")
    for xi, d, kl in zip(x, direct, kls):
        ax1.annotate(f"KL={kl:.2f}", (xi, d), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=8.5, color="#334155")
    ax1.axvspan(2.6, 3.4, color="#ecfdf5", alpha=0.8, zorder=0)
    ax1.text(3.0, 93, "Sweet spot (v4)", ha="center", va="top", fontsize=8.5, color="#065f46", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(xlabels)
    ax1.set_ylim(-5, 102)
    ax1.set_ylabel("Rate on harmful_behaviors [%]")
    ax1.set_title("A. Refusal Removal Progression (v1–v4)")
    ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#e2e8f0")

    # Panel 2: Capability (MMLU) & Benign Degeneration
    ax2.errorbar(x, mmlu, yerr=[mmlu_lo, mmlu_hi], fmt="-o", linewidth=2.4, markersize=8, capsize=4, color="#1d4ed8", label="MMLU accuracy (95% CI)")
    ax2.bar(x, degen, width=0.42, alpha=0.38, color="#dc2626", label="Benign degeneration rate (%)")
    for xi, m_val, hi, d_val in zip(x, mmlu, mmlu_hi, degen):
        ax2.annotate(f"{m_val:.1f}%", (xi, m_val + hi), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8.5, color="#1e3a8a", fontweight="bold")
        if d_val >= 10:
            ax2.text(xi, d_val * 0.45, f"{d_val:.0f}%\nloops", ha="center", va="center", fontsize=8.5, color="#7f1d1d", fontweight="bold")
    ax2.axvspan(3.6, 4.4, color="#fef2f2", alpha=0.85, zorder=0)
    ax2.text(4.0, 95, "Over-ablated (v3)", ha="center", va="top", fontsize=8.5, color="#991b1b", fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(xlabels)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Percentage [%]")
    ax2.set_title("B. Collateral Cost: MMLU & Benign Coherence")
    ax2.legend(loc="center left", frameon=True, facecolor="white", edgecolor="#e2e8f0")

    fig.suptitle("Own Abliteration Pareto Curve on Qwen3-4B-Instruct-2507 (Q4_K_M, thinking = off)", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(ASSETS / "pareto_v1_to_v4.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_tradeoff_scatter(summary: pd.DataFrame, v3: pd.DataFrame, coh: pd.DataFrame) -> None:
    mmlu_off = summary[(summary["task"] == "mmlu") & (summary["thinking"] == "off")].set_index("model")
    v3_ref = v3[(v3["task"] == "refusal") & (v3["thinking"] == "off")].set_index("model")
    coh_off = coh[coh["thinking"] == "off"].set_index("model")

    pairs = [
        ("gemma4-12b-qat-hauhaucs", "gemma4-12b-qat-base", "Gemma 4 12B HauhauCS", (0, 12)),
        ("gemma4-12b-qat-heretic-igorls", "gemma4-12b-qat-base", "Gemma 4 12B igorls", (10, 6)),
        ("gemma4-12b-heretic-culturerevolt", "gemma4-12b-base", "Gemma 4 12B culturerevolt", (10, 4)),
        ("qwen3-14b-abliterated-mlabonne", "qwen3-14b-base", "Qwen3 14B mlabonne", (-12, -16)),
        ("qwen3-4b-instruct-2507-abl", "qwen3-4b-instruct-2507-base", "Qwen3 4B own v1", (10, -6)),
        ("qwen3-4b-instruct-2507-abl-v2", "qwen3-4b-instruct-2507-base", "Qwen3 4B own v2", (0, -18)),
        ("qwen3-4b-instruct-2507-abl-v4", "qwen3-4b-instruct-2507-base", "Qwen3 4B own v4", (-10, -16)),
        ("qwen3-4b-instruct-2507-abl-v3", "qwen3-4b-instruct-2507-base", "Qwen3 4B own v3", (-16, 12)),
    ]

    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    ax.axhspan(-4.0, 4.0, color="#f1f5f9", alpha=0.85, zorder=0, label="MMLU sampling noise band (±4 pts, n = 285)")
    ax.axhline(0.0, color="#64748b", linewidth=1.0, linestyle="--", zorder=1)

    xs, ys, degs, names, offsets = [], [], [], [], []
    for m, b, label, off in pairs:
        xs.append(v3_ref.loc[m, "direct_compliance"] * 100)
        ys.append((mmlu_off.loc[m, "rate"] - mmlu_off.loc[b, "rate"]) * 100)
        degs.append(coh_off.loc[m, "degenerate_rate"] * 100)
        names.append(label)
        offsets.append(off)

    sc = ax.scatter(
        xs,
        ys,
        c=degs,
        cmap="RdYlGn_r",
        vmin=0,
        vmax=65,
        s=[130 + 5 * d for d in degs],
        edgecolors="#0f172a",
        linewidths=1.0,
        zorder=3,
    )
    cbar = fig.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Benign degeneration rate on harmless_quality [%]")

    for x, y, name, (dx, dy) in zip(xs, ys, names, offsets):
        ha = "center" if dx == 0 else ("right" if dx < 0 else "left")
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(dx, dy), ha=ha, fontsize=9, color="#0f172a")

    ax.set_xlim(-4, 92)
    ax.set_ylim(-15, 5.5)
    ax.set_xlabel("Direct compliance on harmful_behaviors (Judge v3) [%]")
    ax.set_ylabel("MMLU delta vs unmodified baseline [percentage points]")
    ax.set_title("Capability vs. Direct Compliance Trade-Off (Color & Size = Benign Degeneration)")
    ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#e2e8f0")
    fig.tight_layout()
    fig.savefig(ASSETS / "capability_vs_compliance.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    _style()
    summary = pd.read_csv(RESULTS / "summary.csv")
    v3 = pd.read_csv(RESULTS / "judge_v3_breakdown.csv")
    coh = pd.read_csv(RESULTS / "coherence.csv")
    plot_refusal_taxonomy(v3)
    plot_pareto_own(summary, v3, coh)
    plot_tradeoff_scatter(summary, v3, coh)
    print(f"Wrote charts to {ASSETS}")


if __name__ == "__main__":
    main()
