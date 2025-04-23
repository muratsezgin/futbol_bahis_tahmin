
import time
import pickle
import pandas as pd
from fetch_live_data import fetch_live_matches
from prepare_features import prepare_features_for_live
from model_utils import load_model, make_prediction

print("⚽ Canlı Premier League analiz başlatıldı...")

def run_loop():
    model = load_model("model_xgb.pkl")
    fixtures = fetch_live_matches()
    for fixture in fixtures:
        try:
            home = fixture["teams"]["home"]["name"]
            away = fixture["teams"]["away"]["name"]
            score_home = fixture["goals"]["home"]
            score_away = fixture["goals"]["away"]
            minute = fixture["fixture"]["status"]["elapsed"]
            print(f"\n💪 {home} vs {away} (dk: {minute})\nSkor: {score_home} - {score_away}")
            features_df = prepare_features_for_live(fixture)
            label, prob = make_prediction(model, features_df)
            print(f"Tahmin: {label} | Güven: {prob*100:.1f}%")
        except Exception as e:
            print(f"⚠️ Error while processing fixture: {e}")

if __name__ == "__main__":
    run_loop()
