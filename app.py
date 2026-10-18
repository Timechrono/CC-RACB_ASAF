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
st.set_page_config(menu_items=None) 

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE UNIFIÉE ---
st.markdown(f"""

<style>

/* 1. DISPARITION TOTALE ET RADICALE DES COMPOSANTS STREAMLIT (PC & MOBILE) */
footer, 
[data-testid="stFooterContainer"], 
[data-testid="stStatusWidget"], 
.stStatusWidget,
[data-testid="stHeader"], 
[data-testid="stDecoration"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    max-height: 0px !important;
    min-height: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
    overflow: hidden !important;
    opacity: 0 !important;
    line-height: 0 !important;
    font-size: 0 !important;
}}

/* L'ASTUCE RADICALE POUR SUPPRIMER TOUT ESPACE ET LE FOOTER HORS DE L'ÉCRAN SUR PC */
@media (min-width: 769px) {{
    footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget {{
        position: fixed !important;
        bottom: -1000px !important; /* Poussé encore plus loin pour libérer l'iframe */
        z-index: -9999 !important;
        height: 0px !important;
    }}
}}

@media (max-width: 768px) {{
    footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget {{
        position: static !important;
        bottom: auto !important;
        transform: none !important;
    }}
}}

button:focus, div:focus, input:focus, select:focus {{
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}}

/* 2. CONFIGURATION DE LA PAGE ET RECUPERATION DE L'ESPACE MAXIMUM SUR PC */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
    overflow: hidden !important; 
    height: 100vh !important;    
    max-height: 100vh !important;
    padding-bottom: 0px !important; /* Force la suppression de toute marge Streamlit */
    margin-bottom: 0px !important;
}}


/* Réduction des marges globales de Streamlit pour gagner de la place */
.block-container {{ 
    padding-top: 5px !important; 
    padding-left: 0.5rem !important; 
    padding-right: 0.5rem !important; 
}}

/* Libère l'espace du bas : plus aucun pixel perdu sur PC */
@media (min-width: 769px) {{
    .block-container {{ 
        padding-bottom: 0px !important; /* Réduit à 0 pour empêcher de pousser l'iframe parent */
    }}
}}
@media (max-width: 768px) {{
    .block-container {{ 
        padding-bottom: 25px !important; 
    }}
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

/* 3. STRUCTURATION DES BANDEAUX DE TITRES GRAPHIQUES */
.titre-live, .titre-hist, .titre-classement {{
    color: #FFFFFF !important; font-size: 1.02rem !important; font-weight: bold !important;
    height: 26px !important; max-height: 26px !important;
    padding: 0px 8px !important; border-radius: 3px !important;
    width: 100% !important; clear: both !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}}

.titre-live {{ background-color: #15803D !important; margin-top: 0px !important; margin-bottom: 6px !important; }}
.titre-hist {{ background-color: #475569 !important; margin-top: 15px !important; margin-bottom: 6px !important; }}
.titre-classement {{ background-color: #1E3A8A !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

.refresh-bleu-clair-historique {{
    color: #064E3B !important;
    background-color: #DCF2E8 !important;
    border: 1px solid #3B8F44 !important;
    font-weight: bold !important;
    font-size: 13px !important;
    padding: 1px 6px !important;
    line-height: 16px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-left: 4px !important;
    vertical-align: middle !important;
}}

.espace-classement-suivant {{
    margin-top: 15px !important;
}}

/* 4. BLOCS DE SCROLL INTERNES CLOISONNÉS */
.div-scroll-local-historique {{
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
}}

.div-scroll-local-general, .div-scroll-local-classes {{
    height: auto !important;
    max-height: none !important;
    overflow-y: visible !important;
    width: 100% !important;
    border: none !important;
}}

@media (min-width: 769px) {{
    .div-scroll-local-historique {{
        height: 456px !important;
        max-height: 456px !important;
        overflow-y: auto !important;
        display: block !important;
    }}
    .div-scroll-local-div4 {{
        height: 114px !important;
        max-height: 114px !important;
        overflow-y: auto !important;
        width: 100% !important;
        display: block !important;
    }}
}}

@media (max-width: 768px) {{
    .block-container {{ padding-left: 2px !important; padding-right: 2px !important; }}
    
    .div-scroll-local-historique {{
        height: 1025px !important;
        max-height: 1025px !important;
        overflow-y: auto !important;
        display: block !important;
        -webkit-overflow-scrolling: touch !important;
        border: 1px solid #CBD5E1 !important;
    }}
    .div-scroll-local-div4 {{
        height: auto !important;
        max-height: none !important;
        overflow-y: visible !important;
        display: block !important;
    }}
}}

/* 5. DESIGN ET RENDU COMPACT DES TABLEAUX */
.table-responsive-container {{
    width: 100% !important;
}}
.table-compacte {{
    width: 100% !important; margin-bottom: 0px !important;
    border-collapse: collapse !important; table-layout: auto !important;
}}
.table-compacte tr {{ height: 18px !important; }}
.table-compacte th, .table-compacte td {{ 
    height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; 
    font-size: 0.85rem !important; color: #000000 !important; vertical-align: middle !important; 
    white-space: nowrap !important; 
}}
.table-compacte td {{ border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }}
.table-compacte th {{ font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }}

.table-live td:last-child, .table-class-robuste td:last-child, .table-hist td:last-child {{ 
    font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; 
}}
.table-hist tr:nth-child(odd) td {{ background-color: #E0F2FE !important; }}

@media (max-width: 768px) {{
    .table-compacte th, .table-compacte td {{ 
        font-size: 0.65rem !important; 
        padding: 1px 2px !important; 
        height: 25px !important; 
    }}
    .table-hist td:nth-child(4) {{ max-width: 32px !important; overflow: hidden !important; text-overflow: clip !important; white-space: nowrap !important; }}
    .table-compacte td:nth-child(3), table td:nth-child(3) {{ max-width: 60px !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }}
    .table-live td:last-child, .table-class-robuste td:last-child {{ font-size: 0.70rem !important; }}
    
    .titre-live, .titre-hist, .titre-classement {{
        height: auto !important;
        max-height: none !important;
        line-height: 1.3 !important;
        padding: 4px 8px !important;
    }}
}}

.table-class-robuste tr.ligne-bleue-separation td,
tr.ligne-separation-classe td, 
.table-compacte tr.ligne-separation-classe td {{ 
    box-shadow: inset 0 -3px 0 0 #1E3A8A !important; 
}}

/* 6. SIGNATURE DE FIN DE PAGE ET AJUSTEMENT DU DESIGN */
@media (min-width: 769px) {{
    .signature-fin-page {{
        position: fixed !important;
        bottom: 0px !important;
        left: 0.5rem !important;
        right: 0.5rem !important;
        width: calc(100% - 1rem) !important;
        background-color: #FFFFFF !important; /* Crée un fond propre pour que les tableaux défilent derrière si besoin */
        z-index: 9999 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 12px !important;
        text-align: center !important;
        color: #1E3A8A !important;
        font-size: 0.92rem !important;
        font-weight: bold !important;
        padding: 4px 0px !important;
        margin: 0px !important;
        border-top: 1px dashed #1E3A8A !important;
    }}
}}

@media (max-width: 768px) {{
    .signature-fin-page {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 12px !important;
        text-align: center !important;
        color: #1E3A8A !important;
        font-size: 0.75rem !important; 
        padding-top: 4px !important; 
        margin-top: 25px !important;
        margin-bottom: 30px !important; /* Conserve la sécurité smartphone intacte */
        border-top: 1px dashed #1E3A8A !important;
        width: 100% !important;
    }}
}}

.logo-signature {{
    height: 24px !important;
    width: auto !important;
    vertical-align: middle !important;
}}

@media (max-width: 768px) {{
    .logo-signature {{ height: 32px !important; }}
}}


</style>





""", unsafe_allow_html=True)

