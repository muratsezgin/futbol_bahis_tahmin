
import pickle

def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def make_prediction(model, df):
    proba = model.predict_proba(df)[0]
    label = model.classes_[proba.argmax()]
    confidence = proba.max()
    return label, confidence
