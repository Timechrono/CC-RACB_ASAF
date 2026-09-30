try:
    import Course_1_ASAF
    import Course_1_RACB
    import Course_2_ASAF  # NAVETTE AJOUTÉE ICI
except Exception:
    pass
    if choix_course == "Course 1 ASAF":
        d_liv, d_his, d_as123, d_as4, d_div = Course_1_ASAF.recuperer_donnees_course()
        d_racb = pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents ASAF"
    elif choix_course == "Course 1 RACB":
        d_liv, d_his, d_racb, d_div = Course_1_RACB.recuperer_donnees_course()
        d_as123, d_as4 = pd.DataFrame(), pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents RACB"
    elif choix_course == "Course 2 ASAF":
        d_liv, d_his, d_as123, d_as4, d_div = Course_2_ASAF.recuperer_donnees_course()
        d_racb = pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS / 2ème COURSE / Concurrents ASAF"
    else:
        d_liv, d_his, d_as123, d_as4, _ = Essais.recuperer_donnees_course()
        d_div, d_racb = pd.DataFrame(), pd.DataFrame()
        titre_historique = "🕒 HISTORIQUE DES TEMPS"
        if choix_course in ["Course 1 ASAF", "Course 2 ASAF"]:
            st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-classement'>📊 CLASSEMENT OFFICIEUX PAR Division / Classe (Top 3)</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_div, "table-class-robuste"), unsafe_allow_html=True)
