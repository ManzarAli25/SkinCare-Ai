import streamlit as st
from components.skin_assessment import skin_assessment
from components.chatbot import chatbot

# Sidebar Navigation
opt = st.sidebar.radio("", options=("Begin Skin Assessment", "Talk to SkinGenie"))

if opt == "Begin Skin Assessment":
    skin_assessment()
elif opt == "Talk to SkinGenie":
    chatbot()
