# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
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

# ==============================================================================
# ⚠️ LIEN DROPBOX LOGO
# ==============================================================================
LIEN_DROPBOX_LOGO = "https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1"

# --- DÉTECTION DES SCRIPTS DE COURSE DISPONIBLES ---
module_actif = Essais # Par défaut

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

# [Conservez tout le début de votre fichier inchangé jusqu'à la configuration CSS]

st.set_page_config(page_title="Live", layout="wide")
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

/* 1. EMPECHE LA DUPLICATION FANTÔME ET L'EFFET MIROIR DU RECHARGEMENT */
div[data-stale="true"], 
div[data-stale="true"] *,
[data-testid="stRenderLoading"],
[data-testid="stRenderLoading"] * {{
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    max-height: 0px !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
}}

/* 2. FORCE L'APPLICATION ACTUELLE ET LE TEXTE EN COURS A RESTER NETS ET VISIBLES */
div[data-stale="false"],
[data-testid="stAppViewContainer"], 
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"] {{
    opacity: 1 !important;
    filter: none !important;
}}

/* 3. DESACTIVE LE SQUELETTE DE CHARGEMENT SOUVENT RESPONSABLE DU SOUCI */
[data-testid="stSkeleton"] {{
    display: none !important;
    height: 0px !important;
}}

