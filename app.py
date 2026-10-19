# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
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
st.markdown("""
<style>
footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget, [data-testid="stHeader"], [data-testid="stDecoration"] {
    display: none !important; visibility: hidden !important; height: 0px !important; margin: 0px !important; padding: 0px !important; overflow: hidden !important; opacity: 0 !important;
}
@media (min-width: 769px) {
    footer, [data-testid="stFooterContainer"], [data-testid="stStatusWidget"], .stStatusWidget {
        position: fixed !important; bottom: -500px !important; transform: translateY(500px) !important;
    }
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    overflow: auto !important; height: auto !important; max-height: none !important;
}
.block-container { padding-top: 5px !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
.titre-live, .titre-hist, .titre-classement {
    color: #FFFFFF !important; font-size: 1.02rem !important; font-weight: bold !important; height: 26px !important; padding: 0px 8px !important; display: flex !important; justify-content: space-between !important; align-items: center !important;
}
.titre-live { background-color: #15803D !important; margin-bottom: 6px !important; }
.titre-hist { background-color: #475569 !important; margin-top: 15px !important; margin-bottom: 6px !important; }
.titre-classement { background-color: #1E3A8A !important; margin-bottom: 6px !important; }
.table-compacte { width: 100% !important; border-collapse: collapse !important; }
.table-compacte th, .table-compacte td { height: 18px !important; padding: 1px 5px !important; font-size: 0.85rem !important; }
.signature-fin-page {
    display: flex !important; justify-content: center !important; align-items: center !important; gap: 12px !important; color: #1E3A8A !important; font-size: 0.92rem !important; font-weight: bold !important; margin-top: 25px !important; border-top: 1px dashed #1E3A8A !important; width: 100% !important;
}
.logo-signature { height: 24px !important; width: auto !important; }
</style>
""", unsafe_allow_html=True)

def gen_html(df, cl):
    phrase_attente = "En attente d'arrivée..." if cl == "table-hist" else "En attente du départ..."
    style_conteneur = "class='div-scroll-local-historique'" if cl == "table-hist" else "class='table-responsive-container'"
    if isinstance(df, str) and "<TABLE" in df.upper():
        debut, fin = df.upper().find("<TABLE"), df.upper().find("</TABLE>") + 8
        return f"<div {style_conteneur}>{df[debut:fin]}</div>"
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        return f"<div {style_conteneur}><table class='table-compacte {cl}'><tr><td style='text-align: center; color: #64748B;'>{phrase_attente}</td></tr></table></div>"
    return f"<div {style_conteneur}>{df.to_html(index=False, classes=f'table-compacte {cl}', escape=False, border=0)}</div>"
query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()
choix_course = "Essais"
# Logique de routage et récupération des données...

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)

with cd:
    if t_haut:
        st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='overflow-y: auto; display: block;'>{gen_html(d_haut, 'table-class-robuste')}</div>", unsafe_allow_html=True)
    if t_milieu:
        st.markdown(f"<div class='espace-classement-suivant'><span class='titre-classement'>{t_milieu}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='overflow-y: auto; display: block;'>{gen_html(d_milieu, 'table-class-milieu')}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='signature-fin-page'>
    <img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>
    www.timechrono.be
</div>
""", unsafe_allow_html=True)

for secondes_restantes in range(30, -1, -1):
    conteneur_titre_live.markdown(f"<span class='titre-live'>🏎️ EN DIRECT / Rafraîchissement {secondes_restantes} Sec.</span>", unsafe_allow_html=True)
    if secondes_restantes > 0: time.sleep(1)

st.rerun()
