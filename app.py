import streamlit as st
import time
import Essais

st.set_page_config(
    page_title="Live Chrono - RACB & ASAF",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN VISUEL CSS ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    .titre-live, .titre-hist, .titre-classement {
        color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
        padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important;
        width: 100% !important; display: block !important; clear: both !important;
    }
    .titre-live { background-color: #15803D !important; margin-top: 0px !important; }
    .titre-hist { background-color: #475569 !important; margin-top: 10px !important; }
    .titre-classement { background-color: #1E3A8A !important; margin-top: 0px !important; }
    
    .table-compacte { width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: fixed !important; }
    .table-compacte tr { height: 18px !important; }
    .table-compacte th, .table-compacte td { 
        height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; 
        vertical-align: middle !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; 
    }
    .table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
    .table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
    
    .table-live td:last-child, .table-hist td:last-child, .table-class-robuste td:last-child {
        font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; overflow: visible !important;
    }
    .badge-piste { background-color: #FEE2E2 !important; color: #DC2626 !important; padding: 1px 4px !important; border-radius: 3px !important; font-weight: bold; }
    .table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }
    
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 25% !important; }
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 17% !important; }
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 12% !important; }
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 25% !important; }

    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 7% !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 7% !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 10% !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 10% !important; }  
    .table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 14% !important; }  

    .table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
    .table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
    .table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
    .table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
    .table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
    .table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

    .block-container { padding-top: 0.3rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

# --- BARRE LATÉRALE DE SÉLECTION (SIDEBAR) ---
with st.sidebar:
    st.markdown("<div class='titre-sidebar'>🏁 Sélection du Live</div>", unsafe_allow_html=True)
    choix_course = st.radio(
        "Choisissez votre session :",
        [
            "⏱️ Essais / Entraînements", 
            "🚗 Course 1 ASAF", "🏆 Course 1 RACB", 
            "🚗 Course 2 ASAF", "🏆 Course 2 RACB", 
            "🚗 Course 3 ASAF", "🏆 Course 3 RACB"
        ],
        label_visibility="collapsed"
    )

# --- ZONE D'AFFICHAGE DYNAMIQUE ---
# st.fragment permet de rafraîchir uniquement les tableaux sans figer toute l'application
@st.fragment(run_every=4)
def afficher_tableaux():
    st.cache_data.clear() # Nettoyage obligatoire pour forcer Streamlit à re-télécharger les fichiers Excel
    
    # Appel du script correspondant à la sélection
    if choix_course == "⏱️ Essais / Entraînements":
        df_live, df_hist, df_racb, df_asaf123, df_asaf4 = Essais.recuperer_donnees_course()
    else:
        # En attente des autres fichiers, on charge Essais par défaut pour éviter un plantage
        df_live, df_hist, df_racb, df_asaf123, df_asaf4 = Essais.recuperer_donnees_course()

    cg, cd = st.columns([1.3, 0.9])
    with cg:
        st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
        st.markdown(generer_tableau_html(df_live, "table-live"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='titre-hist'>🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB</span>", unsafe_allow_html=True)
        st.markdown(generer_tableau_html(df_hist, "table-hist"), unsafe_allow_html=True)
    with cd:
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 20)</span>", unsafe_allow_html=True)
        st.markdown(generer_tableau_html(df_racb, "table-class-robuste"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS ASAF DIV 1-2-3 (Top 25)</span>", unsafe_allow_html=True)
        st.markdown(generer_tableau_html(df_asaf123, "table-class-robuste"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS ASAF DIV 4 (Top 10)</span>", unsafe_allow_html=True)
        st.markdown(generer_tableau_html(df_asaf4, "table-class-robuste"), unsafe_allow_html=True)

# Lancement de la fonction d'affichage
afficher_tableaux()
