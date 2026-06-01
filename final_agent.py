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
            # 1. Vérification de la clé API
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("Erreur : La clé API 'GEMINI_API_KEY' n'est pas configurée dans les secrets.")
                st.stop()

            # 2. Initialisation du client
            client = genai.Client(api_key=api_key)
            
            # 3. Appel au modèle
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Tu es Samira, une assistante experte de DS Digital Hub. Réponds à : {prompt}"
            )
            
            texte_ia = response.text
            
            # 4. Envoi à n8n
            payload = {"agent": "Samira", "message": texte_ia, "question_client": prompt}
            n8n_resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            
            # Résultat final
            st.markdown(texte_ia)
            st.session_state.messages.append({"role": "assistant", "content": texte_ia})
            
        except Exception as e:
            # Cette ligne affichera l'erreur précise (429, 403, etc.) au lieu d'un message générique
            st.error(f"Erreur technique détaillée : {str(e)}")
