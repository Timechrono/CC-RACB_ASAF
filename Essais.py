import streamlit as st
import pandas as pd
import datetime
import os
import time

st.set_page_config(layout="wide")
st.cache_data.clear()

# --- DESIGN SCIENTIFIQUE RIGIDE : CONFIGURATION DU STYLE ET DES MARGES ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    .vrai-gyrophare {
        display: inline-block;
        margin-right: 6px;
        font-size: 1.05rem !important;
        vertical-align: middle !important;
    }
    
    .titre-live, .titre-hist, .titre-classement {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: bold !important;
        padding: 4px 8px !important;
        border-radius: 3px !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        display: block !important;
        clear: both !important;
    }
    
    .titre-live { background-color: #15803D !important; margin-top: 0px !important; }
    .titre-hist { background-color: #475569 !important; margin-top: 10px !important; }
    .titre-classement { background-color: #1E3A8A !important; margin-top: 0px !important; }
    
    .table-compacte { width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: fixed !important; }
    .table-compacte tr { height: 18px !important; }
    .table-compacte th, .table-compacte td { 
        height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; 
        vertical-align: middle !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; 
    }
    .table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
    .table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
    
    /* STYLE DES CELLULES DE CHRONO */
    .table-live td:last-child, .table-hist td:last-child, .table-class-robuste td:last-child {
        font-weight: bold !important;
        font-size: 0.94rem !important;
        color: #0F172A !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    
    /* STYLE DE NOTRE BADGE ALERTE EN PISTE */
    .badge-piste {
        background-color: #FEE2E2 !important;
        color: #DC2626 !important;
        padding: 1px 4px !important;
        border-radius: 3px !important;
        font-weight: bold !important;
        display: inline-block !important;
    }
    
    /* ALTERNANCE DE COULEUR APPLIQUÉE UNIQUEMENT À L'HISTORIQUE (RETIRÉE DU LIVE) */
    .table-hist tr:nth-child(odd) td {
        background-color: #E0F2FE !important;
    }
    
    /* GAUCHE : 1. Tableau En Direct */
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 25% !important; }
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 17% !important; }
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 12% !important; }
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 25% !important; }

    /* GAUCHE : 2. Tableau Historique */
    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 7% !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 7% !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 10% !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 10% !important; }  
    .table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 14% !important; }  

    /* DROITE : 3. Tableaux de Classements */
    .table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
    .table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
    .table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
    .table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
    .table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
    .table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

    .block-container { padding-top: 0.3rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    hr { margin: 6px 0px !important; border: 0 !important; height: 0 !important; }
    </style>
""", unsafe_allow_html=True)

FILE_DEPART = "https://dropbox.com"
FILE_ARRIVEE = "https://dropbox.com"
FILE_ENGAGES = "https://dropbox.com"
def convertir_en_secondes(valeur):
    if pd.isna(valeur) or valeur is None: return None
    if isinstance(valeur, (datetime.time, datetime.datetime)):
        return (valeur.minute * 60) + valeur.second + (valeur.microsecond / 1000000)
    s = str(valeur).strip()
    if s.endswith(".0"): s = s[:-2]
    s_clean = "".join([c for c in s if c.isdigit()])
    if not s_clean: return None
    num = int(s_clean)
    centiemes = num % 100
    secondes = (num // 100) % 100
    minutes = num // 10000
    if minutes >= 60: minutes = minutes % 60
    return (minutes * 60) + secondes + (centiemes / 100)

def nettoyer_numero(valeur):
    if pd.isna(valeur): return "nan"
    s = str(valeur).strip().upper()
    return s[:-2] if s.endswith(".0") else s

def format_final_chrono(total_sec):
    if total_sec is None or pd.isna(total_sec) or total_sec < 0: return "En Piste"
    m, reste_sec = divmod(round(total_sec, 2), 60)
    s = int(reste_sec // 1)
    c = int(round((reste_sec % 1) * 100))
    if c == 100: s += 1; c = 0
    if s == 60: m += 1; s = 0
    return f"{int(m):02d}:{s:02d}.{c:02d}"

def formater_heure_ecran(val):
    if pd.isna(val) or val == "" or str(val).lower() == "nan": return "-"
    s = str(val).strip()
    if s.endswith(".0"): s = s[:-2]
    s = s.zfill(6)
    return f"{s[0:2]}:{s[2:4]}.{s[4:6]}" if len(s) == 6 else str(val)

def calculer_statut_chrono(row, est_dans_le_live=True):
    if pd.notna(row["Calc_Sec"]):
        return format_final_chrono(row["Calc_Sec"])
    
    if pd.notna(row["Heure_Depart"]) and pd.isna(row["Heure_Arrivee"]):
        if est_dans_le_live:
            return "<span class='badge-piste'>&#128680; En Piste</span>"
        else:
            return "No Time"
        
    return "<span class='badge-piste'>&#128680; En Piste</span>" if est_dans_le_live else "En Piste"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Départ", "Arrivée", "Chrono réalisé"]
affichage_dynamique = st.empty()
while True:
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    fichiers_prets = os.path.exists(FILE_ENGAGES) and os.path.exists(FILE_DEPART) and os.path.exists(FILE_ARRIVEE)

    if fichiers_prets and os.path.getsize(FILE_ENGAGES) > 0 and os.path.getsize(FILE_DEPART) > 0 and os.path.getsize(FILE_ARRIVEE) > 0:
        try:
            # CORRECTION APPLIQUÉE : Suppression du skiprows=1 pour ne plus rater la ligne 2 de votre fichier d'origine
            df_eng_raw = pd.read_excel(FILE_ENGAGES, engine='openpyxl')
            df_dep_raw = pd.read_excel(FILE_DEPART, skiprows=2, engine='openpyxl')
            df_arr_raw = pd.read_excel(FILE_ARRIVEE, skiprows=2, engine='openpyxl')

            df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
            df_dep_raw.columns = df_dep_raw.columns.astype(str).str.strip().str.upper()
            df_arr_raw.columns = df_arr_raw.columns.astype(str).str.strip().str.upper()

            df_eng = pd.DataFrame()
            df_eng["N°"] = df_eng_raw.iloc[:, 0].apply(nettoyer_numero)
            df_eng["Nom_Prenom"] = df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip()
            df_eng["Voiture"] = df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip()
            
            def ext_div(x):
                if pd.isna(x): return "-"
                s = str(x).strip()
                return s[:-2] if s.endswith(".0") else s
                
            df_eng["Division"] = df_eng_raw.iloc[:, 5].apply(ext_div)
            df_eng["Classe"] = df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)

            df_dep = df_dep_raw.iloc[:, 0:2].copy()
            df_dep.columns = ["N°", "Heure_Depart"]
            df_dep["N°"] = df_dep["N°"].apply(nettoyer_numero)

            df_arr = df_arr_raw.iloc[:, 0:3].copy()
            df_arr.columns = ["N°", "Poubelle", "Heure_Arrivee"]
            df_arr["N°"] = df_arr["N°"].apply(nettoyer_numero)

            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
            df_dep = df_dep[df_dep["N°"] != "NAN"].copy()
            df_arr = df_arr[df_arr["N°"] != "NAN"].copy()
        except Exception as e:
            pass
        try:
            if len(df_dep) > 0:
                df_dep["Ordre_Saisie"] = range(len(df_dep))
                df_dep["Run_Index"] = df_dep.groupby("N°").cumcount() + 1
                df_arr["Run_Index"] = df_arr.groupby("N°").cumcount() + 1

                df_dep["Sec_Dep"] = df_dep["Heure_Depart"].apply(convertir_en_secondes)
                df_arr["Sec_Arr"] = df_arr["Heure_Arrivee"].apply(convertir_en_secondes)

                fusion = pd.merge(df_dep, df_arr, on=["N°", "Run_Index"], how="left")
                base = pd.merge(fusion, df_eng, on="N°", how="left")

                base["Nom_Prenom"] = base["Nom_Prenom"].fillna("Pilote Inconnu")
                base["Voiture"] = base["Voiture"].fillna("")
                base["Division"] = base["Division"].fillna("-")
                base["Classe"] = base["Classe"].fillna("-")

                if len(base) > 0:
                    base["Calc_Sec"] = base["Sec_Arr"] - base["Sec_Dep"]
                    base["Calc_Sec"] = base["Calc_Sec"].apply(lambda x: x + 3600 if (x is not None and x < 0) else x)
                    base["Départ"] = base["Heure_Depart"].apply(formater_heure_ecran)
                    base["Arrivée"] = base["Heure_Arrivee"].apply(formater_heure_ecran)
                    
                    base_triee = base.sort_values(by="Ordre_Saisie", ascending=False).copy()
                    
                    # 1. En Direct
                    df_live_base = base_triee.head(5).copy()
                    df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                    df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]
                    
                    # 2. Historique complet
                    df_hist_base = base_triee.copy()
                    df_hist_base["Chrono réalisé"] = df_hist_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=False), axis=1)
                    
                    indices_top5 = df_hist_base.head(5).index
                    for idx in indices_top5:
                        if pd.isna(df_hist_base.loc[idx, "Heure_Arrivee"]):
                            df_hist_base.loc[idx, "Chrono réalisé"] = "En Piste"
                            
                    df_hist = df_hist_base[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Départ", "Arrivée", "Chrono réalisé"]]
                    
                    # 3. Classements Scratch
                    valides = base[base["Calc_Sec"].notna()].copy()
                    
                    if len(valides) > 0:
                        scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()

                        # PASSAGE AU TOP 20 RACB SUR VOTRE LOGIQUE DE "N"
                        racb = scr[scr["N°"].astype(str).str.contains("N", na=False)].head(20).copy()
                        if len(racb) > 0:
                            racb["Pos"] = range(1, len(racb) + 1)
                            racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                            df_racb = racb[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]

                        # PASSAGE AU TOP 25 ASAF 1-2-3
                        asaf123 = scr[scr["Division"].isin(["1", "2", "3"])].head(25).copy()
                        if len(asaf123) > 0:
                            asaf123["Pos"] = range(1, len(asaf123) + 1)
                            asaf123["Chrono"] = asaf123["Calc_Sec"].apply(format_final_chrono)
                            df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]

                        # TOP 10 ASAF 4
                        asaf4 = scr[scr["Division"] == "4"].head(10).copy()
                        if len(asaf4) > 0:
                            asaf4["Pos"] = range(1, len(asaf4) + 1)
                            asaf4["Chrono"] = asaf4["Calc_Sec"].apply(format_final_chrono)
                            df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
        except Exception as e:
            pass

    with affichage_dynamique.container():
        if not fichiers_prets:
            st.warning("⚠️ En attente des fichiers Excel sur Dropbox...")
        else:
            cg, cd = st.columns([1.3, 0.9])
            with cg:
                st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_live, "table-live"), unsafe_allow_html=True)
                
                st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-hist'>🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_hist, "table-hist"), unsafe_allow_html=True)
            with cd:
                st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 20)</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_racb, "table-class-robuste"), unsafe_allow_html=True)
                
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLTIF DES ESSAIS ASAF DIV 1-2-3 (Top 25)</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_asaf123, "table-class-robuste"), unsafe_allow_html=True)
                
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLTIF DES ESSAIS ASAF DIV 4 (Top 10)</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_asaf4, "table-class-robuste"), unsafe_allow_html=True)
    time.sleep(1)
