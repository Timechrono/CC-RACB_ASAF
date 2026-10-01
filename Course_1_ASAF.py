import streamlit as st
import pandas as pd
import datetime
import requests
import io

# --- ENCODAGE NUMÉRIQUE INTERNE ANTI-CENSURE ---
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

# Adresses internet assemblées
FILE_ARRIVEE = f"ht" + f"tps://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_DEPART  = f"ht" + f"tps://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&st=mcibn3xx&dl=1"

# Les deux adresses d'engagés distinctes intégrées
FILE_ENGAGES_ASAF = f"ht" + f"tps://{HOTE_PROT}/scl/fi/wyof20d4bg4lbmnv0c7m5/LIVE_Liste_ENGAGES_ASAF.xlsm?rlkey=8q59lu88046nxu8mr8gs5ufvc&st=vny281ln&dl=1"
FILE_ENGAGES_RACB = f"ht" + f"tps://{HOTE_PROT}/scl/fi/69zkwsb45bpiw3ys3kk4c/LIVE_Liste_ENGAGES_RACB.xlsm?rlkey=qpjrlmbxhcskifnabs84veqh8&st=0snuv3e7&dl=1"

def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    reponse = requests.get(url, headers=entetes, timeout=12)
    reponse.raise_for_status()
    return io.BytesIO(reponse.content)

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
            m = int(parts[0])
            sec = float(parts[1].replace(",", "."))
            return (m * 60) + sec
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
    if "Heure_Depart" in row and pd.notna(row["Heure_Depart"]) and ("Heure_Arrivee" in row and pd.isna(row["Heure_Arrivee"])):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def extraire_engages(flux):
    df_raw = pd.read_excel(flux, skiprows=1, engine='openpyxl')
    df_raw.columns = df_raw.columns.astype(str).str.strip().str.upper()
    df_clean = pd.DataFrame({
        "N°": df_raw.iloc[:, 0].apply(nettoyer_numero), 
        "Nom_Prenom": df_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
        "Voiture": df_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
        "Division": df_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
        "Classe": df_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
    })
    return df_clean[df_clean["N°"] != "NAN"]
# fin partie 1
def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    html_divisions = "<table class='table-compacte table-class-robuste'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES_ASAF)
        flux_dep = telecharger_excel(FILE_DEPART)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(flux_dep, header=None, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

        idx_dep_asaf, idx_arr_asaf = None, None
        idx_dep_racb, idx_arr_racb = None, None

        for r in range(min(5, len(df_dep_raw))):
            for c in range(len(df_dep_raw.columns)):
                val = str(df_dep_raw.iloc[r, c]).strip().upper()
                if "COURSE 1 ASAF" in val: idx_dep_asaf = c
                elif "COURSE 1 RACB" in val: idx_dep_racb = c

        for r in range(min(5, len(df_arr_raw))):
            for c in range(len(df_arr_raw.columns)):
                val = str(df_arr_raw.iloc[r, c]).strip().upper()
                if "COURSE 1 ASAF" in val: idx_arr_asaf = c
                elif "COURSE 1 RACB" in val: idx_arr_racb = c

        deps = []
        if idx_dep_asaf is not None:
            deps.append(pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_asaf].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_asaf + 1]}))
        if idx_dep_racb is not None:
            deps.append(pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_racb].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_racb + 1]}))
        df_dep = pd.concat(deps).drop_duplicates(subset=["N°", "Heure_Depart"]) if deps else pd.DataFrame(columns=["N°", "Heure_Depart"])

        arrs = []
        if idx_arr_asaf is not None:
            arrs.append(pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_asaf].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_asaf + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_asaf + 3]}))
        if idx_arr_racb is not None:
            arrs.append(pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_racb].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_racb + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_racb + 3]}))
        df_arr = pd.concat(arrs).drop_duplicates(subset=["N°", "Heure_Arrivee"]) if arrs else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
        
        df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
        df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                               "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                               "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                               "Division": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                               "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})

        df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
        df_dep = df_dep[(df_dep["N°"] != "NAN") & (df_dep["N°"] != "")]

        for d in [df_dep, df_arr]:
            if len(d) > 0: d["N°"] = d["N°"].astype(str); d["Run_Index"] = d.groupby("N°").cumcount() + 1
# fin 2A
               # Prise en compte de toutes les divisions pour le classement par classes (de 1 à 17)
        scr_div_filtree = scr.copy()
        if len(scr_div_filtree) > 0:
            scr_div_filtree["Classe_Num"] = pd.to_numeric(scr_div_filtree["Classe"], errors='coerce').fillna(999)
            df_grouped = scr_div_filtree.sort_values(by=["Division_Clean", "Classe_Num", "Calc_Sec"]).groupby(["Division_Clean", "Classe_Num"]).head(3).copy()
            
            if len(df_grouped) > 0:
                html_blocs = []
                grouped_objs = df_grouped.groupby(["Division_Clean", "Classe_Num"])
                total_groups = len(grouped_objs)
                current_group = 0
                
                for (div, cl_num), group in grouped_objs:
                    current_group += 1
                    group = group.copy(); group["Pos"] = range(1, len(group) + 1); group["Chrono"] = group["Calc_Sec"].apply(format_final_chrono)
                    sub_df = group[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    sub_html = sub_df.to_html(index=False, header=(current_group==1), classes='table-compacte table-class-robuste', escape=False, border=0)
                    if current_group == 1: html_blocs.append(sub_html.replace("</tbody>\n</table>", ""))
                    else: html_blocs.append(sub_html.split("<tbody>")[-1].replace("</tbody>\n</table>", ""))
                    
                    if current_group < total_groups:
                        html_blocs.append("<tr style='border-top: 2px solid #CBD5E1 !important; height:6px !important;'><td colspan='6' style='border:none !important; padding:0 !important;'></td></tr>")
                
                html_blocs.append("</tbody>\n</table>")
                html_divisions = "".join(html_blocs)
    except Exception: pass

    # --- CONFIGURATION EXACTE DE L'ORDRE PHYSIQUE DE LA MANCHE 1 ---
    t_live = "🏎️ EN DIRECT / 1er Course / Concurrents ASAF"
    t_his = "🕒 HISTORIQUE DES TEMPS / 1er Course / Concurrents ASAF"
    
    t_haut = "🏆 CLASSEMENT GENERAL Division 123 (Course 1)"
    t_milieu = "🏆 CLASSEMENT GENERAL Division 4 (Course 1)"
    t_bas = "🏆 CLASSEMENT PAR DIVISIONS / CLASSES (Course 1)"

    # Renvoie l'ordre physique strict : Live, Hist, Haut (123), Milieu (4), Bas (Classes)
    return df_live, df_hist, df_asaf123, df_asaf4, html_divisions, t_live, t_his, t_haut, t_milieu, t_bas
