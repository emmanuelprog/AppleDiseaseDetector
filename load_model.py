import os
import io
import json
import numpy as np
from PIL import Image
#from flask import Flask, request, jsonify, render_template, send_from_directory
from tensorflow.keras.models import load_model

#app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = 'uploads/' # Directory to temporarily store uploaded images
#app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
#if not os.path.exists(app.config['UPLOAD_FOLDER']):
#    os.makedirs(app.config['UPLOAD_FOLDER'])

# Preprocessing function for incoming images
IMG_HEIGHT = 224
IMG_WIDTH = 224
def preprocess_image(image_bytes):
    try:
        print("Preprocessing image...")
        # Open the image from bytes        
        image_array = np.array(image_bytes).astype('float32')

        image_array = image_array / 255.0 # Normalize pixel values to [0, 1]
        image_array = np.expand_dims(image_array, axis=0) # Add batch dimension
        print(f"Image preprocessed: shape {image_array.shape}")
        # Return the preprocessed image array
        return image_array
    except Exception as e:
        print(f"Error during image preprocessing: {e}")
        return None

import app
# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

