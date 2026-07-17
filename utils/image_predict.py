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

print("⏳ Loading ResNet model...")

model = load_model(MODEL_PATH)

print("✅ ResNet model loaded")

# ==========================================
# MediaPipe Face Detection
# ==========================================
# ==========================================
# OpenCV Face Detector
# ==========================================

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# ==========================================
# Validate Uploaded Image
# ==========================================


def has_face(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return False, "Unable to read the uploaded image."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    # No face
    if len(faces) == 0:
        return False, (
            "Invalid Image. Please upload a clear front-facing facial image."
        )

    # Multiple faces
    if len(faces) > 1:
        return False, (
            "Invalid Image. Please upload an image containing only one face."
        )

    x, y, w, h = faces[0]

    # Face too small
    if w < 120 or h < 120:
        return False, (
            "Face is too small. Please upload a closer image."
        )

    return True, ""
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

    prediction = model.predict(
        img,
        verbose=0
    )

    probability = float(prediction[0][0])

    # Dataset:
    # autistic = 0
    # non_autistic = 1

    if probability < 0.5:
        result = "Autism Detected"
        confidence = (1 - probability) * 100
    else:
        result = "No Autism Detected"
        confidence = probability * 100

    return {
        "prediction": result,
        "confidence": round(confidence, 2)
    }