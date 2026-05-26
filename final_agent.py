import streamlit as st
from google import genai
import os
import requests

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo_ds.png")

# Configuration du webhook n8n (URL de production)
N8N_WEBHOOK_URL = "https://primary-production-b36e9.up.railway.app/webhook/samira-whatsapp"

def interroger_n8n(texte_samira, client_prompt):
    """Envoie la réponse à n8n et attend la réponse validée en JSON."""
    payload = {
        "agent": "Samira",
        "message": texte_samira,
        "question_client": client_prompt
    }
    try:
        # Timeout de 10s pour laisser le temps à n8n/IA de traiter
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # On retourne la valeur contenue dans 'output' ou le texte original par défaut
            return data.get("output", texte_samira)
        return texte_samira
    except Exception:
        return texte_samira

# --- STYLE CSS ---
st.markdown("""
    <style>
    .header-container { background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); padding: 25px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 25px; }
    .stChatMessage { border-radius: 15px !important; margin-bottom: 15px !important; }
    .stButton>button { background-color: #218838 !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>DS DIGITAL HUB</h1><p>L\'excellence numérique à Bobo-Dioulasso</p></div>', unsafe_allow_html=True)

# Menu Sidebar
with st.sidebar:
    st.title("Menu Agency")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

# Initialisation API & Mémoire
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erreur de configuration API.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for message in st.session_state.messages:
    role = message["role"]
    with st.chat_message(role):
        st.write(message["content"])

# Gestion input client
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    mission = """Ton nom est Samira, l'assistante intelligente de DS Digital Hub. Tu es une experte en stratégie."""

    with st.chat_message("assistant"):
        with st.spinner("Analyse de votre demande..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"MISSION: {mission}\n\nHISTORIQUE: {st.session_state.messages}\n\nCLIENT: {prompt}"
                )
                texte_genere = response.text
                
                # --- COMMUNICATION AVEC N8N ---
                texte_final = interroger_n8n(texte_genere, prompt)
                
                st.markdown(texte_final)
                st.session_state.messages.append({"role": "assistant", "content": texte_final})
            except Exception:
                st.error("Erreur technique, réessayez.")

st.markdown("---")
if st.button("✅ CONFIRMER MON PAIEMENT"):
    st.balloons()
    st.success("Notification envoyée au Responsable de Production !")
