import streamlit as st
from google import genai
import os

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Titre et Logo
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
st.sidebar.title("DS Digital Hub")
st.sidebar.markdown("Votre partenaire numérique à Bobo-Dioulasso.")

if st.sidebar.button("🔄 Nouvelle discussion"):
    st.session_state.messages = []
    st.rerun()

# Récupération de la clé API depuis les Secrets de Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Erreur de configuration : Clé API introuvable.")
    st.stop()

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    # Afficher le message du client
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Définition de la mission de l'IA (Ton expertise)
    mission = """
    Tu es l'assistant IA de DS Digital Hub, une agence basée à Bobo-Dioulasso.
    Ton rôle est de conseiller les clients sur :
    1. L'Audiovisuel (Spots, montages).
    2. Le Design Graphique (Logos, affiches).
    3. Le Web & l'IA (Sites, agents IA).
    4. Le Digital Marketing & le Community Management.
    5. Le Streaming (Couverture d'événements).
    6. NOUVEAU : La vente de téléphones, vêtements et tickets d'événements.
    
    Sois professionnel, amical, et mentionne que l'agence est à Bobo-Dioulasso. 
    Propose toujours un service complémentaire et demande le budget estimé en FCFA.
    """

    # Génération de la réponse
    with st.chat_message("assistant"):
        with st.spinner("DS Digital Hub réfléchit..."):
            try:
                # UTILISATION DU MODÈLE 1.5 FLASH (Plus stable pour le quota gratuit)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                
                texte_reponse = response.text
                st.markdown(texte_reponse)
                
                # Sauvegarder la réponse
                st.session_state.messages.append({"role": "assistant", "content": texte_reponse})
                
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")

# Bas de page
st.markdown("---")
st.caption("© 2026 DS Digital Hub - Expertise en Intelligence Artificielle et Design")
