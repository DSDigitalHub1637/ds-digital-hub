import streamlit as st
from google import genai
import os

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub - Expert IA", page_icon="🤖", layout="centered")

# --- STYLE CSS AVANCÉ ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; font-family: 'Segoe UI', sans-serif; }
    .header-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        background-color: white !important; border-radius: 20px !important;
        padding: 15px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }
    .stButton>button {
        border-radius: 10px; width: 100%;
        background-color: #28a745; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
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
    if st.button("🔄 Nouvelle session"):
        st.session_state.messages = []
        st.rerun()

# Clé API
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
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Comment DS Digital Hub peut vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # MISSION AVEC LOGIQUE D'ENTONNOIR ET LISTE DES SERVICES
    mission = """
    Tu es Samira l'expert consultante stratégique de DS Digital Hub à Bobo-Dioulasso. 
    Nos services incluent : Audiovisuel (spots, montage), Design Graphique (logos, identité visuelle), Web & IA (sites, agents intelligents), Marketing Digital.
    
    Tu ne dois JAMAIS donner le numéro de paiement dès le début. Suis STRICTEMENT cette séquence :

    ÉTAPE 1 : COMPRÉHENSION DU BESOIN (Phase de découverte)
    Si le client veut un service, pose-lui obligatoirement ces 3 questions pour établir un diagnostic :
    1. Dans quel secteur d'activité évoluez-vous précisément ?
    2. Quelle est la cible principale de ce projet (jeunes, entreprises, population locale, etc.) ?
    3. Quel est l'objectif prioritaire (augmenter les ventes, améliorer la notoriété ou lancer un produit) ?

    ÉTAPE 2 : CONSEIL D'EXPERT
    Analyse ses réponses et propose une recommandation stratégique basée sur nos services (ex: "Pour votre boutique de mode, un catalogue digital et une campagne publicitaire Meta seraient parfaits").

    ÉTAPE 3 : QUALIFICATION DU BUDGET
    Demande-lui ensuite : "Quel budget approximatif en FCFA avez-vous prévu pour ce projet ?"
    - Si le budget est sérieux, passe à la suite.
    - Si le budget est trop bas, explique poliment que l'excellence de DS Digital Hub garantit un meilleur retour sur investissement.

    ÉTAPE 4 : MODALITÉS DE PAIEMENT (Phase de clôture)
    UNIQUEMENT quand le projet est validé et le budget accepté, donne les instructions :
    - Acompte de 50% pour démarrer la production.
    - Paiement via Orange Money ou Wave au +226 67 37 77 08 (Nom du compte : Oudou SANOU).
    """

    with st.chat_message("assistant"):
        with st.spinner("Analyse de votre demande..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"MISSION : {mission}\n\nHISTORIQUE : {st.session_state.messages}\n\nCLIENT : {prompt}"
                )
                texte = response.text
                st.markdown(texte)
                st.session_state.messages.append({"role": "assistant", "content": texte})
            except Exception:
                st.error("Erreur technique, réessayez.")

# --- SECTION NOTIFICATION RESPONSABLE ---
st.markdown("---")
if st.button("✅ CONFIRMER MON PAIEMENT (ACOMPTE)"):
    # Ici, on simule l'envoi au responsable
    st.balloons()
    st.success("Notification envoyée au Responsable de Production ! Le travail va commencer dès vérification du transfert au +226 67 37 77 08.")
    
    # Message interne (pour les logs Streamlit en attendant l'Email/WhatsApp automatique)
    print(f"ALERTE PRODUCTION : Un client a confirmé un paiement pour le compte 67377708.")

st.caption("© 2026 DS Digital Hub | Bobo-Dioulasso")
