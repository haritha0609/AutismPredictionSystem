from flask import Flask, render_template, request
import os

from utils.behavioral_predict import predict_behavior
from utils.image_predict import predict_image, has_face
from utils.recommendations import get_recommendations

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
    # Check whether image contains a human face
    # -----------------------------------------
    if not has_face(image_path):

        os.remove(image_path)

        return render_template(
            "upload_image.html",
            error="Please upload a clear frontal facial image only."
        )

    # -----------------------------------------
    # Facial Prediction
    # -----------------------------------------
    result = predict_image(image_path)

    return render_template(
        "final_result.html",
        image=image_path,
        facial_prediction=result["prediction"]
    )


# =====================================
# WELLNESS PAGE
# =====================================
@app.route("/wellness")
def wellness():

    # Change this later if you want to pass
    # the actual facial prediction.
    prediction = "Autism Detected"

    recommendation = get_recommendations(prediction)

    return render_template(
        "wellness.html",
        status=recommendation["status"],
        recommendations=recommendation["recommendations"]
    )


# =====================================
# RUN APP
# =====================================
if __name__ == "__main__":
    app.run(debug=True)