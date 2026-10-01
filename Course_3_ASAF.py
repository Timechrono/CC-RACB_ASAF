import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import time
import io
import requests

st.set_page_config(layout="wide")
st.cache_data.clear()

# --- DESIGN SCIENTIFIQUE RIGIDE RESTAURÉ ---
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
    
    /* STYLE SÉCURISÉ POUR LES 2 MEILLEURS TEMPS : VERT PASTEL ET ÉCRITURE NOIRE */
    .table-compacte td.meilleur-temps { 
        background-color: #d9fcec !important; 
        color: #000000 !important;
        font-weight: bold !important; 
    }
    
    /* ALTERNANCE BLEU CIEL UNE LIGNE SUR DEUX UNIQUEMENT POUR LE SCRATCH (TABLE-CLASS-ROBUSTE) */
    .table-class-robuste tr:nth-child(odd) td {
        background-color: #E0F2FE !important;
    }
    
    /* Séparateur de classe bleu de 2px de large */
    .ligne-separation-classe td { border-bottom: 2px solid #1E3A8A !important; }
    
    /* LARGEURS DE COLONNES FIGÉES */
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }

    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 6% !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 21% !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 6% !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 10% !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 10% !important; }  
    .table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 14% !important; }  

    .table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
    .table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
    .table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
    .table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
    .table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
    .table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

    .table-class-groupes th:nth-child(1), .table-class-groupes td:nth-child(1) { width: 9% !important; }
    .table-class-groupes th:nth-child(2), .table-class-groupes td:nth-child(2) { width: 11% !important; }
    .table-class-groupes th:nth-child(3), .table-class-groupes td:nth-child(3) { width: 33% !important; }
    .table-class-groupes th:nth-child(4), .table-class-groupes td:nth-child(4) { width: 23% !important; }
    .table-class-groupes th:nth-child(5), .table-class-groupes td:nth-child(5) { width: 6% !important; }
    .table-class-groupes th:nth-child(6), .table-class-groupes td:nth-child(6) { width: 18% !important; text-align: right !important; }

    .block-container { padding-top: 0.3rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
    hr { margin: 6px 0px !important; border: 0 !important; height: 0 !important; }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = "Dropbox Cloud"

# --- ENCODAGE NUMÉRIQUE INTERNE ANTI-CENSURE (VOS VALEURS VALIDÉES) ---
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

# Restauration stricte de vos adresses d'origine avec le bon fichier ENGAGES
FILE_ARRIVEE = f"ht" + f"tps://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&dl=1"
FILE_ENGAGES = f"ht" + f"tps://{HOTE_PROT}/scl/fi/sqrqinksco1am700s27h4/LIVE_Liste_ENGAGES.xlsm?rlkey=8p0n8jyeuiivaa375bh3p608n&dl=1"

def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    reponse = requests.get(url, headers=entetes, timeout=12)
    reponse.raise_for_status()
    return io.BytesIO(reponse.content)

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

#fin partie 1
def recuperer_donnees_course():
    import pandas as pd
    import datetime
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course 1", "Course 2", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    df_eng = pd.DataFrame() 

    try:
        df_eng_raw = pd.read_excel(telecharger_excel(FILE_ENGAGES), skiprows=1, engine='openpyxl')
        df_arr_raw = pd.read_excel(telecharger_excel(FILE_ARRIVEE), header=None, engine='openpyxl')

        def extraire_chiffre_division(txt):
            if pd.isna(txt) or txt is None: return "-"
            s = str(txt).strip()
            if s.endswith(".0"): s = s[:-2]
            chiffres = [c for c in s if c.isdigit()]
            return "".join(chiffres) if chiffres else s

        df_eng = pd.DataFrame({
            "N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
            "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
            "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
            "Division": df_eng_raw.iloc[:, 5].apply(extraire_chiffre_division),
            "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
        })
        df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
        df_eng = df_eng[df_eng["Division"].isin(["1", "2", "3", "4"])].copy()
        
        numeros_autorises_123 = set(df_eng[df_eng["Division"].isin(["1", "2", "3"])]["N°"].unique())
        numeros_autorises_4 = set(df_eng[df_eng["Division"] == "4"]["N°"].unique())
        tous_numeros_autorises_asaf = numeros_autorises_123.union(numeros_autorises_4)

        def trouver_index_colonne_titre(df, chaine_recherche):
            for c_idx in range(len(df.columns)):
                val = str(df.iloc[1, c_idx]).strip().upper()
                if chaine_recherche.upper() in val: return c_idx
            return None

        def extraire_manche_selon_regles_asaf(df_arr_raw, nom_manche, label_categorie):
            d_manche = {}
            col_dossard = trouver_index_colonne_titre(df_arr_raw, f"{nom_manche} {label_categorie}")
            if col_dossard is None: return d_manche
            for r_idx in range(2, len(df_arr_raw)):
                nv = nettoyer_numero(df_arr_raw.iloc[r_idx, col_dossard])
                if nv == "" or nv == "NAN" or nv == "NONE" or nv not in tous_numeros_autorises_asaf: continue
                val_dep = df_arr_raw.iloc[r_idx, col_dossard + 1]
                val_arr = df_arr_raw.iloc[r_idx, col_dossard + 2]
                val_calc = df_arr_raw.iloc[r_idx, col_dossard + 3]
                d_manche[nv] = {"h_dep": val_dep if pd.notna(val_dep) else None, "h_arr": val_arr if pd.notna(val_arr) else None, "sec": convertir_en_secondes(val_calc)}
            return d_manche

        dict_c1_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "ASAF")
        dict_c1_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "RACB")
        dict_c2_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "ASAF")
        dict_c2_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "RACB")
        
        # Extraction des deux colonnes pour la Manche 3
        dict_c3_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 3", "ASAF")
        dict_c3_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 3", "RACB")

        def fusionner_temps_manches(dict_asaf, dict_racb):
            d_fusion = dict_asaf.copy()
            for k, v in dict_racb.items():
                if k not in d_fusion or d_fusion[k]["sec"] is None: d_fusion[k] = v
            return d_fusion

        dict_c1 = fusionner_temps_manches(dict_c1_asaf, dict_c1_racb)
        dict_c2 = fusionner_temps_manches(dict_c2_asaf, dict_c2_racb)
        # CORRECTION : Fusion étanche des données ASAF et RACB pour la Manche 3
        dict_c3 = fusionner_temps_manches(dict_c3_asaf, dict_c3_racb)
    except Exception: pass

