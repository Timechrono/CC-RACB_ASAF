import streamlit as st
import pandas as pd
import time
import Essais

# --- CONFIGURATION INITIALE (Le primaryColor règle définitivement la couleur du cadre au clic sans CSS cassant) ---
st.set_page_config(
    page_title="Live", 
    layout="wide",
    theme={
        "primaryColor": "#1E3A8A", # Le cadre rouge au clic devient automatiquement Bleu Foncé
        "backgroundColor": "#FFFFFF"
    }
)

# --- DESIGN SCIENTIFIQUE RIGIDE ET FIXE RESTAURÉ ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
button:focus, div:focus, input:focus, select:focus {
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}

/* Restauration stricte du texte menu */
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

/* Alignement parfait en hauteur du chrono de décompte */
.texte-chrono {
    font-size: 0.95rem !important;
    font-weight: bold !important;
    color: #475569 !important;
    margin-top: -16px !important; /* Calé sur la même hauteur que le texte de gauche */
    white-space: nowrap !important;
}

/* Cible uniquement le texte dans le bouton sélecteur pour le mettre en gras et plus grand */
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    font-size: 1.15rem !important;
    font-weight: bold !important;
}

.titre-live, .titre-hist, .titre-classement {
    color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
    padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important;
    width: 100% !important; display: block !important; clear: both !important;
}
.titre-live { background-color: #15803D !important; }
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
.table-live td:last-child, .table-hist td:last-child, .table-class-robuste td:last-child { font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }

.table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
.table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
.table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
.table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
.table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
.table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }

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

# --- CONFIGURATION SÉLECTEUR ---
col_texte, col_select, col_chrono, col_reste = st.columns([1.3, 1.4, 1.5, 3.3], vertical_alignment="center")
with col_texte:
    st.markdown('<p class="texte-menu">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements"], label_visibility="collapsed")
with col_chrono:
    emplacement_chrono = st.empty()

st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

# --- REFRESH ET APPEL DIRECT ---
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

    # Décompte fluide
    for secondes_restantes in range(30, 0, -1):
        emplacement_chrono.markdown(f'<p class="texte-chrono">🔄 Rafraîchissement dans {secondes_restantes}s</p>', unsafe_allow_html=True)
        time.sleep(1)
    
    st.rerun()

afficher_tableaux_avec_decompte()
