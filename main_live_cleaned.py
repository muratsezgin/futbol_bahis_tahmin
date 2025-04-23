
import time
import pickle
import pandas as pd
import numpy as np
from config import API_FOOTBALL_KEY
from fetch_live_data import get_live_premier_league_matches, extract_features_from_fixture
from model_utils import preprocess_features

def run_loop():
    print("⚽ Canlı Premier League analiz başlatıldı...")

    while True:
        fixtures = get_live_premier_league_matches(API_FOOTBALL_KEY)

        for fixture in fixtures:
            try:
                fixture_id = fixture['fixture']['id']
                home = fixture['teams']['home']['name']
                away = fixture['teams']['away']['name']
                score_home = fixture['goals']['home']
                score_away = fixture['goals']['away']
                minute = fixture['fixture']['status']['elapsed']

                features = extract_features_from_fixture(fixture)
                features_df = pd.DataFrame([features])
                features_encoded = preprocess_features(features_df)

                with open("model_xgb.pkl", "rb") as f:
                    model = pickle.load(f)

                proba = model.predict_proba(features_encoded)[0]
                pred_label = model.predict(features_encoded)[0]
                confidence = round(float(np.max(proba)) * 100, 2)

                prediction_text = "1 goal more" if pred_label == 1 else "No more goals"

                print(f"Match: {home} vs {away} (min: {minute})")
                print(f"Score: {score_home} - {score_away}")
                print(f"Prediction: {prediction_text}")
                print(f"Confidence: {confidence}%")
                print("-" * 60)

            except Exception as e:
                print(f"⚠️ Hata: {e}")

        time.sleep(300)

if __name__ == "__main__":
    run_loop()
