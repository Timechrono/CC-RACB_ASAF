import streamlit as st
import pandas as pd
import time
import requests
import io
import Essais

# --- CHARGEMENT COMPLET DE TOUTES LES COURSES ---
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

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE SANS MARGE BLANCHE ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
button:focus, div:focus, input:focus, select:focus {
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}

/* 1. COMPACITÉ DE LA ZONE SUPERIEURE */
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

/* STRUCTURE DU CONTENEUR DE BOUTONS HTML PUR (SÉCURITÉ PREMIER CLIC) */
.menu-horizontal-fixe {
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 10px !important;
    margin-top: 10px !important;    /* Marge haute exacte de 10px */
    margin-bottom: 10px !important; /* Marge basse exacte de 10px */
    width: 100% !important;
}

/* STYLE UNIQUE POUR LES BOUTONS DU MENU SANS CONFLIT AVEC STREAMLIT */
.btn-nav-cc {
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
}
.btn-nav-cc.actif {
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

/* LARGEURS DES TABLEAUX */
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
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Données indisponibles (Vérifiez Dropbox)</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Assemblage ordonné des options de session
colonnes_visibles = ["Essais"]
if course1_disponible: colonnes_visibles.append("Course 1 ASAF")
if course1_racb_disponible: colonnes_visibles.append("Course 1 RACB")
if course2_disponible: colonnes_visibles.append("Course 2 ASAF")
if course2_racb_disponible: colonnes_visibles.append("Course 2 RACB")
if course3_disponible: colonnes_visibles.append("Course 3 ASAF")
if course3_racb_disponible: colonnes_visibles.append("Course 3 RACB")

# --- CONSTRUTION DU MENU EN HTML PUR INATTAQUABLE ---
# Injection de boutons HTML avec un script d'écoute pour renvoyer le choix à Streamlit sans doublon
html_menu = "<div class='menu-horizontal-fixe'>"
for nom_session in colonnes_visibles:
    classe_actif = "actif" if st.session_state["active_session"] == nom_session else ""
    html_menu += f"<button class='btn-nav-cc {classe_actif}' onclick=\"window.parent.postMessage({{type: 'set_session', val: '{nom_session}'}}, '*');\">{nom_session}</button>"
html_menu += "</div>"

st.markdown(html_menu, unsafe_allow_html=True)

# Réception sécurisée du clic HTML pour changer la session dans Streamlit
st.markdown("""
    <script>
        window.addEventListener('message', function(e) {
            if (e.data && e.type === 'set_session') {
                const inputs = window.parent.document.querySelectorAll('input');
                // Force le stockage interne de Streamlit à se mettre à jour
                window.parent.location.hash = '?session=' + encodeURIComponent(e.data.val);
            }
        });
    </script>
""", unsafe_allow_html=True)

# Récupération de la session cliquée via les query params (natif et ultra-rapide)
query_params = st.query_params
if "session" in query_params:
    session_cliquee = query_params["session"]
    if session_cliquee in colonnes_visibles and st.session_state["active_session"] != session_cliquee:
        st.session_state["active_session"] = session_cliquee
        st.rerun()

choix_course = st.session_state["active_session"]

# Structures de calcul d'origine
d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
t_live, t_his, t_haut, t_milieu, t_bas = "Chronométrage", "Historique", "Classement Haut", "Classement Milieu", "Classement Bas"

try:
    from concurrent.futures import ThreadPoolExecutor

    def recuperer_avec_timeout():
        if choix_course == "Course 1 ASAF" and course1_disponible: return Course_1_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 1 RACB" and course1_racb_disponible: return Course_1_RACB.recuperer_donnees_course()
        elif choix_course == "Course 2 ASAF" and course2_disponible: return Course_2_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 2 RACB" and course2_racb_disponible: return Course_2_RACB.recuperer_donnees_course()
        elif choix_course == "Course 3 ASAF" and course3_disponible: return Course_3_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 3 RACB" and course3_racb_disponible: return Course_3_RACB.recuperer_donnees_course()
        else: return Essais.recuperer_donnees_course()

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(recuperer_avec_timeout)
        res = future.result(timeout=3.5)
        if res and len(res) == 10:
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = res
except Exception as e:
    t_live = "⚠️ Liaison Dropbox ralentie ou instable — Tentative de reconnexon en cours..."

st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

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

st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# Rafraîchissement automatique toutes les 30 secondes via navigateur pur
st.markdown("""
    <script>
        if (!window.autoRefreshSet) {
            window.autoRefreshSet = true;
            setTimeout(function() { window.parent.location.reload(); }, 30000);
        }
    </script>
""", unsafe_allow_html=True)
