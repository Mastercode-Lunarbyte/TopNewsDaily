from transformers import pipeline

# بارگذاری تنها یک‌بار هنگام اجرای سرور
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_length=130, min_length=30):
    try:
        if len(text) < 100:
            return text

        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    
    except Exception as e:
        print(f"❌ خطا در خلاصه‌سازی متن: {e}")
        return text[:1000] + "..."
