import streamlit as st
from google import genai
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖")
N8N_WEBHOOK_URL = "https://primary-production-b36e9.up.railway.app/webhook/samira-whatsapp"

st.title("DS DIGITAL HUB")

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
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("Erreur : Clé API manquante dans les secrets.")
                st.stop()

            # Appel direct au modèle avec le nom correct
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.5-flash",  # Mise à jour vers le modèle recommandé
                contents=f"Tu es Samira, une assistante experte de DS Digital Hub. Réponds à : {prompt}"
            )
            
            texte_ia = response.text
            
            # Envoi à n8n
            payload = {"agent": "Samira", "message": texte_ia, "question_client": prompt}
            requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            
            # Affichage
            st.markdown(texte_ia)
            st.session_state.messages.append({"role": "assistant", "content": texte_ia})
            
        except Exception as e:
            st.error(f"Erreur technique détaillée : {str(e)}")
