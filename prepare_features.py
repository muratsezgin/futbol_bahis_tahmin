
import pandas as pd

def prepare_features_for_live(fixture):
    # Örnek olarak sadece bazı özellikler alınıyor
    features = {
        "minute": fixture["fixture"]["status"]["elapsed"],
        "home_team": fixture["teams"]["home"]["name"],
        "away_team": fixture["teams"]["away"]["name"],
        "score_home": fixture["goals"]["home"],
        "score_away": fixture["goals"]["away"],
    }
    df = pd.DataFrame([features])
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('category').cat.codes
    return df
