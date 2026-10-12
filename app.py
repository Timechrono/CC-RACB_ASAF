# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
# https://dropbox.com
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
# ⚠️ METTEZ VOTRE LIEN DROPBOX ICI (Assurez-vous qu'il se termine bien par dl=1)
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
# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE UNIFIÉE AVEC RETOUR DU SCROLL DE PAGE ---
st.markdown(f"""
<style>
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
.titre-live, .titre-hist, .titre-classement {{
    color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
    padding: 4px 8px !important; border-radius: 3px !important;
    width: 100% !important; display: block !important; clear: both !important;
}}
.titre-live {{ background-color: #15803D !important; margin-top: 0px !important; margin-bottom: 6px !important; }}
.titre-hist {{ background-color: #475569 !important; margin-top: 15px !important; margin-bottom: 6px !important; }}
.titre-classement {{ background-color: #1E3A8A !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

.table-hist td:last-child {{ 
    font-weight: bold !important; 
    color: #0F172A !important; 
}}

.refresh-bleu-clair-historique {{
    color: #FFFFFF !important;
    font-weight: normal !important;
    background-color: #064E3B !important;
    border: 1px solid #00FF00 !important;
    padding: 1px 6px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-left: 4px !important;
}}

.espace-classement-suivant {{
    margin-top: 15px !important;
}}

/* BOÎTES DE SCROLL INTERNES CLOISONNÉES AUTONOMES */
.div-scroll-local-historique {{
    height: 480px !important;
    max-height: 480px !important;
    overflow-y: auto !important;
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
}}
.div-scroll-local-general {{
    height: 290px !important;
    max-height: 290px !important;
    overflow-y: auto !important;
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
}}
.div-scroll-local-classes {{
    height: 290px !important;
    max-height: 290px !important;
    overflow-y: auto !important;
    width: 100% !important;
    border: 1px solid #CBD5E1 !important;
}}

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
.table-live td:last-child, .table-class-robuste td:last-child {{ font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }}
.table-hist tr:nth-child(odd) td {{ background-color: #E0F2FE !important; }}

.signature-fin-page {{
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 12px !important;
    text-align: center !important;
    color: #1E3A8A !important;
    font-size: 0.92rem !important;
    font-weight: bold !important;
    padding-top: 6px !important;
    margin-top: 12px !important;
    border-top: 1px dashed #1E3A8A !important;
    width: 100% !important;
}}

.logo-signature {{
    height: 34px !important;
    width: auto !important;
    vertical-align: middle !important;
}}

@media (max-width: 768px) {{
    .div-scroll-local-historique, .div-scroll-local-general, .div-scroll-local-classes {{ max-height: none !important; height: auto !important; overflow-y: visible !important; border: none !important; }}
    .block-container {{ padding-left: 2px !important; padding-right: 2px !important; }}
    .titre-live, .titre-hist, .titre-classement {{ font-size: 0.85rem !important; padding: 3px 6px !important; }}
    .table-compacte th, .table-compacte td {{ font-size: 0.65rem !important; padding: 1px 2px !important; }}
    .table-hist td:nth-child(4) {{ max-width: 32px !important; overflow: hidden !important; text-overflow: clip !important; white-space: nowrap !important; }}
    .table-compacte td:nth-child(3), table td:nth-child(3) {{ max-width: 60px !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }}
    .table-live td:last-child, .table-class-robuste td:last-child {{ font-size: 0.70rem !important; }}
    .signature-fin-page {{ font-size: 0.75rem !important; padding-top: 4px !important; }}
    .logo-signature {{ height: 32px !important; }}
}}

.table-class-robuste tr.ligne-bleue-separation td {{ box-shadow: inset 0 -3px 0 0 #1E3A8A !important; }}
tr.ligne-separation-classe td, .table-compacte tr.ligne-separation-classe td {{ box-shadow: inset 0 -3px 0 0 #1E3A8A !important; }}
</style>
""", unsafe_allow_html=True)
def gen_html(df, cl):
    if cl == "table-hist":
        phrase_attente = "En attente d'arrivée..."
    elif cl in ["table-class-robuste", "table-class-groupes"]:
        phrase_attente = "En attente du premier classé RACB..." if "RACB" in choix_course.upper() else "En attente du premier classé ASAF..." if "ASAF" in choix_course.upper() else "En attente du premier classé..."
    else:
        phrase_attente = "En attente du départ..."

    # RECONNAISSANCE CHIRURGICALE POUR FORCER LE SCROLL SUR GROUPE / CLASSE SANS CONFLIT
    if cl == "table-class-groupes" or cl == "table-class-classes":
        cl = "table-class-groupes"

    if isinstance(df, str):
        if "<TABLE" in df.upper() and "</TABLE>" in df.upper():
            debut = df.upper().find("<TABLE")
            fin = df.upper().find("</TABLE>") + 8
            tableau_propre = df[debut:fin]
            
            if cl == "table-hist":
                return f"<div class='div-scroll-local-historique'>{tableau_propre}</div>"
            elif cl == "table-class-groupes":
                return f"<div class='div-scroll-local-classes'>{tableau_propre}</div>"
            else:
                # Si la chaîne contient les en-têtes du groupe/classe on force le routage vers sa boîte de scroll
                if "GROUPE" in tableau_propre.upper() and "CL" in tableau_propre.upper():
                    return f"<div class='div-scroll-local-classes'>{tableau_propre}</div>"
                return f"<div class='div-scroll-local-general'>{tableau_propre}</div>"
                
        return f"<div class='table-responsive-container'><table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table></div>"

    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<div class='table-responsive-container'><table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px; font-style: italic; color: #64748B;'>{phrase_attente}</td></tr></table></div>"
    
    html_table = df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)
    
    if cl == "table-hist":
        return f"<div class='div-scroll-local-historique'>{html_table}</div>"
    elif cl == "table-class-robuste":
        return f"<div class='div-scroll-local-general'>{html_table}</div>"
    elif cl == "table-class-groupes":
        return f"<div class='div-scroll-local-classes'>{html_table}</div>"
        
    return f"<div class='table-responsive-container'>{html_table}</div>"

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

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    if t_his: 
        st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    if choix_course != "Essais":
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_milieu, "table-class-groupes"), unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
    else:
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)

st.markdown(f"""
<div class='signature-fin-page'>
    <img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>
    www.timechrono.be
</div>
""", unsafe_allow_html=True)

for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis / <span class='refresh-bleu-clair-historique'>Refresh {secondes_restantes} Sec.</span></span>", unsafe_allow_html=True)
    else:
        conteneur_titre_live.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    if secondes_restantes > 0:
        time.sleep(1)

st.rerun()
