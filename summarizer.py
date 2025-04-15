#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# summarizer.py

# summarizer.py

def summarize_text(text):
    if len(text) <= 300:
        return text
    else:
        return text[:300] + "..."


