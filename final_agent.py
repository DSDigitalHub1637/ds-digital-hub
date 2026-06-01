import streamlit as st
import requests
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="DS Digital Hub | Expert IA", page_icon="🤖", layout="centered")

# URL de ton webhook n8n
N8N_WEBHOOK_URL = https://primary-production-b36e9.up.railway.app/webhook-test/samira-whatsapp

# --- STYLE CSS AVANCÉ ---
st.markdown("""
    <style>
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
        border-radius: 15px !important;
        padding: 15px !important; 
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

# --- HEADER & SIDEBAR ---
st.markdown("""<div class="header-container"><h1>DS DIGITAL HUB</h1><p>L'excellence numérique à Bobo-Dioulasso</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.title("Menu Agency")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

# --- INITIALISATION MÉMOIRE LOCALE (Affichage) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE DE LA CONVERSATION ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- GESTION DU MESSAGE CLIENT (Logique n8n) ---
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    # 1. Ajout et affichage immédiat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Appel au "Cerveau" n8n
    with st.spinner("Samira réfléchit..."):
        try:
            # On envoie le message au webhook n8n qui gère la mémoire Postgres
            response = requests.post(N8N_WEBHOOK_URL, json={"message": prompt}, timeout=20)
            data = response.json()
            
            # Récupération de la réponse renvoyée par le nœud "Respond to Webhook"
            texte_reponse = data.get("reponse", "Désolé, une erreur de communication est survenue.")
            
            # 3. Ajout et affichage de la réponse
            st.session_state.messages.append({"role": "assistant", "content": texte_reponse})
            st.rerun()
        except Exception as e:
            st.error(f"Erreur de connexion avec le Hub : {e}")

# --- PIED DE PAGE & PAIEMENT ---
st.markdown("---")
if st.button("✅ CONFIRMER MON PAIEMENT (ACOMPTE)"):
    st.balloons()
    st.success("Notification envoyée au Responsable de Production !")

st.caption("© 2026 DS Digital Hub | Bobo-Dioulasso")
