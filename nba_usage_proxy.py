from __future__ import annotations

from datetime import datetime
from typing import Tuple, List

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

from chart_template import render_nba_signal_chart


def find_player_id(full_name: str) -> int:
    matches = players.find_players_by_full_name(full_name)
    if not matches:
        raise ValueError(f"No NBA player found for name: {full_name}")
    # Take best match (first). You can harden later.
    return matches[0]["id"]


def get_last_n_games(player_id: int, n: int = 20) -> Tuple[List[str], List[float]]:
    # Pull current season game logs. If needed, we can add season="2024-25" etc.
    gl = playergamelog.PlayerGameLog(player_id=player_id)
    df = gl.get_data_frames()[0]

    if df.empty:
        raise ValueError("No game logs returned. Player may be inactive or API rate-limited.")

    # Game log is usually newest-first; sort oldest->newest for charting
    df["GAME_DATE"] = df["GAME_DATE"].apply(lambda s: datetime.strptime(s, "%b %d, %Y"))
    df = df.sort_values("GAME_DATE")

    # Keep last n games
    df = df.tail(n)

    # Build x labels (MM/DD) and usage proxy series
    x = df["GAME_DATE"].dt.strftime("%m/%d").tolist()

    # Usage proxy: FGA + 0.44*FTA + AST
    y = (df["FGA"] + 0.44 * df["FTA"] + df["AST"]).astype(float).tolist()

    return x, y


def main():
    # === CHANGE THIS NAME TO TEST ANY PLAYER ===
    player_name = "Jayson Tatum"

    # Settings
    last_n_games = 20
    recent_n = 5  # highlight last 5 games

    player_id = find_player_id(player_name)
    x, y = get_last_n_games(player_id, n=last_n_games)

    baseline = sum(y) / len(y)
    recent_avg = sum(y[-recent_n:]) / recent_n
    delta = recent_avg - baseline

    sign = "+" if delta >= 0 else ""
    annotation = f"{sign}{delta:.1f} vs baseline (last {recent_n})"

    render_nba_signal_chart(
        x_labels=x,
        y_values=y,
        baseline=baseline,
        recent_n=recent_n,
        player_name=player_name,
        metric_name="Usage Proxy (FGA + 0.44*FTA + AST)",
        annotation_text=annotation,
        outfile="nba_usage_proxy_chart.png",
    )

    print("Saved nba_usage_proxy_chart.png")


if __name__ == "__main__":
    main()
