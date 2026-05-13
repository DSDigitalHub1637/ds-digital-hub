import streamlit as st
from google import genai
import os

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")

# --- STYLE CSS AVANCÉ ---
st.markdown("""
    <style>
    /* Fond de page et police */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header avec dégradé */
    .header-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Style des bulles de chat */
    .stChatMessage {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }

    /* Personnalisation de la barre latérale */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Bouton de discussion */
    .stButton>button {
        border-radius: 10px;
        width: 100%;
        background-color: #1e3a8a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Affichage du Header
st.markdown("""
    <div class="header-container">
        <h1>DS DIGITAL HUB</h1>
        <p>L'excellence numérique à Bobo-Dioulasso</p>
    </div>
    """, unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.title("Menu Agency")
    st.info("Expertise : Audiovisuel, Design, Web & Ventes.")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

# Récupération de la clé API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erreur de configuration.")
    st.stop()

# Initialisation/Affichage historique
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    mission = """
    Tu es Samira l'assistant de DS Digital Hub à Bobo-Dioulasso. 
    Services : Audiovisuel, Design Graphique, Web/IA, Marketing,.
    Ton ton est pro, chaleureux et expert. Propose des solutions concrètes et demande le budget en FCFA.
    """

    with st.chat_message("assistant"):
        with st.spinner("Analyse de votre demande..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Une petite erreur technique, réessayez dans un instant.")

# Pied de page
st.markdown("---")
st.caption("© 2026 DS Digital Hub | Design & Intelligence Artificielle")
