# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1

import streamlit as st
import pandas as pd
import time
import requests
import io
import importlib
import Essais

# Initialisation globale stricte de toutes les variables de données et de détection
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

course1_disponible = False
course2_disponible = False
course3_disponible = False
course1_racb_disponible = False
course2_racb_disponible = False
course3_racb_disponible = False

# --- DÉTECTION SÉCURISÉE DES SCRIPTS DE COURSE DISPONIBLES ---
try:
    import Course_1_ASAF
    course1_disponible = True
except ModuleNotFoundError: pass

try:
    import Course_2_ASAF
    course2_disponible = True
except ModuleNotFoundError: pass

try:
    import Course_3_ASAF
    course3_disponible = True
except ModuleNotFoundError: pass

try:
    import Course_1_RACB
    course1_racb_disponible = True
except ModuleNotFoundError: pass

try:
    import Course_2_RACB
    course2_racb_disponible = True
except ModuleNotFoundError: pass

try:
    import Course_3_RACB
    course3_racb_disponible = True
except ModuleNotFoundError: pass

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE UNIFIÉE ---
st.markdown(f"""
<style>
/* 1. DISPARITION TOTALE DES COMPOSANTS STREAMLIT */
footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget,
[data-testid="stHeader"], [data-testid="stDecoration"], header {{
    display: none !important; visibility: hidden !important; height: 0px !important;
    max-height: 0px !important; min-height: 0px !important; margin: 0px !important;
    padding: 0px !important; overflow: hidden !important; opacity: 0 !important;
    line-height: 0 !important; font-size: 0 !important; position: absolute !important;
    top: -9999px !important; left: -9999px !important;
}}

button:focus, div:focus, input:focus, select:focus {{
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}}

/* 2. CONFIGURATION DE LA PAGE - NETTOYAGE DES ESPACES INUTILES */
@media (min-width: 769px) {{
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
        overflow: auto !important; overflow-y: auto !important; height: auto !important; max-height: none !important;
    }}
}}
@media (max-width: 768px) {{
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
        overflow: auto !important; overflow-y: auto !important; height: 100% !important;
    }}
}}

.block-container {{ padding-top: 0px !important; margin-top: 0px !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}
@media (min-width: 769px) {{ .block-container {{ padding-bottom: 5px !important; }} }}
@media (max-width: 768px) {{ .block-container {{ padding-bottom: 40px !important; }} }}

div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; padding-top: 0px !important; margin-top: 0px !important; }}
div.stElementContainer {{ margin-top: 0px !important; margin-bottom: 0px !important; padding-top: 0px !important; padding-bottom: 0px !important; }}

/* 3. BANDEAUX DE TITRES GRAPHIQUES */
.titre-live, .titre-hist, .titre-classement {{
    color: #FFFFFF !important; font-size: 1.02rem !important; font-weight: bold !important;
    height: 26px !important; max-height: 26px !important; padding: 0px 8px !important; border-radius: 3px !important;
    width: 100% !important; clear: both !important; display: flex !important;
    justify-content: space-between !important; align-items: center !important;
}}
.titre-live {{ background-color: #15803D !important; margin-top: 0px !important; margin-bottom: 6px !important; }}
.titre-hist {{ background-color: #475569 !important; margin-top: 15px !important; margin-bottom: 6px !important; }}
.titre-classement {{ background-color: #1E3A8A !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

.refresh-bleu-clair-historique {{
    color: #064E3B !important; background-color: #DCF2E8 !important; border: 1px solid #3B8F44 !important;
    font-weight: bold !important; font-size: 13px !important; padding: 1px 6px !important;
    line-height: 16px !important; border-radius: 4px !important; display: inline-block !important;
    margin-left: 4px !important; vertical-align: middle !important;
}}
.espace-classement-suivant {{ margin-top: 15px !important; }}

/* 4. BLOCS DE SCROLL INTERNES CLOISONNÉS */
.div-scroll-local-historique {{ width: 100% !important; border: 1px solid #CBD5E1 !important; }}
.div-scroll-local-general, .div-scroll-local-classes {{ height: auto !important; max-height: none !important; overflow-y: visible !important; width: 100% !important; border: none !important; }}

@media (min-width: 769px) {{
    .div-scroll-local-historique {{ height: 456px !important; max-height: 456px !important; overflow-y: auto !important; display: block !important; }}
    .div-scroll-local-div4 {{ height: 114px !important; max-height: 114px !important; overflow-y: auto !important; width: 100% !important; display: block !important; }}
}}
@media (max-width: 768px) {{
    .block-container {{ padding-left: 2px !important; padding-right: 2px !important; }}
    .div-scroll-local-historique {{ height: auto !important; max-height: none !important; overflow-y: visible !important; display: block !important; border: 1px solid #CBD5E1 !important; }}
    .div-scroll-local-div4 {{ height: auto !important; max-height: none !important; overflow-y: visible !important; display: block !important; }}
}}

/* 5. DESIGN COMPACT DES TABLEAUX */
.table-responsive-container {{ width: 100% !important; }}
.table-compacte {{ width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: auto !important; }}
.table-compacte tr {{ height: 18px !important; }}
.table-compacte th, .table-compacte td {{ height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; vertical-align: middle !important; white-space: nowrap !important; }}
.table-compacte td {{ border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }}
.table-compacte th {{ font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }}

.table-live td:last-child, .table-class-robuste td:last-child, .table-hist td:last-child {{ font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }}
.table-hist tr:nth-child(odd) td {{ background-color: #E0F2FE !important; }}

@media (max-width: 768px) {{
    .table-compacte th, .table-compacte td {{ font-size: 0.65rem !important; padding: 1px 2px !important; height: 25px !important; }}
    .table-hist td:nth-child(4) {{ max-width: 32px !important; overflow: hidden !important; text-overflow: clip !important; white-space: nowrap !important; }}
    .table-compacte td:nth-child(3), table td:nth-child(3) {{ max-width: 60px !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }}
    .table-live td:last-child, .table-class-robuste td:last-child {{ font-size: 0.70rem !important; }}
    .titre-live, .titre-hist, .titre-classement {{ height: auto !important; max-height: none !important; line-height: 1.3 !important; padding: 4px 8px !important; }}
}}

.table-class-robuste tr.ligne-bleue-separation td, tr.ligne-separation-classe td, .table-compacte tr.ligne-separation-classe td {{ box-shadow: inset 0 -3px 0 0 #1E3A8A !important; }}

/* 6. SIGNATURE DE FIN DE PAGE */
.signature-fin-page {{
    display: flex !important; justify-content: center !important; align-items: center !important; gap: 12px !important;
    text-align: center !important; color: #1E3A8A !important; font-size: 0.92rem !important; font-weight: bold !important;
    padding-top: 6px !important; margin-top: 45px !important; margin-bottom: 5px !important; border-top: 1px dashed #1E3A8A !important; width: 100% !important; clear: both !important;
}}
.logo-signature {{ height: 24px !important; width: auto !important; vertical-align: middle !important; }}
@media (max-width: 768px) {{
    .signature-fin-page {{ font-size: 0.75rem !important; padding-top: 4px !important; margin-bottom: 30px !important; }}
    .logo-signature {{ height: 32px !important; }}
}}
</style>
""", unsafe_allow_html=True)
def gen_html(df, cl):
    if cl == "table-hist":
        phrase_attente = "En attente d'arrivée..."
    elif cl in ["table-class-robuste", "table-class-groupes", "table-class-milieu"]:
        nom_course = choix_course.upper() if 'choix_course' in globals() else ""
        if "RACB" in nom_course: phrase_attente = "En attente du premier classé RACB..."
        elif "ASAF" in nom_course: phrase_attente = "En attente du premier classé ASAF..."
        else: phrase_attente = "En attente du premier classé..."
    else: phrase_attente = "En attente du départ..."

    style_conteneur = "class='div-scroll-local-historique'" if cl == "table-hist" else "class='table-responsive-container'"

    if isinstance(df, str):
        if "<TABLE" in df.upper() and "</TABLE>" in df.upper():
            debut = df.upper().find("<TABLE")
            fin = df.upper().find("</TABLE>") + 8
            return f"<div {style_conteneur}>{df[debut:fin]}</div>"
        return f"<div {style_conteneur}><table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table></div>"

    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<div {style_conteneur}><table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table></div>"
    
    return f"<div {style_conteneur}>{df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)}</div>"

