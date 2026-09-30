import pandas as pd
import datetime
import urllib.request
import streamlit as st

# --- RECONSTRUCTION INTERNE SÉCURISÉE SANS LIENS INTERNET ---
ID_ENG = st.secrets["db_ids"]["eng"]
KEY_ENG = st.secrets["db_keys"]["eng"]

ID_ARR = st.secrets["db_ids"]["arr"]
KEY_ARR = st.secrets["db_keys"]["arr"]

ID_DEP = st.secrets["db_ids"]["dep"]
KEY_DEP = st.secrets["db_keys"]["dep"]

FILE_ENGAGES = f"https://dropboxusercontent.com{ID_ENG}/LIVE_Liste_ENGAGES.xlsm?rlkey={KEY_ENG}&dl=1"
FILE_ARRIVEE = f"https://dropboxusercontent.com{ID_ARR}/LIVE_Temps_ARRIVEE.xlsm?rlkey={KEY_ARR}&dl=1"
FILE_DEPART  = f"https://dropboxusercontent.com{ID_DEP}/LIVE_Temps_DEPART.xlsm?rlkey={KEY_DEP}&dl=1"

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
        return "<span class='badge-piste'>&#128680; En Piste</span>" if est_dans_le_live else "No Time"
    return "<span class='badge-piste'>&#128680; En Piste</span>" if est_dans_le_live else "En Piste"

def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Départ", "Arrivée", "Chrono réalisé"]
    
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    # --- SUPPRESSION VOLONTAIRE DU TRY/EXCEPT POUR AFFICHER LA VÉRITABLE ERREUR ---
    entetes = {'User-Agent': 'Mozilla/5.0'}
    
    req_eng = urllib.request.Request(FILE_ENGAGES, headers=entetes)
    req_dep = urllib.request.Request(FILE_DEPART, headers=entetes)
    req_arr = urllib.request.Request(FILE_ARRIVEE, headers=entetes)

    with urllib.request.urlopen(req_eng) as url:
        df_eng_raw = pd.read_excel(url, engine='openpyxl')
    with urllib.request.urlopen(req_dep) as url:
        df_dep_raw = pd.read_excel(url, skiprows=2, engine='openpyxl')
    with urllib.request.urlopen(req_arr) as url:
        df_arr_raw = pd.read_excel(url, skiprows=2, engine='openpyxl')

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
            
            # 2. Historique
            df_hist_base = base_triee.copy()
            df_hist_base["Chrono réalisé"] = df_hist_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=False), axis=1)
            
            indices_top5 = df_hist_base.head(5).index
            for idx in indices_top5:
                if pd.isna(df_hist_base.loc[idx, "Heure_Arrivee"]):
                    df_hist_base.loc[idx, "Chrono réalisé"] = "En Piste"
                    
            df_hist = df_hist_base[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Départ", "Arrivée", "Chrono réalisé"]]
            
            # 3. Classements
            valides = base[base["Calc_Sec"].notna()].copy()
            if len(valides) > 0:
                scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()

                racb = scr[scr["N°"].astype(str).str.contains("N", na=False)].head(20).copy()
                if len(racb) > 0:
                    racb["Pos"] = range(1, len(racb) + 1)
                    racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                    df_racb = racb[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]

                asaf123 = scr[scr["Division"].isin(["1", "2", "3"])].head(25).copy()
                if len(asaf123) > 0:
                    asaf123["Pos"] = range(1, len(asaf123) + 1)
                    asaf123["Chrono"] = asaf123["Calc_Sec"].apply(format_final_chrono)
                    df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]

                asaf4 = scr[scr["Division"] == "4"].head(10).copy()
                if len(asaf4) > 0:
                    asaf4["Pos"] = range(1, len(asaf4) + 1)
                    asaf4["Chrono"] = asaf4["Calc_Sec"].apply(format_final_chrono)
                    df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]

    return df_live, df_hist, df_racb, df_asaf123, df_asaf4
