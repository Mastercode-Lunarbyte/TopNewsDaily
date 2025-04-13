#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# classifier.py

def classify_topic(title):
    title = title.lower()
    if any(word in title for word in ['دلار', 'بورس', 'نرخ', 'بانک']):
        return 'اقتصادی'
    elif any(word in title for word in ['وزیر', 'دولت', 'مجلس', 'انتخابات']):
        return 'سیاسی'
    elif any(word in title for word in ['فوتبال', 'والیبال', 'مدال', 'بازی']):
        return 'ورزشی'
    else:
        return 'سایر'

