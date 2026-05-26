import streamlit as st
from google import genai
import os
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo_ds.png")

# URL corrigée (avec guillemets)
N8N_WEBHOOK_URL = "https://primary-production-b36e9.up.railway.app/webhook/samira-whatsapp"

def interroger_n8n(texte_samira, client_prompt):
    payload = {"agent": "Samira", "message": texte_samira, "question_client": client_prompt}
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("output", texte_samira)
        return texte_samira
    except Exception:
        return texte_samira

# --- DESIGN CSS ---
st.markdown("""
    <style>
    .header-container { background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); padding: 25px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 25px; }
    .stChatMessage { border-radius: 15px !important; margin-bottom: 15px !important; }
    .stButton>button { background-color: #218838 !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>DS DIGITAL HUB</h1><p>L\'excellence numérique à Bobo-Dioulasso</p></div>', unsafe_allow_html=True)

# --- LOGIQUE ---
with st.sidebar:
    st.title("Menu Agency")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse de votre demande..."):
            try:
                # Initialisation Client Gemini
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model=gemini-1.5-flash,
                    contents=f"Ton nom est Samira, experte chez DS Digital Hub. Réponds à : {prompt}"
                )
                
                texte_final = interroger_n8n(response.text, prompt)
                st.markdown(texte_final)
                st.session_state.messages.append({"role": "assistant", "content": texte_final})
                
            except Exception as e:
                st.error(f"Erreur technique : {str(e)}")