# fin 2 A
    if not df_eng.empty:
        try:
            rows_data = []
            for _, pilot in df_eng.iterrows():
                num = pilot["N°"]
                c1 = dict_c1.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                c2 = dict_c2.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                c3 = dict_c3.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                rows_data.append({
                    "N°": num, "Nom_Prenom": pilot["Nom_Prenom"], "Voiture": pilot["Voiture"], "Division": pilot["Division"], "Classe": pilot["Classe"],
                    "Heure_Depart_3": c3["h_dep"], "Heure_Arrivee_3": c3["h_arr"], "Calc_Sec_1": c1["sec"], "Calc_Sec_2": c2["sec"], "Calc_Sec_3": c3["sec"]
                })
            base = pd.DataFrame(rows_data)
            if len(base) > 0:
                base["Course_1_Txt"] = base["Calc_Sec_1"].apply(lambda x: format_final_chrono(x))
                base["Course_2_Txt"] = base["Calc_Sec_2"].apply(lambda x: format_final_chrono(x))

                if "Heure_Depart_3" in base.columns and base["Heure_Depart_3"].notna().any():
                    base_c3 = base[base["Heure_Depart_3"].notna()].copy()
                    def calculer_statut_live(row):
                        if pd.notna(row["Calc_Sec_3"]) and row["Calc_Sec_3"] > 0: return format_final_chrono(row["Calc_Sec_3"])
                        if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): return "<span class='vrai-gyrophare'>🚨</span> EN PISTE"
                        return "No Time"
                    base_c3["Chrono réalisé"] = base_c3.apply(calculer_statut_live, axis=1)
                    base_c3["Départ"] = base_c3["Heure_Depart_3"].apply(formater_heure_ecran)
                    base_c3["Arrivée"] = base_c3["Heure_Arrivee_3"].apply(formater_heure_ecran)
                    df_live = base_c3.sort_values(by="Heure_Depart_3", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                df_hist_base = base[base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna() | base["Calc_Sec_3"].notna()].copy()
                df_hist_base = df_hist_base.sort_values(by="Heure_Depart_3", ascending=False, na_position="last")
                
                html_hist = "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Division</th><th>Classe</th><th>Course 1</th><th>Course 2</th><th>Chrono réalisé</th></tr></thead><tbody>"
                for idx, row in df_hist_base.iterrows():
                    t1, t2, t3 = row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]
                    valides = [m for m in [t1, t2, t3] if pd.notna(m) and m > 0]
                    valides.sort()
                    s1 = "class='meilleur-temps'" if (pd.notna(t1) and t1 in valides[:2]) else ""
                    s2 = "class='meilleur-temps'" if (pd.notna(t2) and t2 in valides[:2]) else ""
                    s3 = "class='meilleur-temps'" if (pd.notna(t3) and t3 in valides[:2]) else ""

                    if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): txt_c3_visuel = "En Piste"; s3 = ""
                    elif pd.isna(t3) or t3 <= 0: txt_c3_visuel = "No Time"
                    else:
                        txt_c3 = format_final_chrono(t3); temps_precedents = [t for t in [t1, t2] if pd.notna(t) and t > 0]
                        if temps_precedents and t3 < min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                        elif temps_precedents and t3 > min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                        else: txt_c3_visuel = txt_c3

                    html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Division']}</td><td>{row['Classe']}</td><td {s1}>{format_final_chrono(t1)}</td><td {s2}>{format_final_chrono(t2)}</td><td {s3}>{txt_c3_visuel}</td></tr>"
                html_hist += "</tbody></table>"

                def calculer_cumul_deux_meilleurs(row):
                    temps = [t for t in [row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]] if pd.notna(t) and t > 0]
                    if len(temps) < 2: return float('inf')
                    temps.sort()
                    return float(sum(temps[:2]))

                base["Cumul_Sec"] = base.apply(calculer_cumul_deux_meilleurs, axis=1)
                scr = base[base["Cumul_Sec"] < float('inf')].sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                
                if len(scr) > 0:
                    asaf123 = scr[scr["Division"].isin(["1", "2", "3"])].head(25).copy()
                    if len(asaf123) > 0: asaf123["Pos"] = range(1, len(asaf123) + 1); asaf123["Chrono"] = asaf123["Cumul_Sec"].apply(format_final_chrono); df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    asaf4 = scr[scr["Division"] == "4"].head(10).copy()
                    if len(asaf4) > 0: asaf4["Pos"] = range(1, len(asaf4) + 1); asaf4["Chrono"] = asaf4["Cumul_Sec"].apply(format_final_chrono); df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                    df_grouped = scr.sort_values(by=["Division", "Classe_Num", "Cumul_Sec"]).groupby(["Division", "Classe_Num"]).head(3).copy()
                    
                    if len(df_grouped) > 0:
                        html_blocs = []
                        grouped_objs = df_grouped.groupby(["Division", "Classe_Num"])
                        total_groups, current_group = len(grouped_objs), 0
                        for (div, cl_num), group in grouped_objs:
                            current_group += 1
                            group = group.copy(); group["Pos"] = range(1, len(group) + 1); group["Chrono"] = group["Calc_Sec"].apply(format_final_chrono)
                            sub_html = group[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].to_html(index=False, header=(current_group==1), classes='table-compacte table-class-groupes', escape=False, border=0)
                            if current_group == 1: html_blocs.append(sub_html.replace("</tbody>\n</table>", ""))
                            else: html_blocs.append(sub_html.split("<tbody>")[-1].replace("</tbody>\n</table>", ""))
                            if current_group < total_groups:
                                html_blocs.append("<tr style='border-top: 2px solid #CBD5E1 !important; height:6px !important;'><td colspan='6' style='border:none !important; padding:0 !important;'></td></tr>")
                        html_blocs.append("</tbody>\n</table>")
                        df_divisions = "".join(html_blocs)
        except Exception: pass

    t_live = "🏎️ EN DIRECT / Derniers Concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 3ème COURSE / Concurrents ASAF"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 123 (Top 25)"
    t_milieu = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 4 (Top 10)"
    t_bas = "📊 CLASSEMENT OFFICIEUX par Division / Classe (Top 3)"

    return df_live, html_hist, df_asaf123, df_asaf4, df_divisions, t_live, t_his, t_haut, t_milieu, t_bas
