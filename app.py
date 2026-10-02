import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE SANS AUCUNE MARGE BLANCHE ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
button:focus, div:focus, input:focus, select:focus {
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}

/* 1. NETTOYAGE ET REPOSITIONNEMENT EN HAUT DE L'ÉCRAN */
.block-container { 
    padding-top: 5px !important; 
    padding-bottom: 0rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
}
div[data-testid="stMainBlockContainer"] {
    padding-top: 5px !important;
    margin-top: 0px !important;
}
div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
    padding-top: 0px !important;
}

/* CONTENEUR FLEXBOX SUR MESURE POUR ENFERMER ET CENTRER LES BOUTONS SANS ÉTIREMENT */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    width: 100% !important;
    margin: 0px auto !important;
}
div[data-testid="stHorizontalBlock"] > div {
    flex: none !important;
    width: auto !important;
    padding: 0px !important;
    margin: 0px !important;
}

div.stButton > button {
    width: 130px !important;
    min-height: unset !important;
    height: 24px !important;
    background-color: #F1F5F9 !important;
    color: #475569 !important;
    font-weight: bold !important;
    font-size: 0.82rem !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 3px !important;
    padding: 0px !important;
    margin: 0px !important;
    line-height: 22px !important;
    white-space: nowrap !important;
}
</style>
""", unsafe_allow_html=True)
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"

# On force une liste fixe de boutons pour le test
colonnes_visibles = ["Essais", "Course 1 ASAF", "Course 1 RACB"]

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

cols = st.columns([1.0] * len(colonnes_visibles))
for idx, nom_session in enumerate(colonnes_visibles):
    with cols[idx]:
        if st.button(nom_session, key=f"btn_nav_{idx}"):
            st.session_state["active_session"] = nom_session
            st.rerun()

for idx, nom_session in enumerate(colonnes_visibles):
    if st.session_state["active_session"] == nom_session:
        st.markdown(f"""<style>div[data-testid="stHorizontalBlock"] > div:nth-child({idx+1}) button {{ background-color: #1E3A8A !important; color: white !important; border-color: #1E3A8A !important; }}</style>""", unsafe_allow_html=True)

st.markdown("<div style='height: 10px; clear: both;'></div>", unsafe_allow_html=True)

choix_course = st.session_state["active_session"]

# Affichage d'un texte simple à la place des tableaux pour valider le fonctionnement
st.write(f"### Menu actif détecté : {choix_course}")
st.info("Si ce message et le menu s'affichent instantanément, c'est que le problème vient à 100% du contenu du fichier Essais.py.")
