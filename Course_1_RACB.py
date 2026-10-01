import streamlit as st
import pandas as pd
import datetime
import os
import requests
import io

# --- DESIGN SCIENTIFIQUE RIGIDE ET LARGEURS CONSERVÉES À L'IDENTIQUE ---
CSS_RACB = """
<style>
.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 8% !important; }   
.table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 30% !important; }  
.table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 26% !important; }  
.table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 11% !important; }   
.table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 8% !important; }   
.table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 17% !important; }  
</style>
"""

# --- CONFIGURATION DROPBOX ---
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_DEPART  = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&st=mcibn3xx&dl=1"
FILE_ENGAGES_RACB = f"https://{HOTE_PROT}/scl/fi/69zkwsb45bpiw3ys3kk4c/LIVE_Liste_ENGAGES_RACB.xlsm?rlkey=qpjrlmbxhcskifnabs84veqh8&st=0snuv3e7&dl=1"
def telecharger_excel(url):
    try:
        entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        reponse = requests.get(url, headers=entetes, timeout=12)
        reponse.raise_for_status()
        return io.BytesIO(reponse.content)
    except Exception: return None

def convertir_en_secondes(valeur):
    if pd.isna(valeur) or valeur is None: return None
    if isinstance(valeur, pd.Timedelta): return valeur.total_seconds()
    if isinstance(valeur, (datetime.time, datetime.datetime)):
        return (valeur.minute * 60) + valeur.second + (valeur.microsecond / 1000000)
    s = str(valeur).strip()
    if not s or s.lower() == "nan": return None
    if ":" in s:
        try:
            parts = s.split(":")
            return (int(parts[0]) * 60) + float(parts[1].replace(",", "."))
        except Exception: pass
    if s.endswith(".0"): s = s[:-2]
    s_clean = "".join([c for c in s if c.isdigit()])
    if not s_clean: return None
    num = int(s_clean)
    return ((num // 10000) * 60) + ((num // 100) % 100) + ((num % 100) / 100)

def nettoyer_numero(valeur):
    if pd.isna(valeur): return "nan"
    s = str(valeur).strip().upper()
    return s[:-2] if s.endswith(".0") else s

def format_final_chrono(total_sec, fallback_statut="No Time"):
    if total_sec is None or pd.isna(total_sec) or total_sec < 0: return fallback_statut
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
    if "Calc_Sec" in row and pd.notna(row["Calc_Sec"]) and row["Calc_Sec"] > 0:
        return format_final_chrono(row["Calc_Sec"])
    if "Heure_Depart" in row and pd.notna(row["Heure_Depart"]) and pd.isna(row.get("Heure_Arrivee")):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"
def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    data_engages = telecharger_excel(FILE_ENGAGES_RACB)
    data_depart = telecharger_excel(FILE_DEPART)
    data_arrivee = telecharger_excel(FILE_ARRIVEE)

    if data_engages and data_depart and data_arrivee:
        try:
            df_eng_raw = pd.read_excel(data_engages, skiprows=1, engine='openpyxl')
            df_dep_raw = pd.read_excel(data_depart, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(data_arrivee, header=None, engine='openpyxl')

            idx_dep_1, idx_arr_1 = None, None
            for c_idx in range(len(df_dep_raw.columns)):
                if "COURSE 1 RACB" in str(df_dep_raw.iloc[1, c_idx]).strip().upper(): idx_dep_1 = c_idx
            for c_idx in range(len(df_arr_raw.columns)):
                if "COURSE 1 RACB" in str(df_arr_raw.iloc[1, c_idx]).strip().upper(): idx_arr_1 = c_idx

            chrono_excel_1 = df_arr_raw.iloc[2:, idx_arr_1 + 3] if idx_arr_1 is not None else None
            df_dep = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_1].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_1 + 1]}) if idx_dep_1 is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
            df_arr = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_1].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_1 + 2], "Chrono_Excel": chrono_excel_1}) if idx_arr_1 is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])

            df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
            df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                                   "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                                   "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                                   "Groupe": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                                   "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])

            df_dep = df_dep[(df_dep["N°"] != "NAN") & (df_dep["N°"] != "")]
            for d in [df_dep, df_arr]:
                if len(d) > 0:
                    d["N°"] = d["N°"].astype(str)
                    d["Run_Index"] = d.groupby("N°").cumcount() + 1

            df_dep["Sec_Dep"] = df_dep["Heure_Depart"].apply(convertir_en_secondes)
            df_arr["Sec_Arr"] = df_arr["Heure_Arrivee"].apply(convertir_en_secondes)
            df_arr["Sec_Excel"] = df_arr["Chrono_Excel"].apply(convertir_en_secondes)

            base_runs = df_dep[["N°", "Run_Index"]].copy() if len(df_dep) > 0 else df_eng[["N°"]].copy()
            if "Run_Index" not in base_runs.columns: base_runs["Run_Index"] = 1
            base_runs = base_runs.drop_duplicates(subset=["N°", "Run_Index"])

            base = pd.merge(base_runs, df_eng, on="N°", how="inner")
            base = pd.merge(base, df_dep, on=["N°", "Run_Index"], how="left")
            base = pd.merge(base, df_arr, on=["N°", "Run_Index"], how="left")

            if len(base) > 0:
                base["Calc_Sec"] = base["Sec_Excel"].fillna((base["Sec_Arr"] - base["Sec_Dep"]).apply(lambda x: x + 3600 if (x is not None and x < 0) else x))
                base["Départ_C1"] = base["Heure_Depart"].apply(formater_heure_ecran)

                if "Heure_Depart" in base.columns and base["Heure_Depart"].notna().any():
                    base_c1 = base[base["Heure_Depart"].notna()].copy()
                    base_c1["Ordre_Live"] = range(len(base_c1))
                    df_live_base = base_c1.sort_values(by="Ordre_Live", ascending=False).head(5).copy()
                    df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                    df_live_base["Arrivée_Brute"] = df_live_base["Heure_Arrivee"].apply(formater_heure_ecran)
                    df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_C1", "Arrivée_Brute", "Chrono réalisé"]].rename(columns={"Départ_C1": "Départ", "Arrivée_Brute": "Arrivée"})

                def formater_chrono_historique_course1(row):
                    if pd.notna(row["Heure_Depart"]) and pd.isna(row["Heure_Arrivee"]) and pd.isna(row["Sec_Excel"]): return "En Piste"
                    return format_final_chrono(row["Calc_Sec"]) if pd.notna(row["Calc_Sec"]) and row["Calc_Sec"] > 0 else "No Time"

                base["Chrono_C1_Visual_Hist"] = base.apply(formater_chrono_historique_course1, axis=1)
                df_hist_base = base.copy()
                
                # RE-INJECTION DU STYLE DE LARGEUR SPÉCIFIQUE RACB
                html_hist = CSS_RACB + "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Groupe</th><th>Classe</th><th>Chrono réalisé</th></tr></thead><tbody>"
                for idx, row in df_hist_base.iterrows():
                    html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Groupe']}</td><td>{row['Classe']}</td><td>{row['Chrono_C1_Visual_Hist']}</td></tr>"
                html_hist += "</tbody></table>"

                valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
                if len(valides) > 0:
                    scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                    scr = scr[~scr["Groupe"].astype(str).str.strip().str.startswith(('1', '2', '3', '4'), na=False)]
                    racb = scr.head(30).copy()
                    if len(racb) > 0:
                        racb["Pos"] = range(1, len(racb) + 1)
                        racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                        df_racb = racb[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
        except Exception: pass

    # TRANSMISSION PARFAITE DU CONTENU À L'APP SANS FAIRE DE DOUBLON
    # Structure : df_live, df_hist (ici HTML), df_haut, df_milieu, df_bas, Titre1, Titre2, Titre3, Titre4, Titre5
    return df_live, html_hist, df_racb, pd.DataFrame(), pd.DataFrame(), "🏎️ EN DIRECT / Derniers concurrents partis", "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents RACB", "🏆 CLASSEMENT GENERAL OFFICIEUX RACB (Top 30)", "", ""