def gen_html(df, cl):
    # Sécurisation préventive des variables de session ou d'URL
    if cl == "table-hist":
        phrase_attente = "En attente d'arrivée..."
    elif cl in ["table-class-robuste", "table-class-groupes", "table-class-milieu"]:
        nom_course = choix_course.upper() if 'choix_course' in globals() else ""
        if "RACB" in nom_course:
            phrase_attente = "En attente du premier classé RACB..."
        elif "ASAF" in nom_course:
            phrase_attente = "En attente du premier classé ASAF..."
        else:
            phrase_attente = "En attente du premier classé..."
    else:
        phrase_attente = "En attente du départ..."

    # Définition propre du conteneur
    style_conteneur = "class='div-scroll-local-historique'" if cl == "table-hist" else "class='table-responsive-container'"

    if isinstance(df, str):
        if "<TABLE" in df.upper() and "</TABLE>" in df.upper():
            debut = df.upper().find("<TABLE")
            fin = df.upper().find("</TABLE>") + 8
            tableau_propre = df[debut:fin]
            return f"<div {style_conteneur}>{tableau_propre}</div>"
                
        tableau_vide = f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table>"
        return f"<div {style_conteneur}>{tableau_vide}</div>"

    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        tableau_vide = f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table>"
        return f"<div {style_conteneur}>{tableau_vide}</div>"
    
    html_table = df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)
    return f"<div {style_conteneur}>{html_table}</div>"




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

    # Injection CSS dynamique
    st.markdown(f"""
    <style>
      @media (min-width: 769px) {{ .ajust-hauteur-pc {{ max-height: {h_pc} !important; }} }}
      @media (max-width: 768px) {{ .ajust-hauteur-pc {{ max-height: {h_mob} !important; }} }}
    </style>
    """, unsafe_allow_html=True)

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

# CODE ACTUEL
for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis / <span class='refresh-bleu-clair-historique'>Refresh {secondes_restantes} Sec.</span></span>", unsafe_allow_html=True)
    else:
        conteneur_titre_live.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    if secondes_restantes > 0:
        time.sleep(1)

st.rerun()
