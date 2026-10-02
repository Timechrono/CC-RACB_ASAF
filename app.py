import streamlit as st
import pandas as pd
import time
import Essais

# --- RECHERCHE ET CHARGEMENT DES SESSIONS ASAF ---
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

# --- RECHERCHE ET CHARGEMENT DES SESSIONS RACB ---
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

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE RIGIDE ET STRUCTURE DE NAVIGATION FUSIONNÉE ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
button:focus, div:focus, input:focus, select:focus {
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
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

/* BARRE DE NAVIGATION SUR MESURE : REGROUPE EN FLEXBOX TOUS LES ENFANTS DIRECTS */
div[data-testid="stHorizontalBlock"] {
    display: none !important; /* On détruit l'ancien système de colonnes défectueux */
}

.barre-nav-cc-unifiee {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 6px !important; /* Écartement mathématique constant de 6px entre TOUS les éléments */
    width: 100% !important;
    height: 26px !important;
    margin-bottom: 0px !important;
    padding: 0px !important;
}

/* APPLICATION DU STYLE SUR LA SUITE DE BOUTONS NATIFS INJECTÉS */
.barre-nav-cc-unifiee div.element-bouton {
    display: inline-block !important;
    width: auto !important;
}

.barre-nav-cc-unifiee button {
    width: auto !important;
    height: 24px !important;
    background-color: #F1F5F9 !important;
    color: #475569 !important;
    font-weight: bold !important;
    font-size: 0.82rem !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 3px !important;
    padding: 0px 14px !important;
    line-height: 22px !important;
    white-space: nowrap !important;
}

/* BOUTON SÉLECTIONNÉ ACTIF (BLEU MARQUÉ) */
.barre-nav-cc-unifiee .bouton-actif button {
    background-color: #1E3A8A !important;
    color: white !important;
    border-color: #1E3A8A !important;
}

/* TEXTE DU DÉCOMPTE PUR SANS CADRE POSITIONNÉ À DROITE */
.barre-nav-cc-unifiee .label-decompte-epure {
    font-size: 0.85rem !important;
    font-weight: bold !important;
    color: #1E3A8A !important;
    line-height: 26px !important;
    white-space: nowrap !important;
    margin-left: auto !important; /* Repousse automatiquement à l'extrémité droite de la même ligne */
    padding-right: 4px !important;
}
</style>
""", unsafe_allow_html=True)
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais / Entraînements"

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df.empty: return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

colonnes_menu = ["Essais / Entraînements"]
if course1_disponible: colonnes_menu.append("Course 1 ASAF")
if course1_racb_disponible: colonnes_menu.append("Course 1 RACB")
if course2_disponible: colonnes_menu.append("Course 2 ASAF")
if course2_racb_disponible: colonnes_menu.append("Course 2 RACB")
if course3_disponible: colonnes_menu.append("Course 3 ASAF")
if course3_racb_disponible: colonnes_menu.append("Course 3 RACB")

# --- CONCEPTION DE LA LIGNE HORIZONTALE PAR INJECTION CONTENEUR ---
# On crée la structure HTML flexbox en haut de la page
st.markdown('<div class="barre-nav-cc-unifiee">', unsafe_allow_html=True)

# Pour chaque session du menu, on injecte le bouton dans une div alignée
for idx, nom_session in enumerate(colonnes_menu):
    classe_active = "bouton-actif" if st.session_state["active_session"] == nom_session else ""
    st.markdown(f'<div class="element-bouton {classe_active}">', unsafe_allow_html=True)
    if st.button(nom_session, key=f"nav_btn_unifie_{idx}"):
        st.session_state["active_session"] = nom_session
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Ancre texte pour le décompte (placé dans le même alignement Flexbox)
zone_decompte_epure = st.empty()

# Fermeture de la ligne Flexbox
st.markdown('</div>', unsafe_allow_html=True)

# Interligne constant sous la barre de navigation
st.markdown("<div style='height: 14px; margin-bottom: 4px;'></div>", unsafe_allow_html=True)
choix_course = st.session_state["active_session"]

zone_affichage_pure = st.empty()

# --- CYCLAGE AUTOMATIQUE CENTRALISÉ TOUTES LES 30 SECONDES ---
@st.fragment
def afficher_tableaux():
    st.cache_data.clear()
    
    if choix_course == "Course 1 ASAF" and course1_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_ASAF.recuperer_donnees_course()
    elif choix_course == "Course 1 RACB" and course1_racb_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_RACB.recuperer_donnees_course()
    elif choix_course == "Course 2 ASAF" and course2_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_ASAF.recuperer_donnees_course()
    elif choix_course == "Course 2 RACB" and course2_racb_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_RACB.recuperer_donnees_course()
    elif choix_course == "Course 3 ASAF" and course3_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_ASAF.recuperer_donnees_course()
    elif choix_course == "Course 3 RACB" and course3_racb_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_RACB.recuperer_donnees_course()
    else:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Essais.recuperer_donnees_course()

    with zone_affichage_pure.container():
        st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

        cg, cd = st.columns([1.3, 0.9])
        with cg:
            if t_live: st.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
            st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
            if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
            
        with cd:
            if t_haut:
                st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
            
            if t_milieu and not (isinstance(d_milieu, pd.DataFrame) and d_milieu.empty):
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='titre-classement'>{t_milieu}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)
                
            if t_bas and not (isinstance(d_bas, pd.DataFrame) and d_bas.empty):
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='titre-classement'>{t_bas}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)

    # DÉCOMPTE SÉCURISÉ INJECTÉ DANS L'ALIGNEMENT DE LA LIGNE UNIQUE
    for secondes_restantes in range(30, 0, -1):
        zone_decompte_epure.markdown(f"<span class='label-decompte-epure'>⏱️ Rafraîchissement dans : {secondes_restantes}s</span>", unsafe_allow_html=True)
        time.sleep(1)
        
    st.rerun()

afficher_tableaux()
