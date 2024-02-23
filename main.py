import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Constants
img_height = 64
img_width = 64  # You can adjust these values based on your image size

# Define the model architecture
def create_candlestick_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# Load pre-trained model weights
model = create_candlestick_model()
model.load_weights('candlestick_model_weights.h5')

# Function to predict candlestick direction
def predict_candlestick_direction(img):
    img = cv2.resize(img, (img_height, img_width))
    img = img / 255.0  # Normalize pixel values to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    prediction = model.predict(img)
    return prediction[0][0]

# Function to analyze stock trend based on prediction
def analyze_stock_trend(prediction):
    if prediction > 0.5:
        return "The stock is predicted to go up."
    else:
        return "The stock is predicted to go down."

# Streamlit app
def main():
    st.title("Stock Trend Analysis Chatbot")

    choice = st.sidebar.selectbox("Choose an option", ["Upload Image", "Exit"])

    if choice == "Upload Image":
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            prediction = predict_candlestick_direction(image)
            trend_analysis = analyze_stock_trend(prediction)
            
            st.subheader("Analysis Result:")
            st.write(trend_analysis)

    elif choice == "Exit":
        st.write("Thank you for using the Stock Trend Analysis Chatbot!")

if __name__ == "__main__":
    main()
