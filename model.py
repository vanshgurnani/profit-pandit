import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# Define image dimensions
img_height = 64
img_width = 64

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

# Load and preprocess images and labels
def load_data(base_dir):
    images = []
    labels = []
    for label, folder in enumerate(['down', 'up']):
        folder_path = os.path.join(base_dir, folder)
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                img_path = os.path.join(folder_path, filename)
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Failed to read image: {img_path}")
                    continue
                img = cv2.resize(img, (img_height, img_width))
                img = img / 255.0
                images.append(img)
                labels.append(label)
    return np.array(images), np.array(labels).reshape(-1, 1)

# Load all data
base_directory = './img_candel_stick/Train'
all_images, all_labels = load_data(base_directory)

# Split the data into training and validation sets
train_images, val_images, train_labels, val_labels = train_test_split(
    all_images, all_labels, test_size=0.2, random_state=5
)

# Create and compile the model
model = create_candlestick_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=10, validation_data=(val_images, val_labels))

# Evaluate the model on the validation set
loss, accuracy = model.evaluate(val_images, val_labels)
print(f"Validation Loss: {loss}, Validation Accuracy: {accuracy}")

# Save the trained model weights
model.save_weights('candlestick_model_weights.h5')
