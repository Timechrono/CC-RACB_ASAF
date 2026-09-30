def gen_html(df, cl):
    if df.empty:
        return f"<table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)

# --- MENU DE SELECTION PURGE DES AUTRES COURSES ---
col_vide, col_texte, col_select = st.columns([0.6, 1.5, 1.3])
with col_texte:
    st.markdown('<p class="texte-menu" style="margin-top:28px;">Sélectionnez la session à afficher :</p>', unsafe_allow_html=True)
with col_select:
    choix_course = st.selectbox("Session_Label", ["Essais / Entraînements"], label_visibility="collapsed")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# --- AFFICHAGE EXCLUSIF DES ESSAIS ---
@st.fragment(run_every=30)
def afficher_tableaux():
    st.cache_data.clear()
    
    # Appel direct et unique au script Essais
    d_liv, d_his, d_as123, d_as4, d_racb = Essais.recuperer_donnees_course()
    titre_historique = "🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB"
    
    # Application de vos largeurs d'historique 6 colonnes d'essais
    st.markdown("<style>.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; } .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; } .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; } .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; } .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; } .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }</style>", unsafe_allow_html=True)

    cg, cd = st.columns([1.3, 0.9])
    with cg:
        st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
        st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<span class='titre-hist'>{titre_historique}</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    with cd:
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 20)</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_racb, "table-class-robuste"), unsafe_allow_html=True)
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL Division 123 (Top 25)</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_as123, "table-class-robuste"), unsafe_allow_html=True)
        st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL Division 4 (Top 10)</span>", unsafe_allow_html=True)
        st.markdown(gen_html(d_as4, "table-class-robuste"), unsafe_allow_html=True)

afficher_tableaux()

# --- FIN DU SCRIPT ---
