import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CIFAR-10 Image Classifier",
    page_icon="🖼️",
    layout="centered"
)

# Title
st.title("🖼️ CIFAR-10 Image Classifier")
st.write("Upload an image and let the model predict its class.")

# Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.h5", compile=False)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# CIFAR-10 class labels
class_names = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]

# Upload image
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Uploaded Image")
    st.image(image, caption="Your image", use_container_width=True)

    # Preprocessing
    processed_image = image.resize((224, 224))
    image_array = np.array(processed_image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Prediction
    if st.button("🔍 Predict Image"):

        with st.spinner("Making prediction..."):
            predictions = model.predict(image_array, verbose=0)

        probabilities = predictions[0]
        predicted_index = np.argmax(probabilities)
        predicted_class = class_names[predicted_index]
        confidence = probabilities[predicted_index] * 100

        st.success(f"Prediction: **{predicted_class.upper()}**")
        st.info(f"Confidence: **{confidence:.2f}%**")

        # Display top 3 predictions
        st.subheader("Top 3 Predictions")

        top_indices = np.argsort(probabilities)[-3:][::-1]

        results = []

        for index in top_indices:
            results.append({
                "Class": class_names[index],
                "Confidence": f"{probabilities[index] * 100:.2f}%"
            })

        results_df = pd.DataFrame(results)
        st.table(results_df)
