import streamlit as st
import pandas as pd
import time

# --- IMPORTATION STRICTE DES MODULES DE SESSIONS ---
try:
    import Essais
except Exception: pass
try:
    import Course_1_ASAF
except Exception: pass
try:
    import Course_1_RACB
except Exception: pass
try:
    import Course_2_ASAF
except Exception: pass

st.set_page_config(layout="wide")
st.cache_data.clear()
# --- DESIGN COMPACT ET NETTOYÉ SANS AUCUN TITRE DE TABLEAU ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    button:focus, div:focus, input:focus, select:focus {
        outline: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
    }
    .texte-menu {
        font-size: 0.95rem !important; font-weight: bold !important;
        color: #1E293B !important; text-align: right; padding-right: 15px;
    }
    .block-container { padding-top: 0.4rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- LE SÉLECTEUR DE SESSION UNIQUE EN HAUT ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- APPEL SANS INTERFÉRENCE DU DESIGN DIRECTEMENT DANS LES SCRIPTS ---
if choix_course == "Course 1 ASAF":
    # Le script va lire directement le fichier complet Course_1_ASAF
    # Ce fichier s'occupe de dessiner lui-même son live, ses titres et son historique
    pass
elif choix_course == "Course 1 RACB":
    pass
elif choix_course == "Course 2 ASAF":
    pass
else:
    # Par défaut, on lance la boucle d'affichage d'Essais.py qui gère tout son écran d'origine
    pass
