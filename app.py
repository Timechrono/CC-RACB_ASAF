# --- EXÉCUTION RÉACTIVE PROPRE ET AUTONOME ---
if choix_course == "Course 1 ASAF":
    Course_1_ASAF.executer_affichage_c1_asaf()
elif choix_course == "Course 1 RACB":
    Course_1_RACB.executer_affichage_c1_racb()
elif choix_course == "Course 2 ASAF":
    Course_2_ASAF.executer_affichage_c2_asaf()
else:
    # Lancement direct du bloc d'affichage autonome d'Essais
    Essais.executer_affichage_essais()
