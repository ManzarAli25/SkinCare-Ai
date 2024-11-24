import streamlit as st
from streamlit_chat import message
from models.chat_model import gemini_chat

def chatbot():
    st.subheader("Talk to SkinGenie")

    # Initialize Message History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="""You are a skincare and wellness expert with extensive knowledge of skin types, 
                          common skin issues, product recommendations, and holistic wellness practices. 
                          Provide evidence-based advice tailored to individual needs, 
                          considering factors like age, skin type, and lifestyle.
                           Use simple, clear language to explain concepts and offer actionable tips.""")
        ]

    # User Input
    user_input = st.text_input("Your message: ", key="user_input")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = gemini_chat(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Display Messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            message(msg["content"], is_user=True)
        else:
            message(msg["content"], is_user=False)
