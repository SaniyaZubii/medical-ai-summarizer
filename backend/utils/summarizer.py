from transformers import pipeline

# Load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    # limit input size
    text = text[:1000]

    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    
    return summary[0]['summary_text']