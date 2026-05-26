import streamlit as st
from google import genai
import os
import requests

# 1. Correction : Ajout des guillemets autour de l'URL (SyntaxError fixée)
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

# ... (reste de ton code inchangé) ...

    with st.chat_message("assistant"):
        with st.spinner("Analyse de votre demande..."):
            try:
                # Ton code de génération Gemini
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"MISSION: {mission}\n\nHISTORIQUE: {st.session_state.messages}\n\nCLIENT: {prompt}"
                )
                texte_genere = response.text
                texte_final = interroger_n8n(texte_genere, prompt)
                
                st.markdown(texte_final)
                st.session_state.messages.append({"role": "assistant", "content": texte_final})
            
            # 2. Correction : L'alignement du 'except' (IndentationError fixée)
            except Exception as e:
                st.error(f"Erreur Python : {str(e)}")
