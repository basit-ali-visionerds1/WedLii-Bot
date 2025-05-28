# streamlit_app.py
import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Wedding Bot", layout="centered")

# Backend API URL
API_URL = "http://localhost:8000/chat"

# Valid user IDs (from users_data.py)
VALID_USERS = ["user1", "user2", "user3", "user4", "user5"]

# UI Components
st.title("💍 Wedding Assistant Bot")
st.markdown("Update your wedding details or ask questions!")

# User input form
with st.form(key="chat_form"):
    user_id = st.selectbox("Select Your User ID", options=VALID_USERS)
    user_message = st.text_input("Your Message (e.g., 'Change budget to 20000'):")
    submit_button = st.form_submit_button(label="Send")

# Handle form submission
if submit_button:
    if not user_message.strip():
        st.error("Please enter a message!")
    else:
        # Prepare request payload
        payload = {
            "user_id": user_id,
            "message": user_message
        }
        
        try:
            # Send request to FastAPI backend
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # Raise HTTP errors
            
            # Display bot reply
            bot_reply = response.json().get("reply", "No response from bot.")
            st.success(f"Bot: {bot_reply}")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with backend: {str(e)}")