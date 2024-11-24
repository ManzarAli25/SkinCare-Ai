from transformers import pipeline
import streamlit as st
from streamlit_chat import message
from PIL import Image
import json
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Initialize environment
st.title("FYP BME 2021F")
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# Load model and initialize Google Generative AI
pipe = pipeline("image-classification", model="imfarzanansari/skintelligent-acne")
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None, timeout=None, max_retries=2)

# Severity scale
severity_scale = {
    "Severity Levels": {
        "-1": "Clear Skin",
        "0": "Occasional Spots",
        "1": "Mild Acne",
        "2": "Moderate Acne",
        "3": "Severe Acne",
        "4": "Very Severe Acne"
    }
}

# Sidebar options
opt = st.sidebar.radio("", options=("Begin Skin Assessment", "Talk to SkinGenie"))

if opt == "Begin Skin Assessment":
    st.subheader("Skin Assessment")

    # Step 1: Photo Upload
    photo_choice = st.radio(
        "Select how you want to provide the image:",
        ("Upload an Image", "Use Camera")
    )
    
    photo = None
    if photo_choice == "Upload an Image":
        uploaded_photo = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_photo:
            photo = Image.open(uploaded_photo)
            st.image(photo, caption="Uploaded Photo", use_column_width=True)
            if st.button("Confirm Photo"):
                st.success("Photo confirmed. Proceed to the questionnaire!")
        else:
            st.warning("Please upload a photo to proceed.")
    
    elif photo_choice == "Use Camera":
        taken_photo = st.camera_input("Take a picture")
        if taken_photo:
            photo = Image.open(taken_photo)
            st.image(photo, caption="Captured Photo", use_column_width=True)
            if st.button("Confirm Photo"):
                st.success("Photo confirmed. Proceed to the questionnaire!")
        else:
            st.warning("Please take a photo to proceed.")

    # Step 2: Questionnaire
    if photo is not None:
        st.write("Please fill out the following survey to help us analyze your skin type and provide recommendations.")
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

        if st.button("Submit Questionnaire"):
            st.success("Questionnaire submitted successfully! Generating recommendations...")

            # Step 3: Get Recommendations
            with st.spinner("Classifying..."):
                results = pipe(photo)
                prompt = f"""
                You are a skincare and wellness expert.
                Based on the following user-provided information, analyze their skin type, lifestyle, and dietary habits.
                Provide personalized dietary and lifestyle recommendations to help improve their skin health and address their specific skin concerns.
                ADDITIONAL INFORMATION:
                {json.dumps(answers, indent=4)}
                ACNE SEVERITY:
                {json.dumps(results, indent=4)}
                HOW TO INTERPRET THE RESULTS:
                {json.dumps(severity_scale, indent=4)}
                """
                recommendations = gemini.invoke(prompt)
            
            st.subheader("Your Personalized Recommendations")
            st.write(recommendations.content)

elif opt == "Talk to SkinGenie":
    st.subheader("Talk to SkinGenie")

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="""You are a skincare and wellness expert with extensive knowledge of skin types, 
            common skin issues, product recommendations, and holistic wellness practices. 
            Provide evidence-based advice tailored to individual needs, 
            considering factors like age, skin type, and lifestyle. 
            Use simple, clear language to explain concepts and offer actionable tips.""")
        ]

    st.header("Chat with SkinGenie")

    # Sidebar with user input
    user_input = st.sidebar.text_input("Your message: ", key="user_input")
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = gemini.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # Display message history
    for i, msg in enumerate(st.session_state.messages[1:]):
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True, key=f"user_{i}")
        else:
            message(msg.content, is_user=False, key=f"ai_{i}")
