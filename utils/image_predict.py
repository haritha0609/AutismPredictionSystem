import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


# ==========================================
# Load Trained ResNet50 Model
# ==========================================

MODEL_PATH = os.path.join("models", "resnet50_best.keras")

model = load_model(MODEL_PATH)


# ==========================================
# Face Detection
# ==========================================

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def has_face(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    return len(faces) > 0


# ==========================================
# Image Prediction
# ==========================================

def predict_image(image_path):

    img = image.load_img(
        image_path,
        target_size=(224, 224)
    )

    img = image.img_to_array(img)

    img = tf.keras.applications.resnet50.preprocess_input(img)

    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img, verbose=0)

    probability = float(prediction[0][0])

    # Dataset class indices:
    # autistic = 0
    # non_autistic = 1

    if probability < 0.5:

        result = "Autism Detected"

    else:

        result = "No Autism Detected"

    return {

        "prediction": result

    }  