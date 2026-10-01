import streamlit as st
import pandas as pd
import datetime
import os
import requests
import io

CSS_RACB = """
<style>
.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 6% !important; }   
.table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
.table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 21% !important; }  
.table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; }   
.table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 6% !important; }   
.table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 10% !important; }  
.table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 10% !important; }  
.table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 14% !important; }  
</style>
"""

C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
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
    if isinstance(valeur, (datetime.time, datetime.datetime)):
        return (valeur.minute * 60) + valeur.second + (valeur.microsecond / 1000000)
    s = str(valeur).strip()
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
def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    df_racb_gen = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    data_engages = telecharger_excel(FILE_ENGAGES_RACB)
    data_arrivee = telecharger_excel(FILE_ARRIVEE)

    if data_engages and data_arrivee:
        try:
            df_eng_raw = pd.read_excel(data_engages, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(data_arrivee, header=None, engine='openpyxl')

            df_eng = pd.DataFrame({
                "N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                "Division": df_eng_raw.iloc[:, 5].fillna("-").astype(str).str.strip(),
                "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
            })
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
            tous_numeros_autorises_racb = set(df_eng["N°"].unique())

            def trouver_index_colonne_titre(df, chaine_recherche):
                for c_idx in range(len(df.columns)):
                    if chaine_recherche.upper() in str(df.iloc[1, c_idx]).strip().upper(): return c_idx
                return None

            def extraire_manche_selon_regles_racb(df_arr_raw, nom_manche, label_categorie):
                d_manche = {}
                col_dossard = trouver_index_colonne_titre(df_arr_raw, f"{nom_manche} {label_categorie}")
                if col_dossard is None: return d_manche
                
                for r_idx in range(2, len(df_arr_raw)):
                    nv = nettoyer_numero(df_arr_raw.iloc[r_idx, col_dossard])
                    if nv in ["", "NAN", "NONE"] or nv not in tous_numeros_autorises_racb: continue
                    d_manche[nv] = {
                        "h_dep": df_arr_raw.iloc[r_idx, col_dossard + 1] if pd.notna(df_arr_raw.iloc[r_idx, col_dossard + 1]) else None, 
                        "h_arr": df_arr_raw.iloc[r_idx, col_dossard + 2] if pd.notna(df_arr_raw.iloc[r_idx, col_dossard + 2]) else None, 
                        "sec": convertir_en_secondes(df_arr_raw.iloc[r_idx, col_dossard + 3])
                    }
                return d_manche

            dict_c1 = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 1", "RACB")
            dict_c1.update({k: v for k, v in extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 1", "ASAF").items() if k not in dict_c1 or dict_c1[k]["sec"] is None})
            dict_c2 = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 2", "RACB")
            dict_c2.update({k: v for k, v in extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 2", "ASAF").items() if k not in dict_c2 or dict_c2[k]["sec"] is None})
            dict_c3 = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 3", "RACB")
            dict_c3.update({k: v for k, v in extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 3", "ASAF").items() if k not in dict_c3 or dict_c3[k]["sec"] is None})

            if not df_eng.empty:
                rows_data = []
                for _, pilot in df_eng.iterrows():
                    num = pilot["N°"]
                    c1 = dict_c1.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                    c2 = dict_c2.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                    c3 = dict_c3.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                    rows_data.append({
                        "N°": num, "Nom_Prenom": pilot["Nom_Prenom"], "Voiture": pilot["Voiture"],
                        "Division": pilot["Division"], "Classe": pilot["Classe"],
                        "Heure_Depart_3": c3["h_dep"], "Heure_Arrivee_3": c3["h_arr"],
                        "Calc_Sec_1": c1["sec"], "Calc_Sec_2": c2["sec"], "Calc_Sec_3": c3["sec"]
                    })
                base = pd.DataFrame(rows_data)

                if len(base) > 0:
                    if "Heure_Depart_3" in base.columns and base["Heure_Depart_3"].notna().any():
                        base_c3 = base[base["Heure_Depart_3"].notna()].copy()
                        base_c3["Chrono réalisé"] = base_c3.apply(lambda r: format_final_chrono(r["Calc_Sec_3"]) if pd.notna(r["Calc_Sec_3"]) and r["Calc_Sec_3"] > 0 else ("<span class='vrai-gyrophare'>🚨</span> EN PISTE" if pd.isna(r["Heure_Arrivee_3"]) else "No Time"), axis=1)
                        base_c3["Départ"] = base_c3["Heure_Depart_3"].apply(formater_heure_ecran)
                        base_c3["Arrivée"] = base_c3["Heure_Arrivee_3"].apply(formater_heure_ecran)
                        df_live = base_c3.sort_values(by="Heure_Depart_3", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                    df_hist_base = base[(base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna() | base["Calc_Sec_3"].notna())].copy()
                    if not df_hist_base.empty:
                        df_hist_base = df_hist_base.sort_values(by="Heure_Depart_3", ascending=False, na_position="last")
                        html_hist = CSS_RACB + "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Division</th><th>Classe</th><th>Course 1</th><th>Course 2</th><th>Chrono réalisé</th></tr></thead><tbody>"

                        for idx, row in df_hist_base.iterrows():
                            t1, t2, t3 = row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]
                            valeurs_valides = [v for v in [t1, t2, t3] if pd.notna(v) and v > 0]
                            meilleur_sec = min(valeurs_valides) if valeurs_valides else None

                            s1 = "class='meilleur-temps'" if (meilleur_sec and t1 == meilleur_sec) else ""
                            s2 = "class='meilleur-temps'" if (meilleur_sec and t2 == meilleur_sec) else ""
                            s3 = "class='meilleur-temps'" if (meilleur_sec and t3 == meilleur_sec) else ""

                            if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): txt_c3_visuel, s3 = "En Piste", ""
                            elif pd.isna(t3) or t3 <= 0: txt_c3_visuel = "No Time"
                            else:
                                txt_c3 = format_final_chrono(t3)
                                temps_precedents = [t for t in [t1, t2] if pd.notna(t) and t > 0]
                                if temps_precedents and t3 < min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                                elif temps_precedents and t3 > min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                                else: txt_c3_visuel = txt_c3

                            html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Division']}</td><td>{row['Classe']}</td><td {s1}>{format_final_chrono(t1)}</td><td {s2}>{format_final_chrono(t2)}</td><td {s3}>{txt_c3_visuel}</td></tr>"
                        html_hist += "</tbody></table>"

                    def calc_cumul_strict(row):
                        t = [v for v in [row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]] if pd.notna(v) and v > 0]
                        return float(min(t)) if len(t) >= 2 else float('inf')

                    base["Cumul_Sec"] = base.apply(calc_cumul_strict, axis=1)
                    valides = base[base["Cumul_Sec"] < float('inf')].copy()
                    if len(valides) > 0:
                        scr = valides.sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                        racb_gen = scr.head(25).copy()
                        if len(racb_gen) > 0:
                            racb_gen["Pos"] = range(1, len(racb_gen) + 1)
                            racb_gen["Chrono"] = racb_gen["Cumul_Sec"].apply(format_final_chrono)
                            df_racb_gen = racb_gen[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
        except Exception: pass

    return df_live, html_hist, df_racb_gen, pd.DataFrame(), pd.DataFrame(), "🏎️ EN DIRECT / Derniers Concurrents partis", "🕒 HISTORIQUE DES TEMPS / 3ème COURSE / Concurrents RACB", "🏆 CLASSEMENT GENERAL OFFICIEUX (Top 25)", "", ""
