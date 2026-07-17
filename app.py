from flask import Flask, render_template, request, session
import os
from utils.hospital_locator import find_autism_hospitals
from utils.behavioral_predict import predict_behavior
from utils.image_predict import predict_image, has_face
from utils.gemini_service import generate_wellness

app = Flask(__name__)
app.secret_key = "autism_prediction_secret"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================
# HOME PAGE
# =====================================
@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# QUESTIONNAIRE PAGE
# =====================================
@app.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html")


# =====================================
# BEHAVIORAL PREDICTION
# =====================================
@app.route("/behavioral-result", methods=["POST"])
def behavioral_result():

    data = {

        "A1": request.form["A1"],
        "A2": request.form["A2"],
        "A3": request.form["A3"],
        "A4": request.form["A4"],
        "A5": request.form["A5"],
        "A6": request.form["A6"],
        "A7": request.form["A7"],
        "A8": request.form["A8"],
        "A9": request.form["A9"],
        "A10": request.form["A10"],

        "Age": request.form["Age"],
        "Sex": request.form["Sex"],
        "Jauundice": request.form["Jauundice"],
        "Family_ASD": request.form["Family_ASD"]
    }

    result = predict_behavior(data)

    # Save questionnaire answers
    session["questionnaire"] = data

    # Save behavioral prediction
    session["behavior_prediction"] = result["result"]

    return render_template(
        "behavioral_result.html",
        prediction=result["result"],
        autism=result["prediction"] == 1
    )
# =====================================
# IMAGE UPLOAD PAGE
# =====================================
@app.route("/upload-image")
def upload_image():
    return render_template("upload_image.html")


# =====================================
# FACIAL PREDICTION
# =====================================

# =====================================
# FACIAL PREDICTION
# =====================================
@app.route("/predict-image", methods=["POST"])
def facial_prediction():

    if "image" not in request.files:
        return render_template(
            "upload_image.html",
            error="Please upload an image."
        )

    image = request.files["image"]

    if image.filename == "":
        return render_template(
            "upload_image.html",
            error="Please select an image."
        )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(image_path)

    # -----------------------------------------
    # Validate uploaded image
    # -----------------------------------------
    is_valid, message = has_face(image_path)

    if not is_valid:

        if os.path.exists(image_path):
            os.remove(image_path)

        return render_template(
            "upload_image.html",
            error=message
        )

    # -----------------------------------------
    # Facial Prediction
    # -----------------------------------------
    result = predict_image(image_path)

    # Save facial prediction in session
    session["face_prediction"] = result["prediction"]

    return render_template(
        "final_result.html",
        image=image_path,
        facial_prediction=result["prediction"]
    )
# =====================================
# WELLNESS QUESTIONS PAGE
# =====================================
@app.route("/wellness-questions")
def wellness_questions():
    return render_template("wellness_questions.html")


# =====================================
# GENERATE AI WELLNESS PLAN
# =====================================
@app.route("/search-hospitals", methods=["POST"])
def search_hospitals():

    location = request.form.get("location")

    hospitals, fallback = find_autism_hospitals(location)

    return render_template(
        "hospital_results.html",
        hospitals=hospitals,
        location=location,
        fallback=fallback
    )
@app.route("/generate-wellness", methods=["POST"])
def generate_wellness_route():

    questionnaire = session.get("questionnaire", {})

    behavior_prediction = session.get(
        "behavior_prediction",
        "Unknown"
    )

    face_prediction = session.get(
        "face_prediction",
        "Unknown"
    )

    data = {

        # -------------------------
        # Child Details
        # -------------------------
        "age": questionnaire.get("Age"),
        "gender": questionnaire.get("Sex"),

        # -------------------------
        # Behavioral Questionnaire
        # -------------------------
        "A1": questionnaire.get("A1"),
        "A2": questionnaire.get("A2"),
        "A3": questionnaire.get("A3"),
        "A4": questionnaire.get("A4"),
        "A5": questionnaire.get("A5"),
        "A6": questionnaire.get("A6"),
        "A7": questionnaire.get("A7"),
        "A8": questionnaire.get("A8"),
        "A9": questionnaire.get("A9"),
        "A10": questionnaire.get("A10"),

        "family_history": questionnaire.get("Family_ASD"),
        "jaundice": questionnaire.get("Jauundice"),

        # -------------------------
        # Predictions
        # -------------------------
        "behavior_prediction": behavior_prediction,
        "face_prediction": face_prediction,

        # -------------------------
        # Lifestyle Details
        # -------------------------
        "food_allergy": request.form.get("food_allergy", ""),
        "diet_preference": request.form.get("diet_preference", ""),
        "sleep_hours": request.form.get("sleep_hours", ""),
        "outdoor_play": request.form.get("outdoor_play", ""),
        "sensory_issues": request.form.get("sensory_issues", ""),
        "favorite_activity": request.form.get("favorite_activity", ""),
        "parent_concern": request.form.get("parent_concern", "")
    }

    try:
        wellness = generate_wellness(data)

        return render_template(
            "wellness.html",
            wellness=wellness,
            behavior_prediction=behavior_prediction,
            face_prediction=face_prediction
        )

    except Exception as e:

        return render_template(
            "wellness.html",
            wellness={
                "diet_plan": [
                    "Unable to generate recommendations at this time."
                ],
                "exercise_plan": [],
                "sensory_activities": [],
                "communication_activities": [],
                "parent_guidance": [],
                "weekly_routine": [],
                "motivation": str(e)
            },
            behavior_prediction=behavior_prediction,
            face_prediction=face_prediction
        )


# =====================================
# RUN APP
# =====================================
if __name__ == "__main__":
    app.run(debug=True, port=8000)