# --- LECTURE DU PARAMÈTRE DE COURSE DEPUIS L'URL ---
query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()

if choix_course_url == "c1asaf" and course1_disponible: choix_course = "Course 1 ASAF"
elif choix_course_url == "c1racb" and course1_racb_disponible: choix_course = "Course 1 RACB"
elif choix_course_url == "c2asaf" and course2_disponible: choix_course = "Course 2 ASAF"
elif choix_course_url == "c2racb" and course2_racb_disponible: choix_course = "Course 2 RACB"
elif choix_course_url == "c3asaf" and course3_disponible: choix_course = "Course 3 ASAF"
elif choix_course_url == "c3racb" and course3_racb_disponible: choix_course = "Course 3 RACB"
else: choix_course = "Essais"

# Récupération dynamique et FORÇAGE de la relecture physique du module actif
module_actif = None
if choix_course == "Course 1 ASAF": 
    import Course_1_ASAF; module_actif = importlib.reload(Course_1_ASAF)
elif choix_course == "Course 1 RACB": 
    import Course_1_RACB; module_actif = importlib.reload(Course_1_RACB)
elif choix_course == "Course 2 ASAF": 
    import Course_2_ASAF; module_actif = importlib.reload(Course_2_ASAF)
elif choix_course == "Course 2 RACB": 
    import Course_2_RACB; module_actif = importlib.reload(Course_2_RACB)
