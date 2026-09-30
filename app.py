import streamlit as st
import pandas as pd
import time
import Essais

st.set_page_config(page_title="Live", layout="wide")

# --- DESIGN SCIENTIFIQUE RIGIDE ET FIXE ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }

/* --- SUPPRESSION TOTALE DU CADRE ROUGE STREAMLIT ET REMPLACEMENT PAR BLEU FONCÉ --- */
button:focus, div:focus, input:focus, select:focus, [data-baseweb="select"]:focus-within {
    outline: none !important; 
    border-color: #1E3A8A !important; 
    box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.2) !important;
}
/* Annulation de la couleur rouge native de Streamlit au clic */
div[data-baseweb="select"] > div {
    border-color: #CCCCCC !important;
}
div[data-baseweb="select"] > div:focus-within, 
div[data-baseweb="select"] > div:hover {
    border-color: #1E3A8A !important;
}
/* Ciblage de la liste déroulante quand elle s'ouvre */
ul[role="listbox"] {
    border: 1px solid #1E3A8A !important;
}

/* Alignement du texte à gauche avec une marge supérieure propre */
.texte-menu {
    font-size: 1.05rem !important; 
    font-weight: bold !important;
    color: #1E293B !important; 
    text-align: left !important; 
    margin-top: -16px !important; 
    margin-bottom: 0px !important;
    white-space: nowrap !important;
    padding-right: 5px !important;
}

/* Modifié : Le chronomètre remonte un peu plus haut (margin-top passe à -20px) */
.texte-chrono {
    font-size: 0.95rem !important;
    font-weight: bold !important;
    color: #475569 !important;
    margin-top: -20px !important;
    white-space: nowrap !important;
}

/* --- FORCE LA TAILLE ET LE GRAS À L'INTÉRIEUR DU BOUTON SÉLECTEUR --- */
div[data-testid="stSelectbox"] p, 
div[data-testid="stSelectbox"] div,
div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
div[data-baseweb="select"] span {
    font-size: 1.15rem !important;
    font-weight: 800 !important; /* Gras très prononcé */
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

def gen_html(df, cl):
    if df.empty:
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# --- CONFIGURATION SÉLECTEUR ET CHRONO ---
col_texte, col_select, col_chrono, col_reste = st.columns([1.3, 1.6, 1.5, 1.8], vertical_alignment="center")

with col_texte:
    st.markdown('<p class="texte-menu">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)

with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements"], label_visibility="collapsed")

with col_chrono:
    emplacement_chrono = st.empty()

st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

# --- ZONE PRINCIPALE D'AFFICHAGE ---
@st.fragment
def afficher_tableaux_avec_decompte():
    st.cache_data.clear()
    
    d_liv, d_his, d_as123, d_as4, d_racb, t_racb, t_as123, t_as4 = Essais.recuperer_donnees_course()
    titre_historique = "🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB"
    
    st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

    cg, cd = st.columns([1.3, 0.9])
    with cg:
        st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
        st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<span class='titre-hist'>{titre_historique}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    with cd:
        st.markdown(f"<span class='titre-classement'>{t_racb}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_racb, "table-class-robuste"), unsafe_allow_html=True)
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<span class='titre-classement'>{t_as123}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_as123, "table-class-robuste"), unsafe_allow_html=True)
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<span class='titre-classement'>{t_as4}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_as4, "table-class-robuste"), unsafe_allow_html=True)

    for secondes_restantes in range(30, 0, -1):
        emplacement_chrono.markdown(f'<p class="texte-chrono">🔄 Rafraîchissement dans {secondes_restantes}s</p>', unsafe_allow_html=True)
        time.sleep(1)
    
    st.rerun()

afficher_tableaux_avec_decompte()
