import streamlit as st 
from transformers import pipeline 
from datetime import datetime
import random 
import json 
import os

# ----------------- configuring layout----------------------
st.set_page_config(page_title="AI Mood Companion", layout="centered")
DATA_FILE = "journal.json"

# ---------------- Loading emotional model -----------------
@st.cache_resource
def load_em():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

emotion_model = load_em()

# ---------------------- Prompts ---------------------------
prompts = ["Who do you trust most? Why?",
            "What are your strengths in relationships (kindness, empathy, etc.)?",
            "How do you draw strength from loved ones?",
            "What do you value most in relationships (trust, respect, sense of humor, etc.)?",
            "What three important things have you learned from previous relationships?",
            "What five traits do you value most in potential partners?",
            "How do you use your personal strengths and abilities at work?",
            "How do your co-workers and supervisors recognize your strengths?",
            "How does work fulfill you? Does it leave you wanting more?",
            "What part of your workday do you most enjoy?",
            "What about your work feels real, necessary, or important to you?",
            "Do you see yourself in the same job in 10 years?",
            "What are your career ambitions?",
            "What values do you consider most important in life (honesty, justice, altruism, loyalty, etc.)? How do your actions align with those values?",
            "What three changes can you make to live according to your personal values?",
            "Describe yourself using the first 10 words that come to mind. Then, list 10 words that you’d like to use to describe yourself. List a few ways to transform those descriptions into reality.",
            "What do you appreciate most about your personality? What aspects do you find harder to accept?", 
            "Describe your favorite thing to do when feeling low.",
            "What three ordinary things bring you the most joy?",
            "List three strategies that help you stay present in your daily routines. Then, list three strategies to help boost mindfulness in your life.",
            "How do you prioritize self-care?",
            "Describe two or three things you do to relax.",
            "What aspects of your life are you most grateful for?"]

# ---------------------- Saving Data in File ---------------------------
def save_entry(entry_text, mood_score, emotion, confidence):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "prompt": st.session_state.get("prompt", ""), 
        "entry": entry_text, 
        "mood_score": mood_score, 
        "emotion": emotion, 
        "confidence": round(confidence, 2)
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: 
            data.json.load(f)
    else: 
        data = []
    data.append(entry)

    with open(DATA_FILE, "w") as f: 
        json.dump(data, f, indent=4)

# ---------------------- Application UI ---------------------------
st.title("SafenSecure")  
st.subheader("AI Mental Health Buddy")

if "prompt" not in st.session_state:
    st.session_state.prompt = random.choice(prompts)

st.info(f"Reflection Prompt: {st.session_state.prompt}")


journal = st.text_area("How was your day?", height=200)
mood = st.slider("Rate your mood today: ", 1,10,5)

if st.button("Analyze"):
    if journal.strip():
        result = emotion_model(journal)[0]
        detected_emotion = result['label']
        confidence = result["score"]
    else:
        st.warning("Please write something before analyzing.")

# ---------------------- View Entries ---------------------------
with st.expander("View Saved Entries"):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            entries = json.load(f)
        for entry in reversed(entries[-5:]):  # show last 5
            st.markdown(f"""
            **🗓 Date:** {entry['date']}  
            **Prompt:** {entry['prompt']}  
            **Mood (1–10):** {entry['mood_score']}  
            **Detected Emotion:** *{entry['emotion']}* (Confidence: {entry['confidence']})  
            **Entry:**  
            {entry['entry']}
            ---
            """)
    else:
        st.write("No entries yet.")
