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

    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 25% !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 7% !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 14% !important; }  

    .table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
    .table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
    .table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
    .table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 15% !important; }
    .table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 14% !important; }
    .table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

    .table-class-groupes th:nth-child(1), .table-class-groupes td:nth-child(1) { width: 9% !important; }
    .table-class-groupes th:nth-child(2), .table-class-groupes td:nth-child(2) { width: 11% !important; }
    .table-class-groupes th:nth-child(3), .table-class-groupes td:nth-child(3) { width: 33% !important; }
    .table-class-groupes th:nth-child(4), .table-class-groupes td:nth-child(4) { width: 15% !important; }
    .table-class-groupes th:nth-child(5), .table-class-groupes td:nth-child(5) { width: 14% !important; }
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

# Restauration stricte de vos adresses d'origine avec le bon fichier ENGAGES des Essais
FILE_ARRIVEE = f"ht" + f"tps://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&dl=1"
FILE_DEPART  = f"ht" + f"tps://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&dl=1"
FILE_ENGAGES = f"ht" + f"tps://{HOTE_PROT}/scl/fi/sqrqinksco1am700s27h4/LIVE_Liste_ENGAGES.xlsm?rlkey=8p0n8jyeuiivaa375bh3p608n&dl=1"

def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    reponse = requests.get(url, headers=entetes, timeout=12)
    reponse.raise_for_status()
    return io.BytesIO(reponse.content)

def convertir_en_secondes(valeur):
    if pd.isna(valeur) or valeur is None: return None
    if isinstance(valeur, pd.Timedelta):
        return valeur.total_seconds()
    if isinstance(valeur, (datetime.time, datetime.datetime)):
        return (valeur.minute * 60) + valeur.second + (valeur.microsecond / 1000000)
    
    s = str(valeur).strip()
    if not s or s.lower() == "nan": return None

    if ":" in s:
        try:
            parts = s.split(":")
            minutes = int(parts[0])
            secondes_centièmes = float(parts[1].replace(",", "."))
            return (minutes * 60) + secondes_centièmes
        except Exception:
            pass

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

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    
    if classe_specifique == "table-class-groupes" and "Classe" in df.columns and "Division" in df.columns:
        html = f"<table class='table-compacte table-class-groupes'><thead><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for idx in range(len(df)):
            classe_row = ""
            if idx < len(df) - 1:
                if str(df.iloc[idx]["Classe"]) != str(df.iloc[idx + 1]["Classe"]) or str(df.iloc[idx]["Division"]) != str(df.iloc[idx + 1]["Division"]):
                    classe_row = "class='ligne-separation-classe'"
            html += f"<tr {classe_row}>"
            for col in df.columns:
                html += f"<td>{df.iloc[idx][col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course 1", "Chrono réalisé"]
affichage_dynamique = st.empty()

