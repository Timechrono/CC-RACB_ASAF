import streamlit as st
import pandas as pd
import time

# --- RECHERCHE ET DETECTION SECURISEE DES SESSIONS SANS APPEL ---
try:
    import Essais
    essais_dispo = True
except Exception:
    essais_dispo = False

try:
    import Course_1_ASAF
    course1_asaf_dispo = True
except Exception:
    course1_asaf_dispo = False

try:
    import Course_2_ASAF
    course2_asaf_dispo = True
except Exception:
    course2_asaf_dispo = False

try:
    import Course_3_ASAF
    course3_asaf_dispo = True
except Exception:
    course3_asaf_dispo = False

try:
    import Course_1_RACB
    course1_racb_dispo = True
except Exception:
    course1_racb_dispo = False

try:
    import Course_2_RACB
    course2_racb_dispo = True
except Exception:
    course2_racb_dispo = False

try:
    import Course_3_RACB
    course3_racb_dispo = True
except Exception:
    course3_racb_dispo = False

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE SANS AUCUNE MARGE BLANCHE ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
button:focus, div:focus, input:focus, select:focus {
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}

/* 1. SUPPRESSION INTÉGRALE DE LA ZONE BLANCHE TOUT EN HAUT */
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

/* BARRE DE BOUTONS HORIZONTAUX EN HTML PUR FLEXBOX (ZÉRO CONFLIT STREAMLIT) */
.menu-horizontal-cc {
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 10px !important;
    margin-top: 10px !important;
    margin-bottom: 10px !important;
    width: 100% !important;
}

.btn-cc {
    width: 140px !important;
    height: 24px !important;
    background-color: #F1F5F9 !important;
    color: #475569 !important;
    font-weight: bold !important;
    font-size: 0.82rem !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 3px !important;
    cursor: pointer !important;
    text-align: center !important;
    line-height: 22px !important;
    white-space: nowrap !important;
    font-family: sans-serif !important;
    display: inline-block !important;
    text-decoration: none !important;
}
.btn-cc.actif {
    background-color: #1E3A8A !important;
    color: white !important;
    border-color: #1E3A8A !important;
}

/* 2. RAPPROCHEMENT NET ET COLLÉ DES TABLEAUX SOUS LES BOUTONS */
div.stElementContainer {
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
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
.table-live td:last-child, .table-live td:last-child, .table-class-robuste td:last-child { font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }

/* LARGEURS DES TABLEAUX GAUCHE ET DROITE */
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
</style>
""", unsafe_allow_html=True)
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Assemblage strict des boutons horizontaux
options_menu = ["Essais"]
if course1_asaf_dispo: options_menu.append("Course 1 ASAF")
if course1_racb_dispo: options_menu.append("Course 1 RACB")
if course2_asaf_dispo: options_menu.append("Course 2 ASAF")
if course2_racb_dispo: options_menu.append("Course 2 RACB")
if course3_asaf_dispo: options_menu.append("Course 3 ASAF")
if course3_racb_dispo: options_menu.append("Course 3 RACB")

# Rendu de la barre de boutons HTML (Fixée, ne recharge pas inutilement toute la structure)
html_menu = "<div class='menu-horizontal-cc'>"
for nom_session in options_menu:
    classe_actif = "actif" if st.session_state["active_session"] == nom_session else ""
    html_menu += f'<a href="?session={nom_session.replace(" ", "%20")}" target="_self" class="btn-cc {classe_actif}">{nom_session}</a>'
html_menu += "</div>"

st.markdown(html_menu, unsafe_allow_html=True)

# Interception instantanée du clic URL
query_params = st.query_params
if "session" in query_params:
    session_cliquee = query_params["session"]
    if session_cliquee in options_menu and st.session_state["active_session"] != session_cliquee:
        st.session_state["active_session"] = session_cliquee
        st.rerun()

choix_course = st.session_state["active_session"]

# --- FRAGMENT DE RENDU ISOLÉ : RECHARGE LES TABLEAUX TOUTES LES 30S SANS METTRE DE LIGNES GRISEES ---
@st.fragment(run_every=30)
def afficher_grille_tableaux(session_active):
    d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    t_live, t_his, t_haut, t_milieu, t_bas = "Live", "Historique", "Classement Haut", "", ""

    # Appel direct et masqué du fichier associé
    try:
        if session_active == "Course 1 ASAF" and course1_asaf_dispo:
            import Course_1_ASAF
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_ASAF.recuperer_donnees_course()
        elif session_active == "Course 1 RACB" and course1_racb_dispo:
            import Course_1_RACB
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_RACB.recuperer_donnees_course()
        elif session_active == "Course 2 ASAF" and course2_asaf_dispo:
            import Course_2_ASAF
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_ASAF.recuperer_donnees_course()
        elif session_active == "Course 2 RACB" and course2_racb_dispo:
            import Course_2_RACB
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_RACB.recuperer_donnees_course()
        elif session_active == "Course 3 ASAF" and course3_asaf_dispo:
            import Course_3_ASAF
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_ASAF.recuperer_donnees_course()
        elif session_active == "Course 3 RACB" and course3_racb_dispo:
            import Course_3_RACB
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_RACB.recuperer_donnees_course()
        elif essais_dispo:
            import Essais
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Essais.recuperer_donnees_course()
    except Exception as e:
        t_live = f"⚠️ Données en cours de rafraîchissement... ({str(e)})"

    st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

    # Rendu final sans clignotement ni effet grisé
    cg, cd = st.columns([1.3, 0.9])
    with cg:
        st.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
        st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
        if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
        
    with cd:
        if session_active != "Essais":
            if t_haut:
                st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            if t_milieu:
                st.markdown(f"<span class='titre-classement'>{t_milieu}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            if t_bas:
                st.markdown(f"<span class='titre-classement'>{t_bas}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
        else:
            if t_haut:
                st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            if t_milieu:
                st.markdown(f"<span class='titre-classement'>{t_milieu}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            if t_bas:
                st.markdown(f"<span class='titre-classement'>{t_bas}</span>", unsafe_allow_html=True)
                st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)

    st.markdown("<br><br><br><div style='height:30px;'></div>", unsafe_allow_html=True)

# Lancement propre de l'affichage fragmenté
afficher_grille_tableaux(choix_course)
