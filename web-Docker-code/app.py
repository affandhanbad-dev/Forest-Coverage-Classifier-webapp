import streamlit as st
from PIL import Image
import pickle
import numpy as np

model = pickle.load(open('Forest_cover_model.sav', 'rb'))

st.set_page_config(
    page_title="🌲 Forest Coverage Type Predictor",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #2F4F4F, #006400);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        text-align: center;
        color: #FFD700;
        text-shadow: 1px 1px 2px black;
    }
    .stTextInput > div > div > input {
        background-color: #222;
        color: #00FFB3;
        border-radius: 10px;
        border: 2px solid #00FFB3;
        font-weight: bold;
    }
    .block-container {
        padding-top: 2rem;
    }
    .result {
        font-size: 36px;
        font-weight: 800;
        color: #00FFB3;
        text-shadow: 2px 2px 4px black;
    }
    img {
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(255,255,255,0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌲 Forest Coverage Type Predictor 🌲</h1>", unsafe_allow_html=True)
st.write("### Enter your input values (comma-separated) to predict the forest cover type.")

image = Image.open('assets/mainimage.jpg')
st.image(image, use_container_width=True)

user_input = st.text_input("🧮 Enter the feature values (comma-separated):", placeholder="Example: 2596,51,3,258,0,510,...")

if user_input:
    try:
        user_input = user_input.split(',')
        features = np.array(user_input, dtype=np.float32).reshape(1, -1)
        output = model.predict(features)
        cover_type_dict = {
            0: {"name": "Spruce/Fir", "image": "assets/Spruce,Fir.jpg"},
            1: {"name": "Lodgepole Pine", "image": "assets/lodgepole.jpg"},
            2: {"name": "Ponderosa Pine", "image": "assets/Ponderosa.jpg"},
            3: {"name": "Cottonwood/Willow", "image": "assets/Cottonwood,Willow.jpg"},
            4: {"name": "Aspen", "image": "assets/Aspen.jpg"},
            5: {"name": "Douglas-fir", "image": "assets/Douglas.jpg"},
            6: {"name": "Krummholz", "image": "assets/Krummholz.jpg"}
        }
        prediction = int(output[0])
        prediction_info = cover_type_dict.get(prediction, None)
        if prediction_info:
            forest_name = prediction_info["name"]
            forest_image = prediction_info["image"]
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("<p style='font-size:22px;'>🌿 Predicted Forest Type:</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='result'>{forest_name}</p>", unsafe_allow_html=True)
            with col2:
                cover_image = Image.open(forest_image)
                st.image(cover_image, use_container_width=True)
        else:
            st.error("⚠️ Prediction could not be determined.")
    except Exception as e:
        st.error("❌ Invalid input format. Please enter only numbers separated by commas.")
        st.write(e)