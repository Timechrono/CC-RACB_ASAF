import streamlit as st
import pandas as pd
import datetime
import os
import requests
import io

# --- DESIGN SCIENTIFIQUE RIGIDE ET LARGEURS AUTOMATIQUEMENT ADAPTATIVES SUR MOBILE ---
CSS_RACB = """
<style>
/* VRAI GYROPHARE DE COURSE STATIQUE (SANS CLIGNOTEMENT) */
.vrai-gyrophare {
    display: inline-block;
    margin-right: 6px;
    font-size: 1.05rem !important;
    vertical-align: middle !important;
}

.table-compacte { width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: fixed !important; }
.table-compacte tr { height: 18px !important; }
.table-compacte th, .table-compacte td { 
    height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; 
    vertical-align: middle !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; 
}
.table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
.table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }

.ligne-separation-classe td {
    border-bottom: 2px solid #1E3A8A !important;
}

.table-hist td:last-child, .table-live td:last-child, .table-class-robuste td:last-child {
    font-weight: bold !important;
    font-size: 0.94rem !important;
    color: #0F172A !important;
}

/* COLORIAGE BLEU UNE LIGNE SUR DEUX HISTORIQUE */
.table-hist tr:nth-child(odd) td {
    background-color: #E0F2FE !important;
}

/* ORDINATEUR : Configuration stricte des largeurs */
@media (min-width: 769px) {
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }

    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 8% !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 30% !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 26% !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 11% !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 8% !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 17% !important; }  

    .table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
    .table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
    .table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
    .table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
    .table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
    .table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }
}

/* SMARTPHONE (REMÈDE DÉFINITIF) : On déverrouille le blocage pour que le tableau se cale à 100% de l'écran */
@media (max-width: 768px) {
    .table-compacte {
        table-layout: auto !important; /* Rend le tableau fluide et auto-ajustable */
        width: 100% !important;
    }
    .table-compacte th, .table-compacte td {
        padding: 1px 3px !important; /* Resserre les cellules pour éviter la coupure */
    }
}
</style>
"""

# --- CONFIGURATION DROPBOX ---
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_DEPART  = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&st=mcibn3xx&dl=1"
FILE_ENGAGES = f"https://{HOTE_PROT}/scl/fi/69zkwsb45bpiw3ys3kk4c/LIVE_Liste_ENGAGES_RACB.xlsm?rlkey=qpjrlmbxhcskifnabs84veqh8&st=0snuv3e7&dl=1"

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
    centiemes = num % 100
    secondes = (num // 100) % 100
    minutes = num // 10000
    if minutes >= 60: minutes = minutes % 60
    return (minutes * 60) + secondes + (centiemes / 100)

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
def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    
    if classe_specifique == "table-class-groupes" and "Classe" in df.columns and "Groupe" in df.columns:
        html = f"<table class='table-compacte table-class-robuste'><thead><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for idx in range(len(df)):
            classe_row = ""
            if idx < len(df) - 1:
                if df.iloc[idx]["Classe"] != df.iloc[idx + 1]["Classe"] or df.iloc[idx]["Groupe"] != df.iloc[idx + 1]["Groupe"]:
                    classe_row = "class='ligne-separation-classe'"
            html += f"<tr {classe_row}>"
            for col in df.columns:
                html += f"<td>{df.iloc[idx][col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Chrono réalisé"]
    
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    t_live = "🏎️ EN DIRECT / Derniers concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 1er COURSE / Concurrents RACB"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX RACB (Top 20)"
    t_milieu = "📊 CLASSEMENT OFFICIEUX PAR Groupe / Classe (Top 3)"
    t_bas = ""

    data_engages = telecharger_excel(FILE_ENGAGES)
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
                base["Ordre_Saisie"] = range(len(base))
                df_hist_base = base.sort_values(by="Ordre_Saisie", ascending=False).copy()
                df_hist = df_hist_base[["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Chrono_C1_Visual_Hist"]].rename(columns={"Chrono_C1_Visual_Hist": "Chrono réalisé"})

                valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
                if len(valides) > 0:
                    scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                    scr = scr[~scr["Groupe"].astype(str).str.strip().str.startswith(('1', '2', '3', '4'), na=False)]
                    
                    racb = scr.head(20).copy()
                    if len(racb) > 0:
                        racb["Pos"] = range(1, len(racb) + 1)
                        racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                        df_racb = racb[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
                    
                    scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                    top3_div = scr.sort_values(by=["Groupe", "Classe_Num", "Calc_Sec"])
                    df_grouped = top3_div.groupby(["Groupe", "Classe_Num"]).head(3).copy()
                    if len(df_grouped) > 0:
                        df_grouped["Pos"] = df_grouped.groupby(["Groupe", "Classe_Num"]).cumcount() + 1
                        df_grouped["Chrono"] = df_grouped["Calc_Sec"].apply(format_final_chrono)
                        df_divisions = df_grouped[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
        except Exception: pass

    html_hist = CSS_RACB + generer_tableau_html(df_hist, "table-hist")
    html_divisions = generer_tableau_html(df_divisions, "table-class-groupes")

    return df_live, html_hist, df_racb, html_divisions, pd.DataFrame(), t_live, t_his, t_haut, t_milieu, t_bas
