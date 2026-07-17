# 🧩 Autism Prediction System

An AI-powered web application for **early Autism Spectrum Disorder (ASD) screening** using **Behavioral Assessment** and **Facial Image Analysis**. The system also provides **personalized AI wellness guidance** and recommends **nearby autism centers or hospitals** based on the user's location.

---

## 📖 Overview

Early identification of Autism Spectrum Disorder (ASD) is crucial for timely intervention and better developmental outcomes. This project combines Machine Learning and Deep Learning techniques to provide an intelligent preliminary screening system.

The application consists of two independent prediction modules:

- **Behavioral Assessment** using an XGBoost Machine Learning model
- **Facial Image Analysis** using a ResNet50 Deep Learning model

The system also generates AI-powered wellness guidance and recommends nearby autism centers or hospitals using OpenStreetMap.

> **Disclaimer:** This application is intended only for preliminary screening and educational purposes. It is **not a substitute for professional medical diagnosis.**

---

# ✨ Features

- ✅ Behavioral Autism Screening
- ✅ Facial Image Autism Screening
- ✅ AI-generated Personalized Wellness Guidance
- ✅ Nearby Autism Centre Recommendation
- ✅ Hospital Recommendation (Fallback)
- ✅ Face Validation before Prediction
- ✅ Modern Responsive Flask Web Interface
- ✅ Medical Disclaimer
- ✅ Interactive Bootstrap UI

---


# 🏗️ System Architecture

```
                User

                  │

                  ▼

         Flask Web Application

        ┌──────────┴──────────┐

        ▼                     ▼

Behavioral Model       Facial Image Model

(XGBoost)                 (ResNet50)

        │                     │

        └──────────┬──────────┘

                   ▼

          Final Prediction Result

                   │

        ┌──────────┴──────────┐

        ▼                     ▼

AI Wellness          Hospital Recommendation

(Gemini AI)          (OpenStreetMap API)
```

---

# 🚀 Technologies Used

### Programming Language

- Python 3.x

### Backend

- Flask

### Machine Learning

- XGBoost
- Scikit-learn

### Deep Learning

- TensorFlow
- Keras
- ResNet50

### Computer Vision

- OpenCV

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### APIs

- Google Gemini API
- OpenStreetMap
- Nominatim API
- Overpass API

---

# 📂 Project Structure

```
AutismPredictionSystem/

│

├── app.py

├── models/

│   ├── behavior_model.pkl

│   └── resnet50_best.keras

│

├── static/

│   ├── css/

│   ├── uploads/

│   └── images/

│

├── templates/

│   ├── index.html

│   ├── questionnaire.html

│   ├── final_result.html

│   ├── wellness.html

│   ├── wellness_questions.html

│   └── hospital_results.html

│

├── utils/

│   ├── behavioral_predict.py

│   ├── image_predict.py

│   ├── gemini_service.py

│   ├── hospital_locator.py

│   └── prompts.py

│

├── requirements.txt

└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/haritha0609/AutismPredictionSystem.git
```

---

## Navigate into Project

```bash
cd AutismPredictionSystem
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python app.py
```

---

Open browser:

```
http://127.0.0.1:5000
```

---

# 🧠 Machine Learning Model

### Algorithm

- XGBoost Classifier

### Input Features

- A1 – A10 Behavioral Questions
- Age
- Gender
- Jaundice History
- Family History of ASD

### Output

- High Risk
- Low Risk

---

# 👁️ Deep Learning Model

### Architecture

ResNet50

### Input

Facial Image

### Output

- Autism Detected
- No Autism Detected

---

# 🤖 AI Wellness Guidance

The application uses **Google Gemini AI** to generate personalized recommendations based on:

- Child's age
- Behavioral responses
- Facial screening result
- Parent concerns

If Gemini is unavailable, the system automatically provides a default wellness guidance plan.

---

# 🏥 Hospital Recommendation

The application recommends nearby autism centers using:

- OpenStreetMap
- Nominatim Geocoder
- Overpass API

If autism-specific centers are unavailable, nearby hospitals are displayed automatically.

---

# 📊 Workflow

```
Home Page

      │

      ▼

Behavioral Questionnaire

      │

      ▼

Behavioral Prediction

      │

      ▼

Upload Facial Image

      │

      ▼

Facial Prediction

      │

      ▼

Final Screening Result

      │

 ┌────┴────┐

 ▼         ▼

AI Plan   Hospitals
```

---

# 📌 Future Improvements

- User Authentication
- PDF Report Generation
- Email Report
- Doctor Appointment Booking
- Multi-language Support
- Mobile Application
- Cloud Deployment
- Medical Dashboard

---

# ⚠️ Disclaimer

This project is intended for educational and research purposes only.

The prediction generated by this application is **not a medical diagnosis**. Users are advised to consult qualified healthcare professionals for comprehensive evaluation and diagnosis.

---

# 👩‍💻 Developer

**Matta Haritha**

B.Tech Computer Science and Engineering

Shri Vishnu Engineering College for Women

GitHub: https://github.com/haritha0609

---

# ⭐ Support

If you found this project useful,

please consider giving it a ⭐ on GitHub.