/* L'ASTUCE SUR PC : ON EXTRACT LE PIED DE PAGE HORS DE L'ESPACE DE CALCUL DU NAVIGATEUR */
@media (min-width: 769px) {{
    footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget {{
        position: fixed !important;
        bottom: -500px !important;
        transform: translateY(500px) !important;
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
    overflow: auto !important;
    overflow-y: auto !important;
    height: auto !important;
    max-height: none !important;
}}

.block-container {{ 
    padding-top: 5px !important; 
    padding-left: 0.5rem !important; 
    padding-right: 0.5rem !important; 
}}

@media (min-width: 769px) {{
    .block-container {{ 
        padding-bottom: 50px !important; /* Marge de sécurité pour laisser place à la signature fixe sur PC */
    }}
}}

@media (max-width: 768px) {{
    .block-container {{ 
        padding-bottom: 20px !important; /* Réduit sur mobile car la signature ne flotte plus */
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

/* 4. BLOCS DE SCROLL INTERNES COUCHE TACTILE MOBILE */
.div-scroll-local-historique {{
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
    -webkit-overflow-scrolling: touch !important;
}}

.div-scroll-local-general, .div-scroll-local-classes {{
    height: auto !important;
    max-height: none !important;
    overflow-y: visible !important;
    width: 100% !important;
    border: none !important;
}}

@media (max-width: 768px) {{
    .block-container {{ padding-left: 2px !important; padding-right: 2px !important; }}
    
    .div-scroll-local-historique {{
        height: 380px !important;
        max-height: 380px !important;
        overflow-y: auto !important;
        display: block !important;
        border: 1px solid #CBD5E1 !important;
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

.table-live tr td {{ background-color: #FEF9C3 !important; }}
.table-live tr:nth-child(even) td {{ background-color: #FEFCE8 !important; }}

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

/* 6. PIED DE PAGE TECHNIQUE UNIQUE (GESTION PC VS MOBILE) */
.signature-fin-page {{
    position: fixed !important;
    bottom: 0px !important;
    left: 0px !important;
    width: 100vw !important;
    height: 32px !important;
    background-color: #FFFFFF !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 12px !important;
    text-align: center !important;
    color: #1E3A8A !important;
    font-size: 0.92rem !important;
    font-weight: bold !important;
    border-top: 1px dashed #1E3A8A !important;
    z-index: 999999 !important;
    padding: 0px !important;
    margin: 0px !important;
}}

.logo-signature {{
    height: 20px !important;
    width: auto !important;
    vertical-align: middle !important;
}}

/* CORRECTION MOBILE RADICALE : PLUS DE BLOCAGE, PLUS DE RECOUVREMENT */
@media (max-width: 768px) {{
    .signature-fin-page {{ 
        position: relative !important;   /* Devient un élément fluide normal du document */
        bottom: auto !important;
        left: auto !important;
        width: 100% !important;
        height: 40px !important;         /* Légère hauteur propre */
        line-height: 40px !important;
        margin-top: 25px !important;     /* S'écarte proprement après le dernier tableau */
        margin-bottom: 10px !important;
        border-top: 1px solid #CBD5E1 !important;
        background-color: transparent !important;
        display: block !important;
        font-size: 0.82rem !important;
    }}
    .logo-signature {{ 
        display: none !important; 
    }}
}}

</style>
""", unsafe_allow_html=True)


# [Conservez le reste de votre fichier Streamlit strictement identique]

def gen_html(df, cl):
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
# --- LECTURE DU PARAMÈTRE DE COURSE DEPUIS L'URL ---
query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()

if choix_course_url == "c1asaf" and course1_disponible:
    choix_course = "Course 1 ASAF"
    module_actif = Course_1_ASAF
elif choix_course_url == "c1racb" and course1_racb_disponible:
    choix_course = "Course 1 RACB"
    module_actif = Course_1_RACB
elif choix_course_url == "c2asaf" and course2_disponible:
    choix_course = "Course 2 ASAF"
    module_actif = Course_2_ASAF
elif choix_course_url == "c2racb" and course2_racb_disponible:
    choix_course = "Course 2 RACB"
    module_actif = Course_2_RACB
elif choix_course_url == "c3asaf" and course3_disponible:
    choix_course = "Course 3 ASAF"
    module_actif = Course_3_ASAF
elif choix_course_url == "c3racb" and course3_racb_disponible:
    choix_course = "Course 3 RACB"
    module_actif = Course_3_RACB
else:
    choix_course = "Essais"
    module_actif = Essais

# --- EXTRACTION VISUELLE ET DYNAMIQUE DES HAUTEURS DEPUIS LE FICHIER ASSOCIE ---
hauteurs_config = getattr(module_actif, "HAUTEURS_TABLEAUX_PC", {})
h_historique = hauteurs_config.get("HISTORIQUE", "456px")
h_racb = hauteurs_config.get("RACB", "380px")
h_asaf_123 = hauteurs_config.get("ASAF_123", "380px")
h_asaf_4 = hauteurs_config.get("ASAF_4", "114px")

# Injection CSS unifiée (PC + Mobile) pour forcer le scroll sur l'ensemble des conteneurs
st.markdown(f"""
<style>
@media (min-width: 769px) {{
    .div-scroll-local-historique {{ height: {h_historique} !important; max-height: {h_historique} !important; overflow-y: auto !important; }}
}}
.div-scroll-local-div4 {{ height: {h_asaf_4} !important; max-height: {h_asaf_4} !important; overflow-y: auto !important; -webkit-overflow-scrolling: touch !important; }}
.ajust-hauteur-racb {{ height: {h_racb} !important; max-height: {h_racb} !important; overflow-y: auto !important; display: block !important; -webkit-overflow-scrolling: touch !important; }}
.ajust-hauteur-asaf123 {{ height: {h_asaf_123} !important; max-height: {h_asaf_123} !important; overflow-y: auto !important; display: block !important; -webkit-overflow-scrolling: touch !important; }}
</style>
""", unsafe_allow_html=True)

try:
    from concurrent.futures import ThreadPoolExecutor
    def recuperer_avec_timeout():
        return module_actif.recuperer_donnees_course()

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

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    if t_his: 
        st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    h_mob = "380px"
    
    # ==============================================================================
    # SÉCURITÉ ANTI-NAMEERROR : Valeur par défaut obligatoire pour h_pc
    # ==============================================================================
    if 'h_pc' not in locals() and 'h_pc' not in globals():
        h_pc = "380px"

    # Injection CSS dynamique (Votre bloc actuel)
    st.markdown(f"""
    <style>
      @media (min-width: 769px) {{ .ajust-hauteur-pc {{ max-height: {h_pc} !important; }} }}
      @media (max-width: 768px) {{ .ajust-hauteur-pc {{ max-height: {h_mob} !important; }} }}
    </style>
    """, unsafe_allow_html=True)


    if choix_course != "Essais":
        # --- MODE DE COURSE ---
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut_clean}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'>{gen_html(d_haut, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu_clean}</span>", unsafe_allow_html=True)
            # MODIFICATION ICI : On enlève la classe 'ajust-hauteur-pc' pour ce 2ème tableau (Division 4)
            # Cela permet au 3ème tableau de venir se coller directement en dessous sans trou blanc.
            st.markdown(f"<div style='height: auto; display: block;'>{gen_html(d_milieu, 'table-class-milieu')}</div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas_clean}</span>", unsafe_allow_html=True)
            nb_lignes = len(d_bas) if hasattr(d_bas, '__len__') else 0
            style_scroll = "class='ajust-hauteur-pc' style='overflow-y: auto; display: block;'" if nb_lignes > 10 else "style='height: auto; display: block;'"
            st.markdown(f"<div {style_scroll}>{gen_html(d_bas, 'table-class-robuste')}</div>", unsafe_allow_html=True)

    else:
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-racb'>{gen_html(d_bas, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='ajust-hauteur-asaf123'>{gen_html(d_haut, 'table-class-robuste')}</div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='div-scroll-local-div4'>{gen_html(d_milieu, 'table-class-robuste')}</div>", unsafe_allow_html=True)

# INJECTION DE LA SIGNATURE UNIQUE CONTRE LES DOUBLONS
st.markdown(f"""
<div class='signature-fin-page'>
    <img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>
    <span>www.timechrono.be</span>
</div>
""", unsafe_allow_html=True)

# GESTION DES SECONDES ET DU RAFRAÎCHISSEMENT DU LIVE
for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis / <span class='refresh-bleu-clair-historique'>Refresh {secondes_restantes} Sec.</span></span>", unsafe_allow_html=True)
    else:
        conteneur_titre_live.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    if secondes_restantes > 0:
        time.sleep(1)

st.rerun()
