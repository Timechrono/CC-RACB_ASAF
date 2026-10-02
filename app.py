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

# --- CONCEPTION GRAPHIQUE RIGIDE ET BLOC BARRE DE NAVIGATION ---
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
.table-live td:last-child, .table-live td:last-child, .table-class-robuste td:last-child { font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }

/* RECTIFICATION IMPORTANTE : ALIGNEMENT PARFAIT DE LA LIGNE ST.PILLS + COMPTEUR */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
}

/* Force les boutons st.pills à se coller régulièrement avec un écart fixe de 6px */
div[data-testid="stWidgetLabel"] { display: none !important; }
div[role="listbox"] {
    gap: 6px !important;
}

/* Style uniforme des pilules (hauteur 24px, texte gras et encadré) */
div[role="option"] {
    height: 24px !important;
    padding: 0px 14px !important;
    font-weight: bold !important;
    font-size: 0.82rem !important;
    line-height: 22px !important;
    border-radius: 3px !important;
    background-color: #F1F5F9 !important;
    color: #475569 !important;
    border: 1px solid #CBD5E1 !important;
    transition: all 0.15s ease !important;
}

/* Changement de couleur de la pilule active (Bleu marqué de course) */
div[aria-selected="true"] {
    background-color: #1E3A8A !important;
    color: white !important;
    border-color: #1E3A8A !important;
}

/* SÉPARATEUR DE SÉCURITÉ DE 22PX POUR BLOQUER LA FEUILLE EN DESSOUS */
.separateur-statique {
    height: 22px !important;
    margin-bottom: 4px !important;
    clear: both !important;
    display: block !important;
}

.label-decompte-pure-txt {
    font-size: 0.85rem !important;
    font-weight: bold !important;
    color: #1E3A8A !important;
    line-height: 24px !important;
    white-space: nowrap !important;
    display: inline-block !important;
    text-align: right !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
if "active_session" not in st.session_state:
    st.session_state["active_session"] = "Essais"

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df.empty: return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# Assemblage des onglets du menu horizontal
colonnes_menu = ["Essais"]
if course1_disponible: colonnes_menu.append("Course 1 ASAF")
if course1_racb_disponible: colonnes_menu.append("Course 1 RACB")
if course2_disponible: colonnes_menu.append("Course 2 ASAF")
if course2_racb_disponible: colonnes_menu.append("Course 2 RACB")
if course3_disponible: colonnes_menu.append("Course 3 ASAF")
if course3_racb_disponible: colonnes_menu.append("Course 3 RACB")

# Définition de deux colonnes asymétriques : une grande pour les boutons collés, une petite pour le décompte
cols = st.columns([4.0, 1.0], vertical_alignment="center")

with cols[0]:
    # Utilisation du composant st.pills pour un espacement horizontal natif et rigide au millimètre
    choix_selectionne = st.pills(
        "Session_Label", 
        options=colonnes_menu, 
        default=st.session_state["active_session"], 
        label_visibility="collapsed",
        key="active_pills_nav"
    )
    if choix_selectionne != st.session_state["active_session"]:
        st.session_state["active_session"] = choix_selectionne
        st.rerun()

# Utilisation de la colonne de droite pour afficher le décompte en texte brut
zone_decompte_txt = cols[1].empty()

# Insertion du séparateur statique de 22px
st.markdown("<div class='separateur-statique'></div>", unsafe_allow_html=True)
choix_course = st.session_state["active_session"]

# Conteneur d'affichage pur (Anti-miroir / Anti-reliquat)
zone_affichage_pure = st.empty()

# --- FRAGMENT CENTRALISÉ DÉDIÉ UNIQUEMENT AUX CLASSEMENTS (Toutes les 30s) ---
@st.fragment(run_every=30)
def rafraichir_uniquement_tableaux():
    st.cache_data.clear()
    
    terme_recherche = "Essais / Entraînements" if choix_course == "Essais" else choix_course

    if terme_recherche == "Course 1 ASAF" and course1_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_ASAF.recuperer_donnees_course()
    elif terme_recherche == "Course 1 RACB" and course1_racb_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_1_RACB.recuperer_donnees_course()
    elif terme_recherche == "Course 2 ASAF" and course2_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_ASAF.recuperer_donnees_course()
    elif terme_recherche == "Course 2 RACB" and course2_racb_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_2_RACB.recuperer_donnees_course()
    elif terme_recherche == "Course 3 ASAF" and course3_disponible:
        d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = Course_3_ASAF.recuperer_donnees_course()
    elif terme_recherche == "Course 3 RACB" and course3_racb_disponible:
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

# --- MINI-FRAGMENT ISOLÉ DÉDIÉ UNIQUEMENT À L'HORLOGE COMPTEUR (Toutes les 1s) ---
@st.fragment(run_every=1)
def faire_tourner_le_compteur():
    if "chrono_sec" not in st.session_state:
        st.session_state["chrono_sec"] = 30
    
    st.session_state["chrono_sec"] -= 1
    if st.session_state["chrono_sec"] <= 0:
        st.session_state["chrono_sec"] = 30
        
    zone_decompte_txt.markdown(f"<span class='label-decompte-pure-txt'>⏱️ Rafraîchissement dans : {st.session_state['chrono_sec']}s</span>", unsafe_allow_html=True)

# Lancement coordonné
rafraichir_uniquement_tableaux()
faire_tourner_le_compteur()
