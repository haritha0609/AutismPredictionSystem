import joblib
import pandas as pd
import os

# ==========================================
# Load XGBoost Behavioral Model
# ==========================================

MODEL_PATH = os.path.join("models", "behavior_model.pkl")

model = joblib.load(MODEL_PATH)


# ==========================================
# Prediction Function
# ==========================================

def predict_behavior(data):

    df = pd.DataFrame([{

        "A1": int(data["A1"]),
        "A2": int(data["A2"]),
        "A3": int(data["A3"]),
        "A4": int(data["A4"]),
        "A5": int(data["A5"]),
        "A6": int(data["A6"]),
        "A7": int(data["A7"]),
        "A8": int(data["A8"]),
        "A9": int(data["A9"]),
        "A10": int(data["A10"]),

        "Age": int(data["Age"]),

        "Sex": 1 if data["Sex"] == "m" else 0,

        "Jauundice": 1 if data["Jauundice"] == "yes" else 0,

        "Family_ASD": 1 if data["Family_ASD"] == "yes" else 0

    }])

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0]

    confidence = round(max(probability) * 100, 2)

    print("\n==============================")
    print("Input Data")
    print(df)
    print("------------------------------")
    print("Prediction :", prediction)
    print("Probability:", probability)
    print("Classes    :", model.classes_)
    print("==============================\n")

    if prediction == 1:
        result = "Autism Detected"
    else:
        result = "No Autism Detected"

    return {
        "prediction": prediction,
        "result": result,
        "confidence": confidence
    }