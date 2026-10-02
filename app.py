import streamlit as st
import pandas as pd
import time
import Essais

# --- DÉTECTION SIMPLE ET DIRECTE DES MODULES ---
try:
    import Course_1_ASAF
    course1_disponible = True
except ModuleNotFoundError:
    course1_disponible = False

try:
    import Course_2_ASAF
    course2_disponible = True
except ModuleNotFoundError:
    course2_disponible = False

try:
    import Course_3_ASAF
    course3_disponible = True
except ModuleNotFoundError:
    course3_disponible = False

try:
    import Course_1_RACB
    course1_racb_disponible = True
except ModuleNotFoundError:
    course1_racb_disponible = False

try:
    import Course_2_RACB
    course2_racb_disponible = True
except ModuleNotFoundError:
    course2_racb_disponible = False

try:
    import Course_3_RACB
    course3_racb_disponible = True
except ModuleNotFoundError:
    course3_racb_disponible = False

# Configuration de base
st.set_page_config(page_title="Live Chrono", layout="wide")

# Génération de la liste des sessions disponibles
options_sessions = ["Essais"]
if course1_disponible: options_sessions.append("Course 1 ASAF")
if course1_racb_disponible: options_sessions.append("Course 1 RACB")
if course2_disponible: options_sessions.append("Course 2 ASAF")
if course2_racb_disponible: options_sessions.append("Course 2 RACB")
if course3_disponible: options_sessions.append("Course 3 ASAF")
if course3_racb_disponible: options_sessions.append("Course 3 RACB")

# --- SÉLECTION SIMPLE DANS LA BARRE LATÉRALE ---
choix_course = st.sidebar.selectbox("Sélectionnez la session :", options_sessions)

st.title(f"⏱️ Suivi en Direct : {choix_course}")
st.write("---")

# Fonction d'affichage sécurisée des tableaux
def afficher_tableau_html(df):
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        st.write("*Aucune donnée disponible pour le moment*")
    else:
        st.dataframe(df, use_container_width=True)

# --- APPEL DIRECT DES FICHIERS DE CALCULS ---
terme_recherche = "Essais / Entraînements" if choix_course == "Essais" else choix_course

if terme_recherche == "Course 1 ASAF" and course1_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_ASAF.recuperer_donnees_course()
elif terme_recherche == "Course 1 RACB" and course1_racb_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_RACB.recuperer_donnees_course()
elif terme_recherche == "Course 2 ASAF" and course2_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_ASAF.recuperer_donnees_course()
elif terme_recherche == "Course 2 RACB" and course2_racb_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_RACB.recuperer_donnees_course()
elif terme_recherche == "Course 3 ASAF" and course3_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_ASAF.recuperer_donnees_course()
elif terme_recherche == "Course 3 RACB" and course3_racb_disponible:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_RACB.recuperer_donnees_course()
else:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Essais.recuperer_donnees_course()

# --- BLOC DE RENDU EN DEUX COLONNES STANDARDS ---
col_gauche, col_droite = st.columns([1.3, 0.9])

with col_gauche:
    st.subheader(t_live)
    afficher_tableau_html(d_liv)
    
    st.write(" ")
    st.subheader(t_his)
    afficher_tableau_html(d_his)

with col_droite:
    if t_haut:
        st.subheader(t_haut)
        afficher_tableau_html(d_haut)
    if t_milieu:
        st.write(" ")
        st.subheader(t_milieu)
        afficher_tableau_html(d_milieu)
    if t_bas:
        st.write(" ")
        st.subheader(t_bas)
        afficher_tableau_html(d_bas)

# Bouton manuel pour forcer la mise à jour sans attendre
if st.sidebar.button("🔄 Rafraîchir instantanément"):
    st.rerun()
