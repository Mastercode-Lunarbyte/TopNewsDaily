from transformers import pipeline

# مدل سبک‌تر T5
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def summarize_text(text, max_length=100, min_length=30):
    try:
        if len(text) < 100:
            return text

        # برش متن به 512 کاراکتر، چون t5-small محدودیت داره
        text = text[:512]

        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    
    except Exception as e:
        print(f"❌ خطا در خلاصه‌سازی متن: {e}")
        return text[:300] + "..."
