import streamlit as st
import pandas as pd
import time

# --- SÉCURISATION INTÉGRALE DES IMPORTS DE COURSE ---
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

# --- STYLE CSS DE LA PASSERELLE ---
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

# --- SÉLECTEUR CENTRAL UNIQUE ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- AIGUILLAGE ET CORRECTION DE LA NAMEERROR ---
# La variable est maintenant créée au-dessus, l'exécution peut se faire sans bug
if choix_course == "Course 1 ASAF":
    try: Course_1_ASAF.executer_affichage_c1_asaf()
    except Exception: pass
elif choix_course == "Course 1 RACB":
    try: Course_1_RACB.executer_affichage_c1_racb()
    except Exception: pass
elif choix_course == "Course 2 ASAF":
    try: Course_2_ASAF.executer_affichage_c2_asaf()
    except Exception: pass
else:
    # Lancement de vos Essais autonomes avec vos titres et largeurs d'origine
    Essais.executer_affichage_essais()
