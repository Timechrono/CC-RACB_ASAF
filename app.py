import streamlit as st

# Configuration de la page en mode large
st.set_page_config(
    page_title="Live Chrono - RACB & ASAF",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN ET STYLE DE LA BARRE LATÉRALE ---
st.markdown("""
    <style>
    /* Supprime le bandeau blanc Streamlit tout en haut */
    [data-testid="stHeader"] { display: none !important; }
    
    /* Personnalisation de la barre latérale gauche */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important; /* Fond bleu nuit ultra sombre */
        color: #FFFFFF !important;
    }
    
    /* Style du titre de la barre latérale */
    .titre-sidebar {
        color: #F8FAFC !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #38BDF8; /* Ligne de surbrillance bleue */
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRE LATÉRALE DE SÉLECTION (SIDEBAR) ---
with st.sidebar:
    st.markdown("<div class='titre-sidebar'>🏁 Sélection du Live</div>", unsafe_allow_html=True)
    
    # Boutons radio modernes à la place du menu déroulant classique
    choix_course = st.radio(
        "Choisissez votre session :",
        [
            "⏱️ Essais / Entraînements", 
            "🚗 Course 1 ASAF", 
            "🏆 Course 1 RACB", 
            "🚗 Course 2 ASAF",
            "🏆 Course 2 RACB",
            "🚗 Course 3 ASAF",
            "🏆 Course 3 RACB"
        ],
        label_visibility="collapsed" # Masque le texte brut d'explication pour un design plus propre
    )

# --- CHARGEMENT AUTOMATIQUE DE VOS SCRIPT MOTEURS ---
if choix_course == "⏱️ Essais / Entraînements":
    import Essais
elif choix_course == "🚗 Course 1 ASAF":
    import Course_1_ASAF
elif choix_course == "🏆 Course 1 RACB":
    import Course_1_RACB
elif choix_course == "🚗 Course 2 ASAF":
    import Course_2_ASAF
elif choix_course == "🏆 Course 2 RACB":
    import Course_2_RACB
elif choix_course == "🚗 Course 3 ASAF":
    import Course_3_ASAF
elif choix_course == "🏆 Course 3 RACB":
    import Course_3_RACB
