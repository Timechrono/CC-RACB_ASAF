import streamlit as st
import pandas as pd
import time

# --- CHARGEMENT UNIQUE ET PARAMÉTRÉ DES FICHIERS ---
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
# Initialisation de la mémoire tampon locale (ZÉRO utilisation du cache Streamlit défectueux)
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"
if "sauvegarde_loc_donnees" not in st.session_state:
    st.session_state["sauvegarde_loc_donnees"] = {}

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Assemblage des boutons horizontaux
options_menu = ["Essais"]
if course1_asaf_dispo: options_menu.append("Course 1 ASAF")
if course1_racb_dispo: options_menu.append("Course 1 RACB")
if course2_asaf_dispo: options_menu.append("Course 2 ASAF")
if course2_racb_dispo: options_menu.append("Course 2 RACB")
if course3_asaf_dispo: options_menu.append("Course 3 ASAF")
if course3_racb_dispo: options_menu.append("Course 3 RACB")

# Injection du menu horizontal indivisible
html_menu = "<div class='menu-horizontal-cc'>"
for nom_session in options_menu:
    classe_actif = "actif" if st.session_state["active_session"] == nom_session else ""
    html_menu += f'<a href="?session={nom_session.replace(" ", "%20")}" target="_self" class="btn-cc {classe_actif}">{nom_session}</a>'
html_menu += "</div>"

st.markdown(html_menu, unsafe_allow_html=True)

# Interception immédiate du clic par URL
query_params = st.query_params
if "session" in query_params:
    session_cliquee = query_params["session"]
    if session_cliquee in options_menu and st.session_state["active_session"] != session_cliquee:
        st.session_state["active_session"] = session_cliquee
        st.rerun()

choix_course = st.session_state["active_session"]

# Structures de données par défaut
d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
t_live, t_his, t_haut, t_milieu, t_bas = "Live", "Historique", "Classement Haut", "", ""

# Restauration immédiate depuis la mémoire tampon si elle existe déjà (évite l'écran blanc/gris)
if choix_course in st.session_state["sauvegarde_loc_donnees"]:
    d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = st.session_state["sauvegarde_loc_donnees"][choix_course]

# --- APPEL DIRECT BLINDÉ EN TEMPS : SÉCURITÉ TIMEOUT MAX 2 SECONDES ---
try:
    from concurrent.futures import ThreadPoolExecutor

    def recuperer_sans_bloquer():
        if choix_course == "Course 1 ASAF" and course1_asaf_dispo:
            import Course_1_ASAF
            return Course_1_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 1 RACB" and course1_racb_disp:
            import Course_1_RACB
            return Course_1_RACB.recuperer_donnees_course()
        elif choix_course == "Course 2 ASAF" and course2_asaf_dispo:
            import Course_2_ASAF
            return Course_2_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 2 RACB" and course2_racb_dispo:
            import Course_2_RACB
            return Course_2_RACB.recuperer_donnees_course()
        elif choix_course == "Course 3 ASAF" and course3_asaf_dispo:
            import Course_3_ASAF
            return Course_3_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 3 RACB" and course3_racb_disp:
            import Course_3_RACB
            return Course_3_RACB.recuperer_donnees_course()
        else:
            import Essais
            return Essais.recuperer_donnees_course()

    # Si le script de calcul met plus de 2 secondes (Dropbox lent), on coupe l'attente pour afficher la page de suite
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(recuperer_sans_bloquer)
        res = future.result(timeout=2.0)
        if res and len(res) == 10:
            st.session_state["sauvegarde_loc_donnees"][choix_course] = res
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = res
except Exception:
    # Maintient l'affichage des anciennes données si Dropbox sature
    pass

st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

# Rendu de votre grille d'origine exacte
cg, cd = st.columns([1.3, 0.9])
with cg:
    st.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
    if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    if choix_course != "Essais":
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

# --- AUTOMATIQUE REFRESH NAVIGATEUR PUR SANS TOUCHER AU PROCESSEUR STREAMLIT ---
st.markdown("""
    <script>
        if (!window.autoRefreshSet) {
            window.autoRefreshSet = true;
            setTimeout(function() { window.parent.location.reload(); }, 30000);
        }
    </script>
""", unsafe_allow_html=True)
