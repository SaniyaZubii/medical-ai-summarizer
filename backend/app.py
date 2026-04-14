from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

app = Flask(__name__)
CORS(app)

# --- Configuration ---
# Get your token from https://huggingface.co/settings/tokens
# For now, it will work without one, but it's slower.
HF_TOKEN = os.getenv("HF_TOKEN", "") 
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def query_hf_api(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 150, "min_length": 50, "do_sample": False}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Hugging Face sometimes returns a list or a dict depending on the state
    result = response.json()
    if isinstance(result, list):
        return result[0]['summary_text']
    return "Error: Could not retrieve summary. Hugging Face might be loading the model."

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = "temp.pdf"
    file.save(file_path)

    text = ""
    try:
        # Try direct text extraction first
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()

        # If no text found, use OCR
        if not text.strip():
            images = convert_from_path(file_path)
            for img in images:
                text += pytesseract.image_to_string(img)
                
        if not text.strip():
            return jsonify({"error": "No text could be extracted from the PDF"}), 400

        # Use the API instead of the local model
        summary = query_hf_api(text[:3000]) # Truncate text to avoid API limits
        
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)