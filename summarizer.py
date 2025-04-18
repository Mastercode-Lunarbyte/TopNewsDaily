# summarizer.py

def summarize_text(text):
    if len(text) <= 1000:
        return text
    else:
        return text[:1000] + "..."
