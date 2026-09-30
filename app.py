CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 20)# --- DESIGN COMPACT DU SÉLECTEUR ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    button:focus, div:focus, input:focus, select:focus {
        outline: none !important; border-color: transparent !important; box-shadow: none !important;
    }
    .texte-menu {
        font-size: 0.95rem !important; font-weight: bold !important;
        color: #1E293B !important; text-align: right; padding-right: 15px;
    }
    .block-container { padding-top: 0.4rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- MENUS DE SÉLECTION EN HAUT ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements", "Course 1 ASAF", "Course 1 RACB", "Course 2 ASAF", "Course 2 RACB", "Course 3 ASAF", "Course 3 RACB"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- LOGIQUE D'AIGUILLAGE CENTRALE : LE CONTROLE REPASSE AUX FICHIERS ---
if choix_course == "Course 1 ASAF":
    try: Course_1_ASAF.afficher_ecran_complet()
    except Exception: st.error("Fichier Course 1 ASAF en cours de configuration")
elif choix_course == "Course 1 RACB":
    pass
elif choix_course == "Course 2 ASAF":
    pass
else:
    # Appel de la fonction autonome complète que vous venez de coller dans Essais.py
    Essais.afficher_ecran_complet()
