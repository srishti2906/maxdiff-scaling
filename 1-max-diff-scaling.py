# 1-max-diff-scaling.py
# MaxDiff Article 1 — Introduction with Simple Count + ~95% CI visuals (retail example)

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

# Use a non-GUI backend so script runs on macOS/servers/CI without a display
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# =====================================================================
# Utilities
# =====================================================================

def set_seed(seed: int = 42) -> None:
    """Reproducibility across Python's random and NumPy RNGs."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_outdir(path: Path) -> None:
    """Create output directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


# =====================================================================
# Core MaxDiff logic
# =====================================================================

def simulate_maxdiff(
    items: List[str],
    n_respondents: int = 20,
    sets_per_resp: int = 5,
    items_per_set: int = 4,
) -> pd.DataFrame:
    """
    Simulate a simple MaxDiff dataset.
    Each respondent answers `sets_per_resp` sets by selecting a Most and a Least item from a random subset.
    Returns a DataFrame with columns: Respondent, Set (list[str]), Most, Least.
    """
    records: List[Tuple[int, List[str], str, str]] = []
    for resp in range(n_respondents):
        for _ in range(sets_per_resp):
            choice_set = random.sample(items, items_per_set)
            most = random.choice(choice_set)
            # choose a least that's different from most
            least_pool = [i for i in choice_set if i != most]
            least = random.choice(least_pool)
            records.append((resp, choice_set, most, least))

    df = pd.DataFrame(records, columns=["Respondent", "Set", "Most", "Least"])
    return df


def simple_count_scores(df: pd.DataFrame, items: List[str]) -> pd.DataFrame:
    """
    Compute simple-count scores and approximate 95% CI for each item using vectorized operations.

    Score(item) = (Most - Least) / Shown, where:
      - Shown: number of times item appears in any set
      - Most:  number of times item was picked as Most
      - Least: number of times item was picked as Least

    CI uses a normal approximation on (pM - pL), where pM = Most/Shown, pL = Least/Shown.
    """
    # Count appearances ("Shown") by exploding the Set column
    shown = (
        df["Set"]
        .explode()
        .value_counts()
        .reindex(items, fill_value=0)
        .rename("Shown")
    )

    # Count Most and Least selections
    most = df["Most"].value_counts().reindex(items, fill_value=0).rename("Most")
    least = df["Least"].value_counts().reindex(items, fill_value=0).rename("Least")

    # Assemble into a single frame
    out = pd.concat([most, least, shown], axis=1).reset_index()
    out = out.rename(columns={"index": "Item"})

    # Simple-count score
    out["Score"] = (out["Most"] - out["Least"]) / out["Shown"].replace(0, np.nan)

    # Approx standard error for (pM - pL); guard against divide-by-zero with replace
    pM = out["Most"] / out["Shown"].replace(0, np.nan)
    pL = out["Least"] / out["Shown"].replace(0, np.nan)
    out["SE"] = np.sqrt((pM * (1 - pM) + pL * (1 - pL)) / out["Shown"].replace(0, np.nan))

    z = 1.96  # ~95% normal quantile
    out["CI_L"] = out["Score"] - z * out["SE"]
    out["CI_U"] = out["Score"] + z * out["SE"]

    # Ranking + 0–100 scaling for an exec-friendly view
    out = out.sort_values("Score", ascending=False, ignore_index=True)
    min_s, max_s = out["Score"].min(), out["Score"].max()
    span = max_s - min_s
    out["Scaled_0_100"] = np.where(
        span > 0, (out["Score"] - min_s) / span * 100, 50.0
    )
    out["Rank"] = np.arange(1, len(out) + 1)

    # Standardize column order
    cols = ["Rank", "Item", "Most", "Least", "Shown", "Score", "CI_L", "CI_U", "SE", "Scaled_0_100"]
    out = out[cols]
    return out


# =====================================================================
# Plotting
# =====================================================================

def plot_ci_lollipop(ranked: pd.DataFrame, out_path: Path) -> None:
    """
    MaxDiff Simple-Count Scores with Approx. 95% CI
    A clean 'lollipop' plot: stems from 0 to Score, dot at Score, and a horizontal CI.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    # Plot from bottom to top in order of ranking (rank 1 at top)
    y = np.arange(len(ranked))[::-1]

    # Stems from 0 to each score
    ax.hlines(y=y, xmin=0, xmax=ranked["Score"], linewidth=1)

    # Points at score
    ax.plot(ranked["Score"], y, "o")

    # Confidence intervals
    for i, row in ranked.iterrows():
        yy = len(ranked) - 1 - i
        ax.plot([row["CI_L"], row["CI_U"]], [yy, yy], linewidth=3, alpha=0.6)

    ax.axvline(0, linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(ranked["Item"])
    ax.set_xlabel("Preference Score (Most - Least) / Shown")
    ax.set_title("MaxDiff Simple-Count Scores With Approx. 95% CI")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_exec_bar(ranked: pd.DataFrame, out_path: Path) -> None:
    """
    MaxDiff — Executive View (Scaled Utilities From Simple Count)
    Horizontal bar chart on 0–100 scale for clear communication to leadership.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    # Reverse order so rank 1 is on top visually
    items = ranked["Item"][::-1]
    vals = ranked["Scaled_0_100"][::-1]

    ax.barh(items, vals)
    ax.set_xlabel("Scaled Preference (0–100)")
    ax.set_title("MaxDiff — Executive View (Scaled Utilities From Simple Count)")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


# =====================================================================
# Main
# =====================================================================

def main(
    out_dir: Path,
    n_respondents: int,
    sets_per_resp: int,
    items_per_set: int,
) -> None:
    set_seed(42)
    ensure_outdir(out_dir)

    # Retail product features example
    items = [
        "Free Shipping",
        "Same-Day Delivery",
        "Easy Returns",
        "Extended Warranty",
        "Loyalty Points",
        "Discount Coupons"
    ]

    # 1) Simulate
    df = simulate_maxdiff(
        items=items,
        n_respondents=n_respondents,
        sets_per_resp=sets_per_resp,
        items_per_set=items_per_set,
    )

    # 2) Score
    result_table = simple_count_scores(df, items).round(3)

    # 3) Save table
    csv_path = out_dir / "maxdiff_simplecount_results.csv"
    result_table.to_csv(csv_path, index=False)

    # 4) Plots
    ci_png = out_dir / "maxdiff_simplecount_ci.png"
    exec_png = out_dir / "maxdiff_scaled_bar.png"
    plot_ci_lollipop(result_table, ci_png)
    plot_exec_bar(result_table, exec_png)

    # 5) Console summary
    print("\n=== MaxDiff Simple-Count Results (head) ===")
    print(result_table.to_string(index=False))
    print(f"\nSaved CSV:  {csv_path}")
    print(f"Saved plot: {ci_png}")
    print(f"Saved plot: {exec_png}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MaxDiff Simple-Count + ~95% CI visuals (retail example)"
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).parent / "outputs",
        help="Directory to write outputs (CSV + PNGs).",
    )
    parser.add_argument(
        "--respondents",
        type=int,
        default=20,
        help="Number of respondents to simulate.",
    )
    parser.add_argument(
        "--sets-per-respondent",
        type=int,
        default=5,
        help="Number of MaxDiff sets per respondent.",
    )
    parser.add_argument(
        "--items-per-set",
        type=int,
        default=4,
        help="Number of items shown per set.",
    )

    args = parser.parse_args()
    main(
        out_dir=args.out_dir,
        n_respondents=args.respondents,
        sets_per_resp=args.sets_per_respondent,
        items_per_set=args.items_per_set,
    )
