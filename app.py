# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
# Fichier : app.py - Partie 1

import streamlit as st
import pandas as pd
import time

# --- VOTRE VARIABLE GLOBALE DE LOGO INITIALE ---
LIEN_DROPBOX_LOGO = "https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1" 

query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()

if choix_course_url == "c1asaf" and course1_disponible: choix_course = "Course 1 ASAF"
elif choix_course_url == "c1racb" and course1_racb_disponible: choix_course = "Course 1 RACB"
elif choix_course_url == "c2asaf" and course2_disponible: choix_course = "Course 2 ASAF"
elif choix_course_url == "c2racb" and course2_racb_disponible: choix_course = "Course 2 RACB"
elif choix_course_url == "c3asaf" and course3_disponible: choix_course = "Course 3 ASAF"
elif choix_course_url == "c3racb" and course3_racb_disponible: choix_course = "Course 3 RACB"
else: choix_course = "Essais"

# SÉCURITÉ : Initialisation à blanc pour éviter les NameError si Dropbox ralentit au démarrage
d_liv, d_his, d_haut, d_milieu, d_bas = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
t_live, t_his, t_haut, t_milieu, t_bas = "", "", "", "", ""

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
        if res and len(res) == 10: d_liv, d_his, d_haut, d_milieu, d_bas, t_live, t_his, t_haut, t_milieu, t_bas = res
except Exception as e:
    t_live = "⚠️ Liaison Dropbox ralentie ou instable — Tentative de reconnexon en cours..."
# Fichier : app.py - Partie 2

st.markdown("<style>@media (min-width: 769px) { .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 8% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 32% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 28% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 5% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 17% !important; } }</style>", unsafe_allow_html=True)

if t_haut and "TOP 20" in t_haut.upper(): t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX RACB"

# --- FONCTION CHIRURGICALE POUR LIRE VOS HAUTEURS DEPUIS ESSAIS.PY ---
def extraire_titre_et_hauteur(texte_titre, hauteur_defaut="530px"):
    if not texte_titre: return "", hauteur_defaut
    if "##H=" in str(texte_titre):
        try:
            parties = str(texte_titre).split("##H=")
            return parties[0].strip(), parties[1].strip() + "px"
        except Exception: pass
    return str(texte_titre), hauteur_defaut

cg, cd = st.columns([1.3, 0.9])
with cg:
    conteneur_titre_live = st.empty()
    # EN DIRECT : Inchangé (sans scroll)
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    
    # HISTORIQUE : Hauteur lue dynamiquement
    t_his_p, h_his = extraire_titre_et_hauteur(t_his, "530px")
    if t_his_p: st.markdown(f"<span class='titre-hist'><span>{t_his_p}</span></span>", unsafe_allow_html=True)
    st.markdown(f'<div style="max-height: {h_his}; overflow-y: auto;">{gen_html(d_his, "table-hist")}</div>', unsafe_allow_html=True)
# Fichier : app.py - Partie 3

with cd:
    # --- ROUTAGE STRICT DU MODE DE COURSE VS MODE ESSAIS ---
    if choix_course != "Essais":
        t_haut_p, h_haut = extraire_titre_et_hauteur(t_haut, "530px")
        t_milieu_p, h_milieu = extraire_titre_et_hauteur(t_milieu, "530px")
        t_bas_p, h_bas = extraire_titre_et_hauteur(t_bas, "530px")

        if t_haut_p:
            st.markdown(f"<span class='titre-classement'><span>{t_haut_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_haut}; overflow-y: auto;">{gen_html(d_haut, "table-class-robuste")}</div>', unsafe_allow_html=True)
        if t_milieu_p:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'><span>{t_milieu_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_milieu}; overflow-y: auto;">{gen_html(d_milieu, "table-class-milieu")}</div>', unsafe_allow_html=True)
        if t_bas_p:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'><span>{t_bas_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_bas}; overflow-y: auto;">{gen_html(d_bas, "table-class-robuste")}</div>', unsafe_allow_html=True)
    else:
        # --- FORÇAGE INTELLIGENT PAR VÉRIFICATION DIRECTE DES TITRES ---
        elements_essais = [
            (t_haut, d_haut),
            (t_milieu, d_milieu),
            (t_bas, d_bas)
        ]
        
        bloc_racb = next(((t, d) for t, d in elements_essais if t and "RACB" in t.upper()), ("", pd.DataFrame()))
        bloc_div123 = next(((t, d) for t, d in elements_essais if t and "123" in t.upper()), ("", pd.DataFrame()))
        bloc_div4 = next(((t, d) for t, d in elements_essais if t and "4" in t.upper()), ("", pd.DataFrame()))
        
        t_r_p, h_r = extraire_titre_et_hauteur(bloc_racb[0], "530px")
        t_123_p, h_123 = extraire_titre_et_hauteur(bloc_div123[0], "530px")
        t_4_p, h_4 = extraire_titre_et_hauteur(bloc_div4[0], "530px")

        # 1. EN PREMIER : RACB
        if t_r_p:
            st.markdown(f"<span class='titre-classement'><span>{t_r_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_r}; overflow-y: auto;">{gen_html(bloc_racb[1], "table-class-robuste")}</div>', unsafe_allow_html=True)
        
        # 2. EN DEUXIÈME : Division 123
        if t_123_p:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'><span>{t_123_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_123}; overflow-y: auto;">{gen_html(bloc_div123[1], "table-class-robuste")}</div>', unsafe_allow_html=True)
        
        # 3. EN TROISIÈME : Division 4
        if t_4_p:
            st.markdown(f"<span class='titre-classement espace-classement-suivant'><span>{t_4_p}</span></span>", unsafe_allow_html=True)
            st.markdown(f'<div style="max-height: {h_4}; overflow-y: auto;">{gen_html(bloc_div4[1], "table-class-robuste")}</div>', unsafe_allow_html=True)

# Votre bas de page d'origine branché sur votre variable globale
st.markdown(f"<div class='signature-fin-page'><img src='{LIEN_DROPBOX_LOGO}' class='logo-signature'>www.timechrono.be</div>", unsafe_allow_html=True)

for secondes_restantes in range(30, -1, -1):
    if "Derniers concurrents" in t_live or "DIRECT" in t_live.upper():
        conteneur_titre_live.markdown(
            f"<span class='titre-live'>"
            f"<span>{t_live}</span>"
            f"<span class='refresh-bleu-clair-historique' style='padding: 2px 6px !important;'>Refresh {secondes_restantes} Sec.</span>"
            f"</span>", 
            unsafe_allow_html=True
        )
    else:
        conteneur_titre_live.markdown(f"<span class='titre-live'><span>{t_live}</span></span>", unsafe_allow_html=True)
        
    if secondes_restantes > 0:
        time.sleep(1)

st.rerun()
