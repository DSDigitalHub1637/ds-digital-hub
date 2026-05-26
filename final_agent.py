import streamlit as st
from google import genai
import os
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")
N8N_WEBHOOK_URL = "https://primary-production-b36e9.up.railway.app/webhook/samira-whatsapp"

def interroger_n8n(texte_samira, client_prompt):
    """Envoie la réponse à n8n et attend la validation."""
    payload = {"agent": "Samira", "message": texte_samira, "question_client": client_prompt}
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("output", texte_samira)
        return texte_samira
    except:
        return texte_samira

# --- UI & DESIGN ---
st.markdown("""
    <style>
    .header-container { background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>DS DIGITAL HUB</h1></div>', unsafe_allow_html=True)

# --- MÉMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- GESTION IA ---
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Initialisation Client (plus stable)
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Utilisation du modèle 1.5 Flash (meilleur équilibre quota/performance)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Tu es Samira de DS Digital Hub. Réponds à : {prompt}"
            )
            
            texte_final = interroger_n8n(response.text, prompt)
            st.markdown(texte_final)
            st.session_state.messages.append({"role": "assistant", "content": texte_final})
            
        except Exception as e:
            st.error("Service indisponible temporairement. Veuillez réessayer dans quelques instants.")
