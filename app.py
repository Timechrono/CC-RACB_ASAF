cg, cd = st.columns([1.3, 0.9])
with cg:
    st.markdown(f"<span class='titre-live'>{t_live}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_liv, "table-live"), unsafe_allow_html=True)
    
    # Espace d'origine de 35px entre Direct et Historique
    st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)
    
    if t_his: st.markdown(f"<span class='titre-hist'>{t_his}</span>", unsafe_allow_html=True)
    st.markdown(gen_html(d_his, "table-hist"), unsafe_allow_html=True)
    
with cd:
    if choix_course != "Essais":
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
            
            # CORRECTION : Passage de 20px à 35px pour s'aligner parfaitement sur la gauche
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
    else:
        if t_haut:
            st.markdown(f"<span class='titre-classement'>{t_haut}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_bas, "table-class-robuste"), unsafe_allow_html=True)
            
            # CORRECTION IDENTIQUE POUR LE MODE ESSAIS
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        if t_milieu:
            st.markdown(f"<span class='titre-classement'>{t_milieu}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_haut, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        if t_bas:
            st.markdown(f"<span class='titre-classement'>{t_bas}</span>", unsafe_allow_html=True)
            st.markdown(gen_html(d_milieu, "table-class-robuste"), unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# --- SYSTÈME DE RAFRAÎCHISSEMENT NATIF (TOUTES LES 30 SECONDES) ---
@st.fragment
def declencher_compteur_auto():
    time.sleep(30)
    st.rerun()

declencher_compteur_auto()
