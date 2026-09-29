import streamlit as st

st.set_page_config(layout="wide")

# Barre de sélection pour les internautes avec vos 7 configurations
choix_course = st.selectbox(
    "Sélectionnez le live à afficher :",
    [
        "Essais / Entraînements", 
        "Course 1 ASAF", 
        "Course 1 RACB", 
        "Course 2 ASAF",
        "Course 2 RACB",
        "Course 3 ASAF",
        "Course 3 RACB"
    ]
)

# Chargement automatique de vos fichiers exacts
if choix_course == "Essais / Entraînements":
    import Essais
elif choix_course == "Course 1 ASAF":
    import Course_1_ASAF
elif choix_course == "Course 1 RACB":
    import Course_1_RACB
elif choix_course == "Course 2 ASAF":
    import Course_2_ASAF
elif choix_course == "Course 2 RACB":
    import Course_2_RACB
elif choix_course == "Course 3 ASAF":
    import Course_3_ASAF
elif choix_course == "Course 3 RACB":
    import Course_3_RACB
