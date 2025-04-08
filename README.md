# 📈 Stock Trend Analysis Bot

A **Streamlit** web app that uses a **Convolutional Neural Network (CNN)** to predict stock price direction based on candlestick chart images. This tool allows users to upload an image of a candlestick chart and receive a prediction indicating whether the stock is expected to go up or down.

---

## 🚀 Features

- Upload candlestick chart images (`.jpg`, `.jpeg`, `.png`)
- Predicts whether the stock trend is **up** or **down**
- Powered by a CNN trained on candlestick chart patterns
- Clean and interactive Streamlit user interface

---

## 🧠 Model Architecture

The app uses a simple CNN model built with TensorFlow/Keras:

- Conv2D layers with ReLU activation
- MaxPooling for downsampling
- Dense layers for prediction
- Sigmoid activation for binary classification (up/down)

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/vanshgurnani/profit-pandit.git
cd profit-pandit
```

2. **Install dependencies**

We recommend using a virtual environment:

```bash
pip install -r requirements.txt
```

3. **Add the model weights**

Ensure you have a file named `candlestick_model_weights.h5` in the root directory. This file contains the pre-trained weights for the CNN model.

---

## ▶️ Running the App

Start the Streamlit app with the following command:

```bash
streamlit run app.py
```

The app will launch in your browser. Use the sidebar to upload candlestick chart images and receive trend predictions.

---

## 🗂️ Project Structure

```
.
├── app.py                     # Main Streamlit app
├── candlestick_model_weights.h5  # Trained model weights (required)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 📝 Example Usage

1. Launch the app.
2. Upload an image of a candlestick chart.
3. The app predicts and displays whether the stock will go **up** or **down**.

---

## 🔧 Requirements

- Python 3.7+
- TensorFlow
- NumPy
- OpenCV
- Streamlit

Install via:

```bash
pip install streamlit opencv-python tensorflow numpy
```

---
