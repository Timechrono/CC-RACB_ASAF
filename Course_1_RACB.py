import streamlit as st
import pandas as pd
import requests
import io

def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0'}
    reponse = requests.get(url, headers=entetes, timeout=10)
    return io.BytesIO(reponse.content)

st.title("🔧 Moteur de Diagnostic TimeChrono")

# Liens absolus de vos fichiers
HOTE_PROT = "://dropboxusercontent.com"
FILE_DEPART = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&dl=1"
FILE_ENGAGES_ASAF = f"https://{HOTE_PROT}/scl/fi/wyof20d4bg4lbmnv0c7m5/LIVE_Liste_ENGAGES_ASAF.xlsm?rlkey=8q59lu88046nxu8mr8gs5ufvc&dl=1"

st.subheader("1. Vérification du fichier des Départs")
try:
    df_dep = pd.read_excel(telecharger_excel(FILE_DEPART), header=None, engine='openpyxl')
    st.success(f"Fichier Départ lu avec succès ! Nombre de lignes : {len(df_dep)}")
    st.write("Voici les 10 premières lignes détectées :")
    st.dataframe(df_dep.head(10))
except Exception as e:
    st.error(f"Erreur lors de la lecture du fichier Départ : {e}")

st.subheader("2. Vérification du fichier des Engagés ASAF")
try:
    df_asaf = pd.read_excel(telecharger_excel(FILE_ENGAGES_ASAF), engine='openpyxl')
    st.success(f"Fichier Engagés ASAF lu avec succès ! Nombre de lignes : {len(df_asaf)}")
    st.write("Voici les colonnes trouvées dans votre fichier ASAF :")
    st.write(list(df_asaf.columns))
    st.write("Voici les 5 premiers engagés ASAF détectés :")
    st.dataframe(df_asaf.head(5))
except Exception as e:
    st.error(f"Erreur lors de la lecture du fichier Engagés ASAF : {e}")
