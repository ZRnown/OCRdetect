import base64
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import cv2
import numpy as np
from PIL import Image
import io

# Disable Flask extra logging, show only errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)  # Allow CORS for userscript access

print("Initializing ddddocr model... (May download model on first run)")
# Try multiple model configurations to improve recognition accuracy
    try:
        # First try standard model
        ocr = ddddocr.DdddOcr(show_ad=False)
        print("Using standard ddddocr model")
    except Exception as e:
        print(f"Standard model loading failed, trying other configurations: {e}")
        try:
            # If standard model fails, try old=True parameter
            ocr = ddddocr.DdddOcr(show_ad=False, old=True)
            print("Using old ddddocr model")
        except Exception as e2:
            print(f"Old model also failed: {e2}")
            raise

print("Model loaded, OCR service started! Listening on port 5000")

def preprocess_image(img_bytes):
    """Image preprocessing to improve OCR recognition accuracy"""
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return img_bytes

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # Gaussian blur for noise reduction
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)

        # Morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Convert to bytes
        success, encoded_img = cv2.imencode('.png', cleaned)
        if success:
            return encoded_img.tobytes()
        else:
            return img_bytes

    except Exception as e:
        print(f"Image preprocessing failed, using original image: {e}")
        return img_bytes

@app.route('/ocr', methods=['POST'])
def ocr_process():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'code': '', 'msg': 'No image data'}), 400

        # Get Base64 string
        img_base64 = data['image']

        # Decode to binary
        img_bytes = base64.b64decode(img_base64)

        # Image preprocessing to improve recognition accuracy
        processed_img_bytes = preprocess_image(img_bytes)

        # Try multiple recognition methods
        results = []

        # 1. Use processed image recognition
        try:
            res_code = ocr.classification(processed_img_bytes)
            results.append(('processed', res_code))
        except Exception as e:
            print(f"Processed image recognition failed: {e}")

        # 2. Use original image recognition as fallback
        try:
            original_code = ocr.classification(img_bytes)
            results.append(('original', original_code))
        except Exception as e:
            print(f"Original image recognition failed: {e}")

        if not results:
            return jsonify({'code': '', 'msg': 'OCR recognition failed'}), 500

        # Choose the most likely result (simple selection of first successful)
        method, res_code = results[0]

        print(f"Recognition result [{method}]: {res_code}")

        print(f"Recognition successful: {res_code}")
        return jsonify({'code': res_code, 'msg': 'success'})

    except Exception as e:
        print(f"Recognition error: {e}")
        return jsonify({'code': '', 'msg': str(e)}), 500

if __name__ == '__main__':
    # Use waitress deployment, more stable and faster than Flask's built-in server
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000, threads=8)