import streamlit as st
import pandas as pd
import time

# --- CHARGEMENT DES MODULES DÉCOUPLÉ DU DÉMARRAGE ---
@st.cache_resource
def charger_modules_course():
    modules = {"Essais": None, "C1_ASAF": None, "C2_ASAF": None, "C3_ASAF": None, "C1_RACB": None, "C2_RACB": None, "C3_RACB": None}
    try: import Essais; modules["Essais"] = Essais
    except Exception: pass
    try: import Course_1_ASAF; modules["C1_ASAF"] = Course_1_ASAF
    except Exception: pass
    try: import Course_2_ASAF; modules["C2_ASAF"] = Course_2_ASAF
    except Exception: pass
    try: import Course_3_ASAF; modules["C3_ASAF"] = Course_3_ASAF
    except Exception: pass
    try: import Course_1_RACB; modules["C1_RACB"] = Course_1_RACB
    except Exception: pass
    try: import Course_2_RACB; modules["C2_RACB"] = Course_2_RACB
    except Exception: pass
    try: import Course_3_RACB; modules["C3_RACB"] = Course_3_RACB
    except Exception: pass
    return modules

st.set_page_config(page_title="Live", layout="wide")

# --- CSS INJECTÉ DE FORCE POUR LE CENTRAGE PARFAIT ET SERRÉ ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 5px !important; padding-bottom: 0px !important; padding-left: 1rem !important; padding-right: 1rem !important; }
div[data-testid="stMainBlockContainer"] { padding-top: 5px !important; margin-top: 0px !important; }
div[data-testid="stVerticalBlock"] { gap: 0rem !important; padding-top: 0px !important; }
div.stElementContainer { margin-top: 0px !important; margin-bottom: 0px !important; padding-top: 0px !important; padding-bottom: 0px !important; }

/* CENTRAGE ABSOLU ET ESPACE SERRÉ DU MENU */
div[data-testid="stHorizontalBlock"] {
    display: flex !important; justify-content: center !important; align-items: center !important; gap: 8px !important; width: 100% !important; margin: 0px auto !important;
}
div[data-testid="stHorizontalBlock"] > div { flex: none !important; width: auto !important; padding: 0px !important; margin: 0px !important; }

div.stButton > button {
    width: 130px !important; height: 24px !important; background-color: #F1F5F9 !important; color: #475569 !important;
    font-weight: bold !important; font-size: 0.82rem !important; border: 1px solid #CBD5E1 !important; border-radius: 3px !important;
    padding: 0px !important; margin: 0px !important; line-height: 22px !important; white-space: nowrap !important;
}

.titre-live, .titre-hist, .titre-classement { color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important; padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important; width: 100% !important; display: block !important; clear: both !important; }
.titre-live { background-color: #15803D !important; }
.titre-hist { background-color: #475569 !important; }
.titre-classement { background-color: #1E3A8A !important; }
.table-compacte { width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: fixed !important; }
.table-compacte tr { height: 18px !important; }
.table-compacte th, .table-compacte td { height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; vertical-align: middle !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }
.table-compacte td { border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
.table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }
</style>
""", unsafe_allow_html=True)
# Chargement ultra-sécurisé des modules au premier run
mods = charger_modules_course()

if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Détermination dynamique des boutons disponibles
colonnes_visibles = ["Essais"]
if mods["C1_ASAF"]: colonnes_visibles.append("Course 1 ASAF")
if mods["C1_RACB"]: colonnes_visibles.append("Course 1 RACB")
if mods["C2_ASAF"]: colonnes_visibles.append("Course 2 ASAF")
if mods["C2_RACB"]: colonnes_visibles.append("Course 2 RACB")
if mods["C3_ASAF"]: colonnes_visibles.append("Course 3 ASAF")
if mods["C3_RACB"]: colonnes_visibles.append("Course 3 RACB")

# Marge haute (10px)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Rendu natif des boutons dans une ligne
cols = st.columns([1.0] * len(colonnes_visibles))
for idx, nom_session in enumerate(colonnes_visibles):
    with cols[idx]:
        if st.button(nom_session, key=f"btn_nav_{idx}"):
            st.session_state["active_session"] = nom_session
            st.rerun()

# Rendu couleur du bouton actif
for idx, nom_session in enumerate(colonnes_visibles):
    if st.session_state["active_session"] == nom_session:
        st.markdown(f"""<style>div[data-testid="stHorizontalBlock"] > div:nth-child({idx+1}) button {{ background-color: #1E3A8A !important; color: white !important; border-color: #1E3A8A !important; }}</style>""", unsafe_allow_html=True)

# Marge basse symétrique (10px)
st.markdown("<div style='height: 10px; clear: both;'></div>", unsafe_allow_html=True)

choix_course = st.session_state["active_session"]
zone_affichage_pure = st.empty()

# --- FRAGMENT DE RENDU TOTALEMENT ISOLÉ ---
@st.fragment(run_every=30)
def rafraichir_uniquement_tableaux():
    d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    t_live, t_his, t_haut, t_milieu, t_bas = "Live", "Historique", "Classement Haut", "", ""
    
    try:
        # Sélection sécurisée du module
        m = mods["Essais"]
        if choix_course == "Course 1 ASAF": m = mods["C1_ASAF"]
        elif choix_course == "Course 1 RACB": m = mods["C1_RACB"]
        elif choix_course == "Course 2 ASAF": m = mods["C2_ASAF"]
        elif choix_course == "Course 2 RACB": m = mods["C2_RACB"]
        elif choix_course == "Course 3 ASAF": m = mods["C3_ASAF"]
        elif choix_course == "Course 3 RACB": m = mods["C3_RACB"]
        
        if m and hasattr(m, 'recuperer_donnees_course'):
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = m.recuperer_donnees_course()
        else:
            t_live = "⚠️ Module ou fonction indisponible"
    except Exception as e:
        t_live = f"⚠️ Erreur durant l'exécution : {str(e)}"

    with zone_affichage_pure.container():
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

rafraichir_uniquement_tableaux()
