import streamlit as st
from google import genai
import os
import requests  # Bibliothèque réseau pour communiquer avec n8n

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo_ds.png")

# Configuration du tunnel n8n (Ton adresse active)
N8N_WEBHOOK_URL = "https://daylong-relock-cleat.ngrok-free.dev/webhook-test/samira-whatsapp"

def notifier_n8n(texte_samira, client_prompt):
    """Envoie discrètement la réponse de Samira vers ton serveur n8n local."""
    payload = {
        "agent": "Samira",
        "message": texte_samira,
        "question_client": client_prompt
    }
    # Cet en-tête permet de sauter la page d'avertissement ngrok automatiquement
    headers = {
        "ngrok-skip-browser-warning": "true"
    }
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload, headers=headers, timeout=4)
    except Exception:
        pass

# --- INTERFACE EN MODE SOMBRE INTERACTIF ---
st.markdown("""
    <style>
    /* Fond global de l'application */
    .stApp { 
        background-color: #121214 !important; 
        color: #E2E8F0 !important;
        font-family: 'Segoe UI', sans-serif; 
    }
    
    /* Barre latérale (Sidebar) en mode sombre */
    [data-testid="stSidebar"] {
        background-color: #1A1A1E !important;
        border-right: 1px solid #2D2D34;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #E2E8F0 !important;
    }

    /* En-tête (Header Container) */
    .header-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
        padding: 25px; 
        border-radius: 15px; 
        color: white !important; 
        text-align: center;
        margin-bottom: 25px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .header-container h1 { color: white !important; margin: 0; }
    .header-container p { color: #bfdbfe !important; margin-top: 5px; }

    /* Bulles de messages de Chat */
    .stChatMessage {
        background-color: #1A1A1E !important; 
        border: 1px solid #2D2D34 !important;
        border-radius: 15px !important;
        padding: 15px !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        margin-bottom: 15px !important;
    }
    .stChatMessage p { color: #E2E8F0 !important; }

    /* Zone de saisie (Chat Input) tout en bas */
    .stChatInput textarea {
        background-color: #222226 !important;
        color: #ffffff !important;
        border: 1px solid #3A3A40 !important;
        border-radius: 10px !important;
    }

    /* Personnalisation des boutons */
    .stButton>button {
        border-radius: 10px; 
        width: 100%;
        background-color: #218838 !important; 
        color: white !important; 
        font-weight: bold;
        border: none !important;
        padding: 10px !important;
        transition: background 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e7e34 !important;
    }

    /* Ligne de séparation */
    hr { border-color: #2D2D34 !important; }
    </style>
    """, unsafe_allow_html=True)

# Header de la page
st.markdown("""
    <div class="header-container">
        <h1>DS DIGITAL HUB</h1>
        <p>L'excellence numérique à Bobo-Dioulasso</p>
    </div>
    """, unsafe_allow_html=True)

# Barre latérale (Menu)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.title("Menu Agency")
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

# Récupération de la clé API Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erreur de configuration API.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE DE L'HISTORIQUE DE CONVERSATION ---
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=logo_path):
            st.write(message["content"])

# --- CAPTURE DU NOUVEAU MESSAGE CLIENT ---
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    # Ajout à l'historique en mémoire
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mission d'identité et consignes pour Samira
    mission = """
    Ton nom est Samira, l'assistante intelligente de DS Digital Hub à Bobo-Dioulasso. 
    Tu es une experte en stratégie.

    RÈGLE D'OR : 
    - Lors du TOUT PREMIER message, tu dois obligatoirement présenter l'agence et ses services.
    - Pose UNE SEULE QUESTION à la fois.
    - Ne pas afficher l'étape au début : "--- Étape X ---".

    [ÉTAPE 1] : ACCUEIL ET DÉCOUVERTE
    1. Si l'historique est vide ou ne contient que la salutation initiale, réponds ceci : 
       "Bienvenue chez DS Digital Hub ! Je suis Samira. Nous excellons dans :
       ✅ L'Audiovisuel (Spots & Montage)
       ✅ Le Design Graphique (Logos & Visuels)
       ✅ Le Web & l'IA (Sites & Agents intelligents)
       ✅ Le Marketing Digital.
       
       Pour mieux vous orienter, dans quel secteur d'activité évoluez-vous ?"
    
    2. Une fois le secteur connu, demande : "C'est noté ! Quel service ou produit souhaitez-vous réaliser avec nous aujourd'hui ?"

    [ÉTAPE 2] : ANALYSE & CONSEIL
    Analyse son besoin et propose un service complémentaire (ex: 'Puisque vous voulez un logo, un petit spot de présentation pour vos réseaux sociaux serait un grand atout').

    [ÉTAPE 3] : BUDGET & RÉPARTITION
    Demande le budget en FCFA. Propose une répartition intelligente ou un tarif pro réaliste si le budget est trop bas.

    [ÉTAPE 4] : PAIEMENT
    Donne les infos : Acompte 50%, Orange Money/Wave au +226 67 37 77 08 (Oudou SANOU).
    """

    # Génération de la réponse avec prise en compte complète de la mémoire
    with st.chat_message("assistant", avatar=logo_path):
        with st.spinner("Analyse de votre demande..."):
            try:
                # Envoi de la mission, de la mémoire complète et du nouveau message
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                texte = response.text
                st.markdown(texte)
                
                # Sauvegarde de la réponse de l'assistant dans l'historique de session
                st.session_state.messages.append({"role": "assistant", "content": texte})
                
                # Notification discrète vers n8n
                notifier_n8n(texte, prompt)
                
            except Exception:
                st.error("Erreur technique, réessayez.")

# --- ACTION DE NOTIFICATION DE PAIEMENT ---
st.markdown("---")
if st.button("✅ CONFIRMER MON PAIEMENT (ACOMPTE)"):
    st.balloons()
    st.success("Notification envoyée au Responsable de Production ! Le travail va commencer dès vérification du transfert au +226 67 37 77 08.")
    print(f"ALERTE PRODUCTION : Un client a confirmé un paiement pour le compte 67377708.")

st.caption("© 2026 DS Digital Hub | Bobo-Dioulasso")
