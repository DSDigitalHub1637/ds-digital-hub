import streamlit as st

# Configuration de la page
st.set_page_config(page_title="DS Digital Hub", layout="centered")

# --- Initialisation de l'état ---
if 'etape' not in st.session_state:
    st.session_state.etape = 'accueil'

# --- En-tête avec Logo et Titre ---
# Assurez-vous que 'logo_ds.png' est dans le même dossier
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("logo_ds.png", width=80)
    except:
        st.write("Logo") # Texte de remplacement si l'image est manquante
with col2:
    st.title("DS Digital Hub")

st.subheader("L'excellence numérique à Bobo-Dioulasso")

# --- Logique de la conversation ---

if st.session_state.etape == 'accueil':
    st.markdown("""
    ---
    **Bienvenue chez DS Digital Hub ! Je suis Samira. Nous excellons dans :**
    * ✅ **L'Audiovisuel** (Spots & Montage)
    * ✅ **Le Design Graphique** (Logos & Visuels)
    * ✅ **Le Web & l'IA** (Sites & Agents intelligents)
    * ✅ **Le Marketing Digital & les Ventes** (Téléphones, Mode, Billetterie)
    
    Pour mieux vous orienter, dans quel secteur d'activité évoluez-vous ?
    ---
    """)
    
    if st.button("Discuter d'un projet"):
        st.session_state.etape = 'demande_budget'
        st.rerun()

elif st.session_state.etape == 'demande_budget':
    budget = st.number_input("Quel est votre budget pour ce projet ? (en FCFA)", min_value=0, step=1000)
    if st.button("Soumettre mon budget"):
        if budget < 10000:
            st.warning("⚠️ Notre tarif minimum pour garantir une prestation de qualité est de 10 000 FCFA.")
            st.session_state.etape = 'validation_budget'
        else:
            st.success("✅ Ce budget nous convient parfaitement !")
            st.session_state.etape = 'paiement'
        st.rerun()

elif st.session_state.etape == 'validation_budget':
    st.write("Acceptez-vous d'ajuster votre budget à 10 000 FCFA pour démarrer le projet ?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Oui, je valide"):
            st.session_state.etape = 'paiement'
            st.rerun()
    with col2:
        if st.button("Non, merci"):
            st.write("Nous sommes désolés de ne pouvoir donner suite. N'hésitez pas si vos besoins évoluent !")
            if st.button("Retour à l'accueil"):
                st.session_state.etape = 'accueil'
                st.rerun()

elif st.session_state.etape == 'paiement':
    st.success("🎉 Super, nous pouvons commencer !")
    st.markdown("""
    ### 💳 Informations de paiement
    Pour valider votre commande, veuillez effectuer le transfert via **Wave** ou **Orange Money** :
    
    * **Nom :** Oudou SANOU
    * **Numéro :** 67377708
    
    *Merci de nous envoyer une capture d'écran du paiement pour finaliser votre dossier.*
    """)
    if st.button("Retour à l'accueil"):
        st.session_state.etape = 'accueil'
        st.rerun()
