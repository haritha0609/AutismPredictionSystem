import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from utils.prompts import build_prompt

# ============================
# Load .env from project root
# ============================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# ============================
# Gemini Client
# ============================

client = genai.Client(api_key=API_KEY)


# ============================
# Test Gemini Connection
# ============================

def test_connection():
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Reply with exactly: Gemini Connected Successfully"
    )
    return response.text.strip()
def list_models():
    print("\nAvailable Gemini Models:\n")

    for model in client.models.list():
        print(model.name)

# ============================
# Generate Personalized Wellness
# ============================

def generate_wellness(data):
    """
    Sends child information to Gemini and
    returns structured wellness guidance.
    """

    prompt = build_prompt(data)

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        text = response.text.strip()

        print("\n================ GEMINI RESPONSE ================\n")
        print(text)
        print("\n=================================================\n")

        # Remove markdown if Gemini returns ```json
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "diet_plan": [
                "Provide a balanced diet with fruits, vegetables, whole grains, milk, eggs, pulses and protein-rich foods.",
                "Reduce processed foods and sugary drinks.",
                "Encourage adequate water intake."
            ],

            "exercise_plan": [
                "30–45 minutes of outdoor play daily.",
                "Walking, cycling or simple stretching exercises.",
                "Indoor movement games when outdoor activity isn't possible."
            ],

            "sensory_activities": [
                "Sand play",
                "Water play",
                "Building blocks",
                "Sensory bins with rice or beans"
            ],

            "communication_activities": [
                "Picture cards",
                "Story reading",
                "Singing rhymes",
                "Simple conversation practice"
            ],

            "parent_guidance": [
                "Maintain a consistent daily routine.",
                "Reward positive behaviour.",
                "Encourage social interaction.",
                "Consult a developmental pediatrician if needed."
            ],

            "weekly_routine": [
                {
                    "day": "Monday",
                    "activity": "Speech practice and outdoor play"
                },
                {
                    "day": "Tuesday",
                    "activity": "Sensory activities"
                },
                {
                    "day": "Wednesday",
                    "activity": "Reading and puzzles"
                },
                {
                    "day": "Thursday",
                    "activity": "Physical exercise"
                },
                {
                    "day": "Friday",
                    "activity": "Communication games"
                },
                {
                    "day": "Saturday",
                    "activity": "Family activities"
                },
                {
                    "day": "Sunday",
                    "activity": "Relaxation and nature walk"
                }
            ],

            "motivation": "Every child develops at their own pace. Early support, patience and consistent care can make a meaningful difference."
        }