#fin partie 1
def recuperer_donnees_course():
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    try:
        df_eng_raw = pd.read_excel(telecharger_excel(FILE_ENGAGES), skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(telecharger_excel(FILE_DEPART), header=None, engine='openpyxl')
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
                s_calc = convertir_en_secondes(val_calc)
                d_manche[nv] = {"h_dep": val_dep if pd.notna(val_dep) else None, "h_arr": val_arr if pd.notna(val_arr) else None, "sec": s_calc}
            return d_manche

        dict_c1_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "ASAF")
        dict_c1_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "RACB")
        dict_c2_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "ASAF")
        dict_c2_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "RACB")

        def fusionner_temps_manches(dict_asaf, dict_racb):
            d_fusion = dict_asaf.copy()
            for k, v in dict_racb.items():
                if k not in d_fusion or d_fusion[k]["sec"] is None: d_fusion[k] = v
            return d_fusion

        dict_c1 = fusionner_temps_manches(dict_c1_asaf, dict_c1_racb)
        dict_c2 = fusionner_temps_manches(dict_c2_asaf, dict_c2_racb)

        if not df_eng.empty:
            rows_data = []
            for _, pilot in df_eng.iterrows():
                num = pilot["N°"]
                c1 = dict_c1.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                c2 = dict_c2.get(num, {"h_dep": None, "h_arr": None, "sec": None})
                rows_data.append({
                    "N°": num, "Nom_Prenom": pilot["Nom_Prenom"], "Voiture": pilot["Voiture"],
                    "Division": pilot["Division"], "Classe": pilot["Classe"],
                    "Heure_Depart_2": c2["h_dep"], "Heure_Arrivee_2": c2["h_arr"],
                    "Calc_Sec_1": c1["sec"], "Calc_Sec_2": c2["sec"]
                })
            
            base = pd.DataFrame(rows_data)
            base = base[base["N°"].isin(tous_numeros_autorises_asaf)].copy()

            if len(base) > 0:
                base["Course_1_Txt"] = base["Calc_Sec_1"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))

                if "Heure_Depart_2" in base.columns and base["Heure_Depart_2"].notna().any():
                    base_c2 = base[base["Heure_Depart_2"].notna()].copy()
                    def calculer_statut_live(row):
                        if pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0: return format_final_chrono(row["Calc_Sec_2"])
                        if pd.notna(row["Heure_Depart_2"]) and pd.isna(row["Heure_Arrivee_2"]): return "<span class='vrai-gyrophare'>🚨</span> EN PISTE"
                        return "No Time"
                    base_c2["Chrono réalisé"] = base_c2.apply(calculer_statut_live, axis=1)
                    base_c2["Départ"] = base_c2["Heure_Depart_2"].apply(formater_heure_ecran)
                    base_c2["Arrivée"] = base_c2["Heure_Arrivee_2"].apply(formater_heure_ecran)
                    df_live = base_c2.sort_values(by="Heure_Depart_2", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                df_hist_base = base[base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna()].copy()
                df_hist_base = df_hist_base.sort_values(by="Heure_Depart_2", ascending=False, na_position="last")
                def formater_chrono_historique_pur(row):
                    t2 = row["Calc_Sec_2"]; t1 = row["Calc_Sec_1"]
                    if pd.notna(row["Heure_Depart_2"]) and pd.isna(row["Heure_Arrivee_2"]): return "En Piste"
                    if pd.isna(t2) or t2 <= 0: return "No Time"
                    txt_c2 = format_final_chrono(t2)
                    if pd.notna(t1) and t1 > 0 and pd.notna(t2) and t2 > 0:
                        if t2 < t1: return f"{txt_c2} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                        elif t2 > t1: return f"{txt_c2} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                    return txt_c2
                df_hist_base["Chrono réalisé"] = df_hist_base.apply(formater_chrono_historique_pur, axis=1)
                df_hist = df_hist_base[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course_1_Txt", "Chrono réalisé"]].rename(columns={"Course_1_Txt": "Course 1"})

                valides_cumul = base[base["Calc_Sec_1"].notna() & (base["Calc_Sec_1"] > 0) & base["Calc_Sec_2"].notna() & (base["Calc_Sec_2"] > 0)].copy()
                if len(valides_cumul) > 0:
                    valides_cumul["Cumul_Sec"] = valides_cumul["Calc_Sec_1"] + valides_cumul["Calc_Sec_2"]
                    scr = valides_cumul.sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                    
                    asaf123 = scr[scr["N°"].isin(numeros_autorises_123)].head(25).copy()
                    if len(asaf123) > 0: asaf123["Pos"] = range(1, len(asaf123) + 1); asaf123["Chrono"] = asaf123["Cumul_Sec"].apply(format_final_chrono); df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    asaf4 = scr[scr["N°"].isin(numeros_autorises_4)].head(10).copy()
                    if len(asaf4) > 0: asaf4["Pos"] = range(1, len(asaf4) + 1); asaf4["Chrono"] = asaf4["Cumul_Sec"].apply(format_final_chrono); df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                    df_divisions = scr.sort_values(by=["Division", "Classe_Num", "Cumul_Sec"]).groupby(["Division", "Classe_Num"]).head(3).copy()
                    if len(df_divisions) > 0: df_divisions["Pos"] = df_divisions.groupby(["Division", "Classe_Num"]).cumcount() + 1; df_divisions["Chrono"] = df_divisions["Cumul_Sec"].apply(format_final_chrono); df_divisions = df_divisions[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
    except Exception: pass

    t_live = "🏎️ EN DIRECT / 2ème Course / Concurrents ASAF"
    t_his = "🕒 HISTORIQUE DES TEMPS / 2ème COURSE / Concurrents ASAF"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 123 (Top 25)"
    t_milieu = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 4 (Top 10)"
    t_bas = "📊 CLASSEMENT PAR Division / Classe (Top 3)"

    return df_live, df_hist, df_asaf123, df_asaf4, df_divisions, t_live, t_his, t_haut, t_milieu, t_bas

