import streamlit as st
import pandas as pd
import time
import Essais

# --- RECHERCHE AND CHARGEMENT DES SESSIONS ASAF ---
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

# --- RECHERCHE AND CHARGEMENT DES SESSIONS RACB ---
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

# --- INTERCEPTION ET GESTION DES CLICS VIA URL (ANTI-CLIGNOTEMENT CRITIQUE) ---
# Définition de l'onglet actif initial
if "session" not in st.query_params:
    st.query_params["session"] = "Essais"
choix_course = st.query_params["session"]

# --- STYLE CSS DU MENU EN BÉTON ARMÉ (SANS COLONNES STREAMLIT) ---
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }

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

/* LARGEURS DES EN-TÊTES DE TABLEAUX */
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

/* LA BARRE HORIZONTALE UNIQUE SANS COMPOSANT SÉISMIQUE */
.barre-horizontale-statique {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 6px !important; /* Distance fixe et serrée de 6px */
    width: 100% !important;
    height: 26px !important;
    margin-bottom: 0px !important;
    padding: 0px !important;
}

/* FORMAT DU BOUTON EN LIEN HTML HYPER STABLE */
.ong-btn-cc {
    display: inline-block !important;
    height: 24px !important;
    background-color: #F1F5F9 !important;
    color: #475569 !important;
    font-weight: bold !important;
    font-size: 0.82rem !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 3px !important;
    padding: 0px 14px !important;
    line-height: 22px !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    text-align: center !important;
    transition: all 0.1s ease !important;
}
.ong-btn-cc:hover {
    border-color: #1E3A8A !important;
    color: #1E3A8A !important;
    background-color: #E0F2FE !important;
}

/* MARQUAGE BLEU SUR LE BOUTON SÉLECTIONNÉ */
.ong-btn-cc.actif {
    background-color: #1E3A8A !important;
    color: white !important;
    border-color: #1E3A8A !important;
}

/* TEXTE DU COMPTEUR REPOUSSÉ STRICTEMENT À DROITE SANS CADRE COULEUR */
.compteur-txt-pur {
    font-size: 0.85rem !important;
    font-weight: bold !important;
    color: #1E3A8A !important;
    line-height: 26px !important;
    margin-left: auto !important; /* Force le placement en fin de ligne horizontale */
    white-space: nowrap !important;
}

/* ESPACEMENT LÉGÈREMENT AUGMENTÉ ET PARFAITEMENT IMMOBILE AVEC LA FEUILLE DU DESSOUS */
.separateur-final-fixe {
    height: 22px !important;
    display: block !important;
    clear: both !important;
}
</style>
""", unsafe_allow_html=True)
# Construction de la ligne d'onglets stables
onglets = [("Essais", "Essais")] # RECTIFICATION : Le libellé affiche à nouveau "Essais"
if course1_disponible: onglets.append(("Course 1 ASAF", "Course 1 ASAF"))
if course1_racb_disponible: onglets.append(("Course 1 RACB", "Course 1 RACB"))
if course2_disponible: onglets.append(("Course 2 ASAF", "Course 2 ASAF"))
if course2_racb_disponible: onglets.append(("Course 2 RACB", "Course 2 RACB"))
if course3_disponible: onglets.append(("Course 3 ASAF", "Course 3 ASAF"))
if course3_racb_disponible: onglets.append(("Course 3 RACB", "Course 3 RACB"))

# --- GÉNÉRATION EN INJECTION DIRECTE DU MENU HORIZONTALE (ZÉRO CLIGNOTEMENT) ---
html_menu = '<div class="barre-horizontale-statique">'
for libelle, code_id in onglets:
    style_actif = "actif" if choix_course == code_id else ""
    html_menu += f'<a class="ong-btn-cc {style_actif}" href="?session={code_id}" target="_self">{libelle}</a>'

# Ajout du point d'ancrage textuel pour l'horloge à l'extrémité droite
html_menu += '<span id="zone-chrono-txt" class="compteur-txt-pur">⏱️ Rafraîchissement dans : 30s</span>'
html_menu += '</div>'

st.markdown(html_menu, unsafe_allow_html=True)
st.markdown('<div class="separateur-final-fixe"></div>', unsafe_allow_html=True)

# Conteneurs de réception pur (Anti-miroir)
zone_affichage_pure = st.empty()
zone_compteur_isole = st.empty()

# --- FRAGMENT INDÉPENDANT DÉDIÉ UNIQUEMENT AUX TABLEAUX (Toutes les 30s) ---
# Il s'exécute sans jamais toucher ni redessiner le menu du haut !
@st.fragment(run_every=30)
def rafraichir_uniquement_tableaux():
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
            st.markdown(df_live.to_html(index=False, classes="table-compacte table-live", escape=False, border=0) if not d_liv.empty else gen_html(d_liv, "table-live"), unsafe_allow_html=True)
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

# --- MINI-FRAGMENT DÉDIÉ UNIQUEMENT À LA MISE À JOUR DU TEXTE DU COMPTEUR ---
# Modifie uniquement la valeur du texte sans faire sauter l'écran
@st.fragment(run_every=1)
def faire_tourner_le_compteur():
    if "chrono_sec" not in st.session_state:
        st.session_state["chrono_sec"] = 30
    st.session_state["chrono_sec"] -= 1
    if st.session_state["chrono_sec"] <= 0:
        st.session_state["chrono_sec"] = 30
    
    # Injection JavaScript ultra-légère pour écraser la valeur textuelle à droite sans faire sauter les boutons
    st.markdown(f"""<script>document.getElementById("zone-chrono-txt").innerText = "⏱️ Rafraîchissement dans : {st.session_state['chrono_sec']}s";</script>""", unsafe_allow_html=True)

# Exécution fluide en tâche de fond
rafraichir_uniquement_tableaux()
faire_tourner_le_compteur()
