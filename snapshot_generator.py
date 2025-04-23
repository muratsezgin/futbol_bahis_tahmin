
import pandas as pd
import os

# Klasör yolu
base_path = "."

# Dosya yolları
match_info = pd.read_csv(f"{base_path}/match_info.csv")
xg_data = pd.read_csv(f"{base_path}/xg_data_all_merged_cleaned.csv")
events = pd.read_csv(f"{base_path}/events.csv")
tempo = pd.read_csv(f"{base_path}/tempo_by_fixture.csv")
lineups = pd.read_csv(f"{base_path}/lineups.csv")
subs = pd.read_csv(f"{base_path}/substitutions.csv")
team_form = pd.read_csv(f"{base_path}/team_form.csv")
player_form = pd.read_csv(f"{base_path}/player_form.csv")
importance = pd.read_csv(f"{base_path}/match_importance.csv")
difficulty = pd.read_csv(f"{base_path}/fixture_difficulty.csv")

# Örnek snapshot: dakika 25 itibarıyla skor, xG farkı, tempo, maç önemi vs.
snapshots = []

for fixture_id in match_info["fixture_id"].unique():
    fixture_events = events[events["fixture_id"] == fixture_id]
    fixture_xg = xg_data[xg_data["match_id"] == fixture_id]
    tempo_df = tempo[tempo["fixture_id"] == fixture_id]
    form_home = match_info[match_info["fixture_id"] == fixture_id]["home_team"].values[0]
    form_away = match_info[match_info["fixture_id"] == fixture_id]["away_team"].values[0]

    for minute in range(5, 95, 5):
        snap = {
            "fixture_id": fixture_id,
            "time_elapsed": minute,
            "home_team": form_home,
            "away_team": form_away,
        }

        # Anlık skor
        goals = fixture_events[fixture_events["type"] == "Goal"]
        snap["home_goals"] = len(goals[goals["team"] == form_home][goals["time_elapsed"] <= minute])
        snap["away_goals"] = len(goals[goals["team"] == form_away][goals["time_elapsed"] <= minute])

        # Tempo
        snap["tempo_5min"] = len(fixture_events[fixture_events["time_elapsed"].between(minute-5, minute)])

        # xG farkı (dakikaya kadar)
        if not fixture_xg.empty:
            snap["home_xg"] = fixture_xg["home_xg"].values[0]
            snap["away_xg"] = fixture_xg["away_xg"].values[0]
            snap["xg_diff"] = snap["home_xg"] - snap["away_xg"]
        else:
            snap["home_xg"] = snap["away_xg"] = snap["xg_diff"] = 0

        # Maç önemi
        imp = importance[importance["fixture_id"] == fixture_id]["match_importance"]
        snap["importance"] = imp.values[0] if not imp.empty else "unknown"

        # Fikstür zorluğu
        diff_row = difficulty[difficulty["fixture_id"] == fixture_id]
        if not diff_row.empty:
            snap["home_fixture_difficulty"] = diff_row["home_fixture_difficulty"].values[0] if not diff_row["home_fixture_difficulty"].isna().all() else None
            snap["away_fixture_difficulty"] = diff_row["away_fixture_difficulty"].values[0] if not diff_row["away_fixture_difficulty"].isna().all() else None
        else:
            snap["home_fixture_difficulty"] = snap["away_fixture_difficulty"] = None

        snapshots.append(snap)

df_snapshots = pd.DataFrame(snapshots)
df_snapshots.to_csv(f"{base_path}/snapshot_dataset.csv", index=False)
print("✅ snapshot_dataset.csv oluşturuldu.")
