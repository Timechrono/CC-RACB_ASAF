import streamlit as st
import pandas as pd
import time

# --- LOGIQUE D'IMPORT DIRECT SANS APPEL AU DÉMARRAGE ---
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

# --- STYLE GRAPHIQUE COMPACT + MENU TEXTUEL HORIZONTAL SURLIGNÉ ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }

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

/* LE MENU EN LIENS HORIZONTAUX SURLIGNÉS */
.barre-liens-cc {
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 20px !important;
    width: 100% !important;
    margin: 10px auto !important;
    font-family: sans-serif !important;
}
.lien-cc {
    color: #475569 !important;
    font-weight: bold !important;
    font-size: 0.95rem !important;
    text-decoration: none !important;
    padding-bottom: 2px !important;
    border-bottom: 2px solid transparent !important;
    cursor: pointer !important;
    background: none !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
}
.lien-cc:hover {
    color: #1E3A8A !important;
    border-bottom: 2px solid #CBD5E1 !important;
}
.lien-cc.actif {
    color: #1E3A8A !important;
    border-bottom: 2px solid #1E3A8A !important; /* Le surlignage bleu marqué */
    font-size: 1rem !important;
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
# Initialisation propre des variables dans l'état de session Streamlit
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Données en attente (Réseau Dropbox ralenti)</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Reconstitution de la liste des sessions
colonnes_visibles = ["Essais"]
if course1_disponible: colonnes_visibles.append("Course 1 ASAF")
if course1_racb_disponible: colonnes_visibles.append("Course 1 RACB")
if course2_disponible: colonnes_visibles.append("Course 2 ASAF")
if course2_racb_disponible: colonnes_visibles.append("Course 2 RACB")
if course3_disponible: colonnes_visibles.append("Course 3 ASAF")
if course3_racb_disponible: colonnes_visibles.append("Course 3 RACB")

# --- RENDU DU MENU DE LIENS TEXTUELS HORIZONTAUX SURLIGNÉS VIA LES SÉLECTEURS DE REQUÊTES NATIFS ---
html_menu = "<div class='barre-liens-cc'>"
for nom_session in colonnes_visibles:
    style_actif = "actif" if st.session_state["active_session"] == nom_session else ""
    html_menu += f'<a class="lien-cc {style_actif}" href="?session={encodeURIComponent(nom_session) if "encodeURIComponent" in locals() else nom_session.replace(" ", "%20")}" target="_self">{nom_session}</a>'
html_menu += "</div>"

# Affichage direct du menu textuel pur
st.markdown(html_menu, unsafe_allow_html=True)

# Interception instantanée du clic sur le lien via l'URL pour changer de tableau sans bug graphique
query_params = st.query_params
if "session" in query_params:
    session_cliquee = query_params["session"]
    if session_cliquee in colonnes_visibles and st.session_state["active_session"] != session_cliquee:
        st.session_state["active_session"] = session_cliquee
        st.rerun()

choix_course = st.session_state["active_session"]
terme_recherche = "Essais / Entraînements" if choix_course == "Essais" else choix_course

# Structures vides par défaut pour empêcher l'écran de se figer
d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
t_live, t_his, t_haut, t_milieu, t_bas = "Live Chrono", "Historique", "Classement Haut", "Classement Milieu", "Classement Bas"

# --- TIMEOUT DE SÉCURITÉ ABSOLU (MAX 2 SECONDES) POUR TUER DÉFINITIVEMENT LE ROND QUI TOURNE ---
try:
    from concurrent.futures import ThreadPoolExecutor
    import Essais

    def executer_calculs():
        if terme_recherche == "Course 1 ASAF" and course1_disponible: return Course_1_ASAF.recuperer_donnees_course()
        elif terme_recherche == "Course 1 RACB" and course1_racb_disponible: return Course_1_RACB.recuperer_donnees_course()
        elif terme_recherche == "Course 2 ASAF" and course2_disponible: return Course_2_ASAF.recuperer_donnees_course()
        elif terme_recherche == "Course 2 RACB" and course2_racb_disponible: return Course_2_RACB.recuperer_donnees_course()
        elif terme_recherche == "Course 3 ASAF" and course3_disponible: return Course_3_ASAF.recuperer_donnees_course()
        elif terme_recherche == "Course 3 RACB" and course3_racb_disponible: return Course_3_RACB.recuperer_donnees_course()
        else: return Essais.recuperer_donnees_course()

    # Si Dropbox met plus de 2.5 secondes à envoyer le fichier Excel, on coupe la connexion pour forcer l'affichage immédiat
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(executer_calculs)
        res = future.result(timeout=2.5)
        if res and len(res) == 10:
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = res
except Exception:
    t_live = "🔄 Synchronisation avec Dropbox en cours... (Affichage fluide maintenu)"

# --- RENDU DE VOTRE PRÉSENTATION ET DE VOS TABLEAUX D'ORIGINE ---
cg, cd = st.columns([1.3, 0.9])
with cg:
    if t_live: st.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
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

# --- REFRESH INVISIBLE GÉRÉ PAR LE NAVIGATEUR (ZÉRO UTILISATION DE PYTHON SOU SOUVRAINE) ---
st.markdown("""
    <script>
        if (!window.autoRefreshSet) {
            window.autoRefreshSet = true;
            setTimeout(function() { window.parent.location.reload(); }, 30000);
        }
    </script>
""", unsafe_allow_html=True)
