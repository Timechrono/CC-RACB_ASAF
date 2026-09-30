import streamlit as st
import pandas as pd
import time

# --- CHARGEMENT DES SESSIONS DE COURSE ---
try: import Essais
except Exception: pass
try: import Course_1_ASAF
except Exception: pass
try: import Course_1_RACB
except Exception: pass
try: import Course_2_ASAF
except Exception: pass

st.set_page_config(layout="wide")

# --- STYLE CSS DU SÉLECTEUR UNIQUEMENT ---
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

# --- BARRE DE NAVIGATION CONTÔLÉE ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- L'AIGUILLAGE PUR : CHAQUE FICHIER REPREND SA LIBERTÉ ---
if choix_course == "Course 1 ASAF":
    Course_1_ASAF.afficher_ecran_complet()
elif choix_course == "Course 1 RACB":
    Course_1_RACB.afficher_ecran_complet()
elif choix_course == "Course 2 ASAF":
    Course_2_ASAF.afficher_ecran_complet()
else:
    # Par défaut, les Essais gèrent l'intégralité de leur affichage
    Essais.afficher_ecran_complet()
