# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1


import streamlit as st
import pandas as pd
import time
import requests
import io
import Essais

# Initialisation préventive globale de toutes les variables pour éviter le NameError
d_liv = pd.DataFrame()
d_his = pd.DataFrame()
d_haut = pd.DataFrame()
d_milieu = pd.DataFrame()
d_bas = pd.DataFrame()

t_live = "🏎️ EN DIRECT / Derniers concurrents partis"
t_his = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents RACB"
t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX RACB"
t_milieu = "📊 CLASSEMENT OFFICIEUX PAR Groupe / Classe (Top 3)"
t_bas = ""

# ==============================================================================
# ⚠️ LIEN DROPBOX LOGO
# ==============================================================================
LIEN_DROPBOX_LOGO = "https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1"

# --- DÉTECTION DES SCRIPTS DE COURSE DISPONIBLES ---
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

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE UNIFIÉE ---
st.markdown(f"""
<style>
/* Masquer le bandeau blanc et la mention Built with Streamlit */
footer {{ visibility: hidden !important; }}
[data-testid="stFooterContainer"] {{ display: none !important; }}

[data-testid="stHeader"] {{ display: none !important; }}
button:focus, div:focus, input:focus, select:focus {{
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}}

/* RESTAURATION COMPLÈTE DU SCROLL SUR TOUTE LA PAGE WEB */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
    overflow: auto !important;
    overflow-y: auto !important;
    height: auto !important;
    max-height: none !important;
}}

.block-container {{ 
    padding-top: 5px !important; 
    padding-bottom: 0rem !important; 
    padding-left: 0.5rem !important; 
    padding-right: 0.5rem !important; 
}}

div[data-testid="stVerticalBlock"] {{
    gap: 0rem !important;
    padding-top: 0px !important;
}}
div.stElementContainer {{
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}}

/* AJUSTEMENT 1 : HAUTEUR PHYSIQUE DU BANDEAU DE TITRE A 24PX */
/* REGLAGE DU TITRE A 24PX AVEC EMOJI DE SCROLL REPOUSSÉ À DROITE */
.titre-live, .titre-hist, .titre-classement {{
    color: #FFFFFF !important; font-size: 1.02rem !important; font-weight: bold !important;
    height: 26px !important; max-height: 26px !important;
    padding: 0px 8px !important; border-radius: 3px !important;
    width: 100% !important; clear: both !important;
    /* STRUCTURE FLEXBOX POUR CHASSER L'EMOJI A DROITE */
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}}

.titre-live {{ background-color: #15803D !important; margin-top: 0px !important; margin-bottom: 6px !important; }}
.titre-hist {{ background-color: #475569 !important; margin-top: 15px !important; margin-bottom: 6px !important; }}
.titre-classement {{ background-color: #1E3A8A !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

.table-hist td:last-child {{ 
    font-weight: bold !important; 
    color: #0F172A !important; 
}}

.refresh-bleu-clair-historique {{
    color: #064E3B !important;
    background-color: #DCF2E8 !important;
    border: 1px solid #3B8F44 !important;
    font-weight: bold !important;
    font-size: 13px !important;           /* TAILLE INTERMÉDIAIRE IDÉALE */
    padding: 1px 6px !important;          /* REHAUSSÉ LÉGÈREMENT POUR REDONNER DE L'AIR */
    line-height: 16px !important;         /* HAUTEUR AJUSTÉE POUR RESTER COMPACTE */
    border-radius: 4px !important;
    display: inline-block !important;
    margin-left: 4px !important;
    vertical-align: middle !important;    /* MAINTIENT LE CENTRAGE HORIZONTAL */
}}




.espace-classement-suivant {{
    margin-top: 15px !important;
}}

/* BOÎTES DE SCROLL INTERNES CLOISONNÉES AUTONOMES COORDONNÉES */
.div-scroll-local-historique {{
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
}}
/* AJUSTEMENT 2 : HAUTEUR DE L'HISTORIQUE SUR PC FORCEE A 456PX */
@media (min-width: 769px) {{
    .div-scroll-local-historique {{
        height: 456px !important;
        max-height: 456px !important;
        overflow-y: auto !important;
    }}
}}

/* Hauteur sur-mesure sur PC pour s'aligner avec le bas de la colonne de droite */
@media (min-width: 769px) {{
    .div-scroll-local-historique {{
        height: 456px !important;
        max-height: 456px !important;
        overflow-y: auto !important;
    }}
}}


# fin bloc 1

source: 1




# fin bloc 2

# --- LECTURE DU PARAMÈTRE DE COURSE DEPUIS L'URL ---
query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()

if choix_course_url == "c1asaf" and course1_disponible:
    choix_course = "Course 1 ASAF"
elif choix_course_url == "c1racb" and course1_racb_disponible:
    choix_course = "Course 1 RACB"
elif choix_course_url == "c2asaf" and course2_disponible:
    choix_course = "Course 2 ASAF"
elif choix_course_url == "c2racb" and course2_racb_disponible:
    choix_course = "Course 2 RACB"
elif choix_course_url == "c3asaf" and course3_disponible:
    choix_course = "Course 3 ASAF"
elif choix_course_url == "c3racb" and course3_racb_disponible:
    choix_course = "Course 3 RACB"
else:
    choix_course = "Essais"

try:
    from concurrent.futures import ThreadPoolExecutor

    def recuperer_avec_timeout():
        if choix_course == "Course 1 ASAF": return Course_1_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 1 RACB": return Course_1_RACB.recuperer_donnees_course()
        elif choix_course == "Course 2 ASAF": return Course_2_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 2 RACB": return Course_2_RACB.recuperer_donnees_course()
        elif choix_course == "Course 3 ASAF": return Course_3_ASAF.recuperer_donnees_course()
        elif choix_course == "Course 3 RACB": return Course_3_RACB.recuperer_donnees_course()
        else: return Essais.recuperer_donnees_course()

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(recuperer_avec_timeout)
        res = future.result(timeout=3.5)
        if res and len(res) == 10:
            d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = res
except Exception as e:
    t_live = "⚠️ Liaison Dropbox ralentie ou instable — Tentative de reconnexon en cours..."

st.markdown("<style>@media (min-width: 769px) { .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 8% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 32% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 28% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 5% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 17% !important; } }</style>", unsafe_allow_html=True)

if t_haut and "TOP 20" in t_haut.upper():
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX RACB"

# CORRECTION DU BLOCAGE ICI : FORCE STRICTEMENT LE BRIDAGE VISUEL À 10 LIGNES (215PX) POUR LES ESSAIS
if "ESSAIS" in choix_course.upper():
    h_pc = "215px"
elif "COURSE 1" in choix_course.upper():
    h_pc = "425px"
else:
    h_pc = "380px"

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    if t_his: 
        st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    h_mob = "380px"

    # Construction du CSS sans triple guillemet pour empêcher tout crash de syntaxe Python
    style_ligne_1 = "@media (min-width: 769px) { .ajust-hauteur-pc { max-height: " + str(h_pc) + " !important; } }"
    style_ligne_2 = "@media (max-width: 768px) { .ajust-hauteur-pc { max-height: " + str(h_mob) + " !important; } }"
    
    st.markdown("<style>" + style_ligne_1 + "\n" + style_ligne_2 + "</style>", unsafe_allow_html=True)

    # Repère fixe universel pour la navigation tactile smartphone
    st.markdown("<div id='zone-classements-droite'></div>", unsafe_allow_html=True)

    if choix_course != "Essais":
        # --- MODE DE COURSE ---
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'>{gen_html(d_haut, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'>{gen_html(d_milieu, 'table-class-milieu')}</div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            nb_lignes = len(d_bas) if hasattr(d_bas, '__len__') else 0
            style_scroll = "class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'" if nb_lignes > 10 else "style='height: auto; display: block;'"
            st.markdown(f"<div {style_scroll}>{gen_html(d_bas, 'table-class-robuste')}</div>", unsafe_allow_html=True)
    else:
        # --- MODE ESSAIS ---
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'>{gen_html(d_bas, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'>{gen_html(d_haut, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            
            # APPLICATION BRIDAGE : Encapsulation dans le conteneur forcé à 114px pour la Division 4 en mode Essais
            st.markdown(f"<div class='div-scroll-local-div4'>{gen_html(d_milieu, 'table-class-robuste')}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='signature-fin-page'>
    <img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>
    www.timechrono.be
</div>
""", unsafe_allow_html=True)

# CODE ACTUEL DE REFRESH
for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis / <span class='refresh-bleu-clair-historique'>Refresh {secondes_restantes} Sec.</span></span>", unsafe_allow_html=True)
    else:
        conteneur_titre_live.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    if secondes_restantes > 0:
        time.sleep(1)

st.rerun()
