from chart_template import render_nba_signal_chart

# Fake "last 12 games" example
x = [f"G{i}" for i in range(1, 13)]
y = [28, 27, 29, 30, 28, 31, 33, 34, 35, 34, 36, 37]  # e.g., minutes or usage-proxy
baseline = sum(y) / len(y)

render_nba_signal_chart(
    x_labels=x,
    y_values=y,
    baseline=baseline,
    recent_n=5,
    player_name="Player X",
    metric_name="Minutes (Trend)",
    annotation_text="+6 over last 5",
    outfile="nba_template_chart.png",
)

print("Saved nba_template_chart.png")
