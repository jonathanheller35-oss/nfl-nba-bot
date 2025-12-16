from __future__ import annotations
import matplotlib.pyplot as plt


def render_nba_signal_chart(
    x_labels: list[str],              # e.g. ["G1","G2","G3","G4","G5","G6"]
    y_values: list[float],            # metric values aligned to x_labels
    baseline: float,                  # season average (or long-run avg)
    recent_n: int,                    # highlight last N games (usually 5)
    player_name: str,
    metric_name: str,
    annotation_text: str,             # e.g. "+6.2 over last 5"
    outfile: str = "chart.png",
) -> str:
    if len(x_labels) != len(y_values):
        raise ValueError("x_labels and y_values must have the same length.")
    if len(x_labels) < 6:
        raise ValueError("Use at least 6 points so the trend is meaningful.")
    if recent_n < 2 or recent_n > len(x_labels):
        raise ValueError("recent_n must be between 2 and len(x_labels).")

    # Canvas sized for X/Twitter
    plt.figure(figsize=(12, 6.75))

    # Main line (full series)
    plt.plot(x_labels, y_values, linewidth=2)

    # Highlight recent window (last N)
    start = len(x_labels) - recent_n
    plt.plot(x_labels[start:], y_values[start:], linewidth=3)

    # Baseline (season avg)
    plt.axhline(baseline, linestyle="--", linewidth=1)

    # Title (top-left)
    plt.title(f"{player_name} — {metric_name}", loc="left", fontsize=16, fontweight="semibold")

    # One annotation (pointing to latest value)
    plt.annotate(
        annotation_text,
        xy=(x_labels[-1], y_values[-1]),
        xytext=(-90, 35),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
        fontsize=12,
    )

    # Clean styling
    plt.grid(axis="y", alpha=0.15)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    plt.savefig(outfile, dpi=150)
    plt.close()
    return outfile
