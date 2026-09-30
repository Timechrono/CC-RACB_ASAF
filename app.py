import streamlit as st
import time
import Essais

st.set_page_config(
    page_title="Live Chrono - RACB & ASAF",
    page_icon="🏎️",
    layout="wide"
)

# --- DESIGN VISUEL CSS UNIQUE & SUPPRESSION DU FLASH ---
st.markdown("""
    <style>
    /* Supprime le bandeau blanc Streamlit tout en haut */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SUPPRESSION DE LA PERTE D'INTENSITÉ AU RAFRAÎCHISSEMENT */
    [data-testid="stForm"], [data-testid="stVerticalBlock"] > div {
        opacity: 1 !important;
        transition: none !important;
    }
    div[data-testid="stFragment"] {
        opacity: 1 !important;
        animation: none !important;
    }
    
    /* CONFIGURATION ALIGNEMENT HORIZONTAL DU MENU SUPER-COMPACT */
    .bloc-menu-horizontal {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin: 0 auto 10px auto;
        max-width: 800px;
    }
    .texte-menu {
        font-size: 0.95rem !important;
        font-weight: bold !important;
        color: #334155 !important;
        white-space: nowrap;
    }
    /* Largeur forcée du sélecteur pour qu'il reste compact */
    div[data-testid="stSelectbox"] {
        width: 300px !important;
        margin-bottom: 0px !important;
    }
    /* Masque le titre natif de Streamlit pour ne garder que notre texte à gauche */
    div[data-testid="stSelectbox"] label {
        display: none !important;
    }
    
    /* Styles des tableaux et titres */
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

    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)


# --- CRÉATION DE LA LIGNE HORIZONTALE UNIQUE POUR LE MENU ---
conteneur_menu = st.container()
with conteneur_menu:
    st.markdown('<div class="bloc-menu-horizontal">', unsafe_allow_html=True)
    
    col_texte, col_select = st.columns([1.1, 1.0])
    with col_texte:
        st.markdown('<p class="texte-menu" style="margin-top: 8px; text-align: right;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
    
    with col_select:
        choix_course = st.selectbox(
            "Session",
            [
                "Essais / Entraînements", 
                "Course 1 ASAF", "Course 1 RACB", 
                "Course 2 ASAF", "Course 2 RACB", 
                "Course 3 ASAF", "Course 3 RACB"
            ]
        )
    st.markdown('</div>', unsafe_allow_html=True)


# --- ZONE D'AFFICHAGE DYNAMIQUE AUTOMATIQUE (FIXÉE À 30 SECONDES) ---
@st.fragment(run_every=30)
def afficher_tableaux():
    st.cache_data.clear()
    
    if choix_course == "Essais / Entraînements":
        df_live, df_hist, df_racb, df_asaf123, df_asaf4 = Essais.recuperer_donnees_course()
    else:
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

# Lancement de la vue
afficher_tableaux()
