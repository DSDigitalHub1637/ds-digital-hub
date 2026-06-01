import streamlit as st
from google import genai
import os
import requests

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo_ds.png")

# Configuration du tunnel n8n
N8N_WEBHOOK_URL = "https://primary-production-b36e9.up.railway.app/webhook-test/samira-whatsapp"

def notifier_n8n(texte_samira, client_prompt):
    """Envoie discrètement la réponse de Samira vers ton serveur n8n."""
    payload = {
        "agent": "Samira",
        "message": texte_samira,
        "question_client": client_prompt
    }
    headers = {"ngrok-skip-browser-warning": "true"}
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload, headers=headers, timeout=4)
    except Exception:
        pass

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { font-family: 'Segoe UI', sans-serif; }
    .header-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
        padding: 25px; 
        border-radius: 15px; 
        color: white !important; 
        text-align: center;
        margin-bottom: 25px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .header-container h1 { color: white !important; margin: 0; }
    .header-container p { color: #bfdbfe !important; margin-top: 5px; }
    .stChatMessage {
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 15px !important;
        padding: 15px !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }
    .stButton>button {
        border-radius: 10px; 
        width: 100%;
        background-color: #218838 !important; 
        color: white !important; 
        font-weight: bold;
        border: none !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""<div class="header-container"><h1>DS DIGITAL HUB</h1><p>L'excellence numérique à Bobo-Dioulasso</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.title("Menu Agency")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erreur de configuration API.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    mission = """
    Ton nom est Samira, l'assistante intelligente de DS Digital Hub à Bobo-Dioulasso. 
    Tu es une experte en stratégie.
    RÈGLE D'OR : 
    - Lors du TOUT PREMIER message, présente l'agence : Audiovisuel, Design, Web/IA, Marketing.
    - Pose UNE SEULE QUESTION à la fois.
    - Ne pas afficher d'étapes (ex: 'Étape 1').
    - Ne demande pas le budget en premier.
    """

    with st.chat_message("assistant", avatar=logo_path):
        with st.spinner("Analyse de votre demande..."):
            try:
                # Utilisation du modèle valide
                response = client.models.generate_content(
                    model="gemini-3.5-flash", 
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                texte = response.text
                st.markdown(texte)
                st.session_state.messages.append({"role": "assistant", "content": texte})
                notifier_n8n(texte, prompt)
            except Exception as e:
                st.error(f"Erreur technique : {e}")

st.markdown("---")
if st.button("✅ CONFIRMER MON PAIEMENT (ACOMPTE)"):
    st.balloons()
    st.success("Notification envoyée au Responsable de Production !")

st.caption("© 2026 DS Digital Hub | Bobo-Dioulasso")
