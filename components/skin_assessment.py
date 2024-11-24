import streamlit as st
from PIL import Image
from utils.constants import severity_scale
from models.image_model import classify_image
from models.chat_model import get_recommendations

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def skin_assessment():
    st.subheader("Skin Assessment")

    # Image Upload/Camera
    photo = None
    photo_choice = st.radio("Select how you want to provide the image:", ["Upload an Image", "Use Camera"])
    if photo_choice == "Upload an Image":
        photo = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if photo:
            photo = Image.open(photo)
            st.write("Your photo was successfully uploaded.")
    elif photo_choice == "Use Camera":
        picture = st.camera_input("Take a picture")
        if picture:
            photo = Image.open(picture)
            st.write("Your photo was successfully uploaded.")

    # Survey Form
    st.write("Please fill out the survey to help analyze your skin.")
    answers = {
        "age": st.slider("What is your age?", 18, 100, 25),
        "gender": st.radio("What is your gender?", ["Male", "Female"]),
        "skin_type": st.radio("What is your skin type?", ["Dry", "Oily", "Combination", "Sensitive"]),
        "skin_condition": st.radio("Do you have any skin conditions?", ["Yes", "No"]),
        "breakouts": st.radio("How often do you experience breakouts?", ["Rarely", "Occasionally", "Frequently"]),
        "skin_concerns": st.text_input("Do you have any specific skin concerns?", "Acne"),
        "sensitivity": st.radio("Are you sensitive to certain ingredients?", ["Yes", "No"]),
        "routine": st.radio("What is your skincare routine?", ["Basic", "Moderate", "Extensive"]),
        "makeup": st.radio("Do you wear makeup?", ["Daily", "Occasionally", "Rarely"]),
        "allergies": st.text_input("Do you have any allergies?", "None"),
        "diet": st.radio("What is your diet?", ["Healthy", "Moderate", "Unhealthy"]),
        "water": st.radio("How much water do you drink daily?", ["1-2L", "2-3L", "3-4L"]),
        "sleep": st.radio("How many hours of sleep do you get daily?", ["5-7 hours", "7-9 hours", "9-11 hours"]),
    }

    if st.button("Submit and get recommendations"):
        if photo:
            st.write("Classifying...")
            results = classify_image(photo)
            recommendations = get_recommendations(answers, results, severity_scale)
            st.write("Your personalized recommendations are ready:")
            st.write(recommendations)
        else:
            st.write("Please upload a photo.")
