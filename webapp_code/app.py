import streamlit as st
from PIL import Image
import pickle
import numpy as np
import sklearn
from pyexpat import features

model = pickle.load(open('Forest_cover_model.sav', 'rb'))

st.markdown(
    """
    <h1 style='text-align: center; color: #2E8B57;'>
        Forest Coverage Type Predictor
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Change main page background color */
    .stApp {
        background-color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

image = Image.open('mainimage2.jpg')
st.image(image, use_container_width=True)
user_input = st.text_input("Enter the values")

if user_input:
    user_input = user_input.split(',')
    features = np.array(user_input, dtype=np.float32).reshape(1, -1)
    output = model.predict(features)

    cover_type_dict = {
        0: {"name": "Spruce/Fir", "image": "Spruce,Fir.jpg"},
        1: {"name": "Lodgepole Pine", "image": "lodgepole.jpg"},
        2: {"name": "Ponderosa Pine", "image": "Ponderosa.jpg"},
        3: {"name": "Cottonwood/Willow", "image": "Cottonwood,Willow.jpg"},
        4: {"name": "Aspen", "image": "Aspen.jpg"},
        5: {"name": "Douglas-fir", "image": "Douglas.jpg"},
        6: {"name": "Krummholz", "image": "Krummholz.jpg"}
    }

    prediction = output[0]
    prediction_info = cover_type_dict[prediction]

    if prediction_info is not None:
        forest_name = prediction_info["name"]
        forest_image = prediction_info["image"]

        col1, col2 = st.columns(2)
        with col1:
            st.write("Predicted Forest Coverage")
            st.write(f"<h1 style='font-size: 40px; font-weight: bold;'>{forest_name}</h1>", unsafe_allow_html=True)
        with col2:
            cover_image = Image.open(forest_image)
            st.image(cover_image, use_container_width=True)
    else :
        st.write("No prediction available")
