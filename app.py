import streamlit as st
import pandas as pd
import time

# --- NAVETTES SÉCURISÉES SANS CHARGEMENT SAUVAGE ---
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
# --- DESIGN COMPACT ET FIXE DU SÉLECTEUR ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    button:focus, div:focus, input:focus, select:focus {
        outline: none !important; border-color: transparent !important; box-shadow: none !important;
    }
    .texte-menu {
        font-size: 0.95rem !important; font-weight: bold !important;
        color: #1E293B !important; text-align: right; padding-right: 15px;
    }
    .block-container { padding-top: 0.4rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- MENUS DE SÉLECTION EN HAUT ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- BOÎTE D'AIGUILLAGE ÉTANCHE ---
# On utilise un conteneur principal Streamlit pour forcer l'affichage propre
with st.container():
    if choix_course == "Course 1 ASAF":
        try: Course_1_ASAF.afficher_ecran_complet()
        except Exception: st.error("Fichier Course 1 ASAF en cours de configuration")
    elif choix_course == "Course 1 RACB":
        pass
    elif choix_course == "Course 2 ASAF":
        pass
    else:
        # Appel de vos Essais autonomes d'origine
        Essais.afficher_ecran_complet()
