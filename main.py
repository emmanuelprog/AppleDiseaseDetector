from app import app, load_ml_artifacts

if __name__ == '__main__':
    # Load model and labels when the Flask app starts
    load_ml_artifacts()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
