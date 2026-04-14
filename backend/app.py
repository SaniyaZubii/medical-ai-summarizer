from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils.pdf_reader import extract_text_from_pdf

app = Flask(__name__)
CORS(app)

# 1. Load a Lighter, Faster Model (Fits in 512MB RAM)
model_name = "sshleifer/distilbart-cnn-12-6" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_chunk(text):
    """Helper function to summarize individual pieces of text"""
    inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

@app.route('/')
def home():
    return "Medical Summarizer Backend is Active"

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    # Create the utils folder if it doesn't exist to avoid saving errors
    if not os.path.exists("utils"):
        os.makedirs("utils")
        
    temp_path = os.path.join("utils", file.filename)
    file.save(temp_path)
    
    try:
        # 2. Extract text using your utility function
        # We call it 'full_text' here to avoid 'text is not defined' errors
        full_text = extract_text_from_pdf(temp_path)
        
        # Clean up the file immediately after reading
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # 3. Validation Check
        if not full_text or len(full_text) < 50:
            return jsonify({"error": "PDF text too short or unreadable. Is it a scanned image?"}), 400

        # 4. CHUNKING: Split long text (3000 chars per chunk)
        chunks = [full_text[i:i+3000] for i in range(0, len(full_text), 3000)]
        
        # Summarize each chunk and join them together
        summaries = [summarize_chunk(c) for c in chunks]
        final_result = " ".join(summaries)
        
        return jsonify({"summary": final_result})

    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        return jsonify({"error": "An internal error occurred during analysis"}), 500

if __name__ == "__main__":
    # use_reloader=False is critical for Windows to prevent the model loading twice
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)