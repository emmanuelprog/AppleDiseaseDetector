import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import uuid
from datetime import datetime
from PIL import Image
import json 
from load_model import preprocess_image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model 

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-12345")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///apple_disease.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}


# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize the app with the extension
db.init_app(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Global variables for model and class labels ---
model = None
class_labels = None
IMG_HEIGHT = 224
IMG_WIDTH = 224

# Function to load the Keras model and class labels
def load_ml_artifacts():
    global model, class_labels
    try:
        model_path = os.path.join('model', 'best_model.keras')
        model = load_model(model_path)
        # It's crucial to compile the model after loading if you plan to train further
        # or if the saved_model format did not store the optimizer state in a way
        # that allows direct inference for all TensorFlow versions.
        # For inference only, usually `compile=False` is fine during load.
        # If issues arise, try: model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print(f"Keras model loaded from: {model_path}")

        labels_path = os.path.join('model', 'class_labels.json')
        with open(labels_path, 'r') as f:
            class_labels_dict = json.load(f)
            # Convert keys back to int if they were stored as strings
            class_labels = [class_labels_dict[str(i)] for i in range(len(class_labels_dict))]
        print(f"Class labels loaded: {class_labels}")

    except Exception as e:
        print(f"Error loading ML artifacts: {e}")
        model = None
        class_labels = [] # Set to empty list to prevent errors if not loaded
        # In a production app, you might want to raise an error or halt.

load_ml_artifacts()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_path):
    """Validate that the uploaded file is a valid image"""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception as e:
        logging.error(f"Image validation failed: {e}")
        return False

def get_session_id():
    """Get or create a session ID for tracking user history"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()

# Import disease detector
#from disease_detector import AppleDiseaseDetector

#detector = AppleDiseaseDetector()

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and disease detection"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        print(f"Received file: {file.filename}")

        # Check if file is empty
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not file or not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or WEBP images only.', 'error')
            return redirect(url_for('index'))
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        print(f"Saving file to: {file_path}")
        # Save file
        file.save(file_path)
        
        # Validate image
        if not validate_image(file_path):
            os.remove(file_path)
            flash('Invalid image file. Please upload a valid image.', 'error')
            return redirect(url_for('index'))
        
        print(f"File saved successfully: {file_path}")

        # detect using model 
        if file and allowed_file(file.filename):
            try:
                img_bytes = tf.keras.utils.load_img(file_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
                # debugging
                print(f"Type of img_bytes: {type(img_bytes)}")

                # Preprocess the image
                #img_bytes = file.read()
                processed_image = preprocess_image(img_bytes)

                # Get session ID for history tracking
                session_id = get_session_id()

                # debugging
                print(f"Type of model before prediction: {type(model)}")
                print(f"Value of model before prediction: {model}")
                print(f"Type of processed_image: {type(processed_image)}")

                # Make prediction
                predictions = model.predict(processed_image) # Get probabilities for the single image
                
                print(f"Predictions: {predictions}")
                # Get the predicted class and confidence
                predicted_class_idx = np.argmax(predictions, axis=1)[0]
                print(f"Predicted class index: {predicted_class_idx}")
                predicted_class_name = class_labels[predicted_class_idx]
                print(f"Predicted class name: {predicted_class_name}")
                confidence = float(predictions[0][predicted_class_idx]) * 100 # Convert to percentage
                print(f"Confidence: {confidence:.2f}%")                

                # Prepare all class probabilities for a more detailed response
                #all_probabilities = {class_labels[i]: float(predictions[i]) * 100 for i in range(len(class_labels))}
                #print(f"All probabilities: {all_probabilities}")
                
                # Save to history
                detection = models.Detection(
                    session_id=session_id,
                    filename=unique_filename,
                    original_filename=filename,
                    disease_type=predicted_class_name,
                    confidence=confidence,
                    timestamp=datetime.utcnow()
                )
                db.session.add(detection)
                db.session.commit()
                
                return redirect(url_for('result', detection_id=detection.id))
                        
            except Exception as e:
                # Clean up file if processing fails
                if os.path.exists(file_path):
                    os.remove(file_path)
                logging.error(f"Disease detection failed: {e}")
                flash('Error processing image. Please try again.', 'error')
                return redirect(url_for('index'))
        
    except Exception as e:
        logging.error(f"Upload failed: {e}")
        flash('Upload failed. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/result/<int:detection_id>')
def result(detection_id):
    """Display detection result"""
    print(f"Loading result for detection ID: {detection_id}")
    try:
        detection = models.Detection.query.get_or_404(detection_id)
        print(f"Loaded detection: {detection}")
        
        # Check if this detection belongs to the current session
        session_id = get_session_id()
        if detection.session_id != session_id:
            flash('Detection not found', 'error')
            return redirect(url_for('index'))
        
        return render_template('result.html', detection=detection)
    
    except Exception as e:
        logging.error(f"Error loading result: {e}")
        flash('Error loading result', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """Display user's detection history"""
    try:
        session_id = get_session_id()
        
        # Get page number for pagination
        page = request.args.get('page', 1, type=int)
        per_page = 12  # Number of items per page
        
        # Query detections for this session with pagination
        detections = models.Detection.query.filter_by(session_id=session_id)\
                                           .order_by(models.Detection.timestamp.desc())\
                                           .paginate(
                                               page=page,
                                               per_page=per_page,
                                               error_out=False
                                           )
        
        return render_template('history.html', detections=detections)
    
    except Exception as e:
        logging.error(f"Error loading history: {e}")
        flash('Error loading history', 'error')
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logging.error(f"Internal server error: {e}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_ml_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
