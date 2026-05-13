import streamlit as st
from google import genai
import sys

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🚀", layout="centered")

# --- 2. SÉCURITÉ : RÉCUPÉRATION DE LA CLÉ VIA LES SECRETS ---
try:
    CLE_API = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=CLE_API)
except Exception as e:
    st.error("Erreur de configuration : La clé API est manquante dans les Secrets.")
    st.stop()

# --- 3. INITIALISATION DE L'HISTORIQUE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "etape" not in st.session_state:
    st.session_state.etape = "accueil"

# --- 4. BARRE LATÉRALE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.title("DS Digital Hub")
    st.info("Votre partenaire numérique à Bobo-Dioulasso.")
    if st.button("🔄 Nouvelle discussion"):
        st.session_state.messages = []
        st.session_state.etape = "accueil"
        st.rerun()

# --- 5. INTERFACE CHAT ---
st.title("🚀 Assistant DS Digital Hub")
st.markdown("---")

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Définition de la mission de l'IA selon l'étape
    if st.session_state.etape == "accueil":
        mission = (
            "Tu es l'assistant virtuel de Daouda pour DS Digital Hub à Bobo-Dioulasso. "
            "Accueille chaleureusement le client. Présente brièvement nos pôles : "
            "1. Audiovisuel, 2. Design Graphique, 3. Développement Web/IA, 4. Digital Marketing, 5. Live Streaming/Photo. "
            "Demande-lui quel projet il souhaite réaliser."
        )
    else:
        mission = (
            "Tu es un expert en marketing digital. Analyse la demande du client. "
            "Pose 3 questions techniques pertinentes pour préciser le besoin. "
            "Propose toujours un service complémentaire (ex: si design, propose marketing). "
            "Demande poliment le BUDGET estimé en FCFA et le DÉLAI souhaité."
        )

    # Génération de la réponse
    with st.chat_message("assistant"):
        with st.spinner("Daouda réfléchit..."):
            try:
                # On essaie le modèle flash pour la rapidité
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                texte_reponse = response.text
                st.markdown(texte_reponse)
                
                # Sauvegarder la réponse
                st.session_state.messages.append({"role": "assistant", "content": texte_reponse})
                st.session_state.etape = "discussion"
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 DS Digital Hub - Expertise en Intelligence Artificielle et Design")