elif choix_course == "Course 3 ASAF": 
    import Course_3_ASAF; module_actif = importlib.reload(Course_3_ASAF)
elif choix_course == "Course 3 RACB": 
    import Course_3_RACB; module_actif = importlib.reload(Course_3_RACB)
else: 
    import Essais; module_actif = importlib.reload(Essais)

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

if t_haut and "TOP 20" in t_haut.upper(): t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX RACB"

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    # --- CHARGEMENT DYNAMIQUE DES VARIABLES DE HAUTEUR SUR PC ---
    h_racb_pc, h_asaf123_pc, h_asaf4_pc = "215px", "215px", "114px"
    if module_actif and hasattr(module_actif, 'HAUTEURS_TABLEAUX_PC'):
        h_racb_pc = str(module_actif.HAUTEURS_TABLEAUX_PC.get("RACB", "215px"))
        h_asaf123_pc = str(module_actif.HAUTEURS_TABLEAUX_PC.get("ASAF_123", "215px"))
        h_asaf4_pc = str(module_actif.HAUTEURS_TABLEAUX_PC.get("ASAF_4", "114px"))

    st.markdown(f"""
    <style>
      @media (min-width: 769px) {{
        .div-pc-scroll-racb {{ max-height: {h_racb_pc} !important; height: {h_racb_pc} !important; overflow-y: auto !important; }}
        .div-pc-scroll-asaf123 {{ max-height: {h_asaf123_pc} !important; height: {h_asaf123_pc} !important; overflow-y: auto !important; }}
        .div-pc-scroll-asaf4 {{ max-height: {h_asaf4_pc} !important; height: {h_asaf4_pc} !important; overflow-y: auto !important; }}
      }}
    </style>
    """, unsafe_allow_html=True)

    if choix_course != "Essais":
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-racb" style="border: 1px solid #CBD5E1;">{gen_html(d_haut, "table-class-robuste")}</div>', unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-asaf123" style="border: 1px solid #CBD5E1;">{gen_html(d_milieu, "table-class-milieu")}</div>', unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-asaf4" style="border: 1px solid #CBD5E1;">{gen_html(d_bas, "table-class-robuste")}</div>', unsafe_allow_html=True)
    else:
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-racb" style="border: 1px solid #CBD5E1;">{gen_html(d_bas, "table-class-robuste")}</div>', unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-asaf123" style="border: 1px solid #CBD5E1;">{gen_html(d_haut, "table-class-robuste")}</div>', unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="div-pc-scroll-asaf4" style="border: 1px solid #CBD5E1;">{gen_html(d_milieu, "table-class-robuste")}</div>', unsafe_allow_html=True)

    st.markdown("""<style>@media (max-width: 768px) { .div-pc-scroll-racb, .div-pc-scroll-asaf123, .div-pc-scroll-asaf4 { max-height: none !important; height: auto !important; overflow-y: visible !important; border: none !important; } }</style>""", unsafe_allow_html=True)

st.markdown(f"<div class='signature-fin-page'><img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>www.timechrono.be</div>", unsafe_allow_html=True)

for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis / <span class='refresh-bleu-clair-historique'>Refresh {secondes_restantes} Sec.</span></span>", unsafe_allow_html=True)
    else: conteneur_titre_live.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    if secondes_restantes > 0: time.sleep(1)

st.rerun()
