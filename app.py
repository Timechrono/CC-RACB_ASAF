import streamlit as st
import pandas as pd
import time
import Essais

# CONNEXION SÉCURISÉE AVEC LES SCRIPTS DE COURSE
try:
    import Course_1_ASAF
except Exception: pass
try:
    import Course_1_RACB
except Exception: pass
try:
    import Course_2_ASAF
except Exception: pass

st.set_page_config(page_title="Live", layout="wide")

# --- FEUILLE DE STYLE CSS DE L'APPLICATION ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }

/* REJET DU ROUGE ET DES CONTOURS DE SÉLECTION */
button:focus, div:focus, input:focus, select:focus {
    outline: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
}
[data-testid="stForm"], [data-testid="stVerticalBlock"] > div {
    opacity: 1 !important; transition: none !important;
}
div[data-testid="stFragment"] {
    opacity: 1 !important; animation: none !important;
}
.texte-menu {
    font-size: 0.95rem !important; font-weight: bold !important;
    color: #1E293B !important; text-align: right; padding-right: 15px;
}

.titre-live, .titre-hist, .titre-classement {
    color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
    padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important;
    width: 100% !important; display: block !important; clear: both !important;
}
.titre-live { background-color: #1E3A8A !important; }
.titre-hist { background-color: #475569 !important; }
.titre-classement { background-color: #1E3A8A !important; }

.table-compacte {
    width: 100% !important; margin-bottom: 0px !important;
    border-collapse: collapse !important; table-layout: fixed !important;
}
.table-compacte tr { height: 18px !important; }
.table-compacte th, .table-compacte td { 
    height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; 
    font-size: 0.85rem !important; color: #000000 !important; vertical-align: middle !important; 
    overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; 
}
.table-compacte td { border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
.table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
.table-live td:last-child, .table-hist td:last-child, .table-class-robuste td:last-child { font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; overflow: visible !important; }
.badge-piste { background-color: #FEE2E2 !important; color: #DC2626 !important; padding: 1px 4px !important; border-radius: 3px !important; font-weight: bold; }
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }

.table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
.table-live th:nth-child(2), .table-live td:nth-child(2) { width: 25% !important; }
.table-live th:nth-child(3), .table-live td:nth-child(3) { width: 17% !important; }
.table-live th:nth-child(4), .table-live td:nth-child(4) { width: 12% !important; }
.table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
.table-live th:nth-child(6), .table-live td:nth-child(6) { width: 25% !important; }
.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 8% !important; }
.table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 30% !important; }
.table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 26% !important; }
.table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 11% !important; }
.table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 8% !important; }
.table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 17% !important; }

.table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
.table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
.table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
.table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
.table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
.table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

.block-container { padding-top: 0.4rem !important; padding-bottom: 0rem !important; }
div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
</style>
""", unsafe_allow_html=True)

def gen_html(df, cl):
    if df.empty:
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# --- SÉLECTEUR CENTRAL UNIQUE ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])

with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)

with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- BLOC DE REFRESCH AUTOMATIQUE (30 SECONDES) ---
@st.fragment(run_every=30)
def afficher_tableaux():
    st.cache_data.clear()
    
    if choix_course == "Course 1 ASAF":
        d_liv, d_his, d_as123, d_as4, d_div = Course_1_ASAF.recuperer_donnees_course()
        d_racb = pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents ASAF"
    elif choix_course == "Course 1 RACB":
        d_liv, d_his, d_racb, d_div = Course_1_RACB.recuperer_donnees_course()
        d_as123, d_as4 = pd.DataFrame(), pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents RACB"
    elif choix_course == "Course 2 ASAF":
        d_liv, d_his, d_as123, d_as4, d_div = Course_2_ASAF.recuperer_donnees_course()
        d_racb = pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 2ème COURSE / Concurrents ASAF"
    else:
        d_liv, d_his, d_as123, d_as4, _ = Essais.recuperer_donnees_course()
        d_div, d_racb = pd.DataFrame(), pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS"

    cg, cd = st.columns([1.3, 0.9])
    with cg:
        st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
        st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<span class='titre-hist'>{titre_historique}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    with cd:
        if choix_course == "Course 1 RACB":
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL OFFICIEUX RACB (Top 30)</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_racb, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-classement'>📊 CLASSEMENT OFFICIEUX PAR Groupe / Classe (Top 3)</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_div, "table-class-robuste"), unsafe_allow_html=True)
        else:
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL OFFICIEUX Division 123 (Top 25)</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_as123, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL OFFICIEUX Division 4 (Top 10)</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_as4, "table-class-robuste"), unsafe_allow_html=True)
            
            if choix_course in ["Course 1 ASAF", "Course 2 ASAF"]:
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-classement'>📊 CLASSEMENT PAR Division / Classe (Top 3)</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_div, "table-class-robuste"), unsafe_allow_html=True)

afficher_tableaux()
