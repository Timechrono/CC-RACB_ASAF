import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import time
import io
import requests

# ==============================================================================
# ⚙️ CONFIGURATION DES HAUTEURS VISUELLES SUR PC (en pixels)
# ==============================================================================
HAUTEURS_TABLEAUX_PC = {
    "HISTORIQUE": "487px",       # ⬅️ Colonne de gauche (Historique des temps)
    "RACB": "213px",             # ➡️ Haut de la colonne droite (Classement Général RACB)
    "ASAF_123": "147px",         # ➡️ Milieu de la colonne droite (Classement par Groupe / Classe)
    "ASAF_4": "215px"              # ➡️ Bas de la colonne droite (0px car inutilisé sur cette feuille)
}


st.cache_data.clear()

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    .vrai-gyrophare { display: inline-block; margin-right: 6px; font-size: 1.05rem !important; vertical-align: middle !important; }
    .titre-live, .titre-hist, .titre-classement {
        color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
        padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important;
        width: 100% !important; display: block !important; clear: both !important;
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
    .table-compacte td { border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
    .table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
    .table-compacte td.meilleur-temps { background-color: #d9fcec !important; color: #000000 !important; font-weight: bold !important; }
    .table-class-robuste tr:nth-child(odd) td { background-color: #E0F2FE !important; }
    .table-class-groupes tr.ligne-separation-classe td { border-bottom: 2px solid #1E3A8A !important; }

    /* 🚨 LE CODE DE SECOURS ABSOLU : Force le gras et la taille en ciblant chaque tableau de droite */
    div[data-testid="stMarkdownContainer"] table tr td:last-child {
        font-weight: 900 !important;
        font-size: 0.85rem !important;
    }


    /* 🎯 SOLUTION RADICALE : Force TOUTES les dernières cellules (colonne Chrono) des tableaux de droite */
    .table-compacte td:last-child, 
    .table-class-groupes td:last-child {
        font-weight: bold !important;
        font-size: 0.85rem !important;
    }
    
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
    .table-hist th:nth-child(6), .table-hist td:nth-child(15) { width: 15% !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(19) { width: 19% !important; }  
    .zone-defilement-tactile { width: 100% !important; overflow-x: auto !important; display: block !important; }
    </style>
""", unsafe_allow_html=True)
BASE_DIR = "Dropbox Cloud"
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&dl=1"
FILE_DEPART  = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&dl=1"
FILE_ENGAGES = f"https://{HOTE_PROT}/scl/fi/sqrqinksco1am700s27h4/LIVE_Liste_ENGAGES.xlsm?rlkey=8p0n8jyeuiivaa375bh3p608n&dl=1"

@st.cache_data(ttl=30)
def telecharger_excel(url):
    try:
        entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        reponse = requests.get(url, headers=entetes, timeout=12)
        return io.BytesIO(reponse.content)
    except Exception: return None

def convertir_en_secondes(valeur):
    if pd.isna(valeur) or valeur is None: return None
    if isinstance(valeur, (datetime.time, datetime.datetime)):
        return (valeur.minute * 60) + valeur.second + (valeur.microsecond / 1000000)
    s = str(valeur).strip()
    if s.endswith(".0"): s = s[:-2]
    s_clean = "".join([c for c in s if c.isdigit()])
    if not s_clean or len(s_clean) < 3: return None
    num = int(s_clean)
    if num > 595999: return None
    centiemes = num % 100
    secondes = (num // 100) % 100
    minutes = num // 10000
    return (minutes * 60) + secondes + (centiemes / 100)

def nettoyer_numero(valeur):
    if pd.isna(valeur): return "nan"
    s = str(valeur).strip().upper()
    return s[:-2] if s.endswith(".0") else s

def format_final_chrono(total_sec, fallback_statut="No Time"):
    if total_sec is None or pd.isna(total_sec) or total_sec < 0 or total_sec == float('inf'): return fallback_statut
    m, reste_sec = divmod(round(total_sec, 2), 60)
    return f"{int(m):02d}:{int(reste_sec // 1):02d}.{int(round((reste_sec % 1) * 100)):02d}".replace(".100", ".00")

def formater_heure_ecran(val):
    if pd.isna(val) or val == "" or str(val).lower() == "nan": return "-"
    s = str(val).strip()
    if s.endswith(".0"): s = s[:-2]
    s = s.zfill(6)
    return f"{s[0:2]}:{s[2:4]}.{s[4:6]}" if len(s) == 6 else str(val)

def calculer_statut_chrono_live(valeur_sec):
    if pd.isna(valeur_sec) or valeur_sec <= 0: return "No Time"
    return f"{format_final_chrono(valeur_sec)} &nbsp;<span style='color: #22C55E;'>✓</span>"

def generer_tableau_html(df, cls_spec):
    if df.empty: return "<div class='zone-defilement-tactile'><table class='table-compacte'><tr><td>Aucune donnée</td></tr></table></div>"
    return f"<div class='zone-defilement-tactile'>{df.to_html(index=False, classes=f'table-compacte {cls_spec}', escape=False, border=0)}</div>"
def recuperer_donnees_course():
    df_live = pd.DataFrame(columns=["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"])
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    html_hist = "<div class='zone-defilement-tactile'><table class='table-compacte'><tr><td>Aucune donnée</td></tr></table></div>"
    df_divisions = html_hist

    t_live = "🏎️ EN DIRECT / Derniers Concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / ASAF<span>↕️</span>"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 123 (Top 25)<span>↕️</span>"
    t_milieu = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 4 (Top 10)<span>↕️</span>"
    t_bas = "📊 CLASSEMENT OFFICIEUX par Division / Classe (Top 3)<span>↕️</span>"

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        if flux_eng is not None and flux_arr is not None:
            df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
            df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

            df_eng = pd.DataFrame({
                "N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                "Division": df_eng_raw.iloc[:, 5].astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x),
                "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
            })
            
            df_eng = df_eng[~df_eng["N°"].str.startswith("N", na=False)].copy()
            df_eng["Num_Tri_Sec"] = pd.to_numeric(df_eng["N°"], errors='coerce').fillna(-1)
            df_eng = df_eng[~((df_eng["Num_Tri_Sec"] >= 900) & (df_eng["Num_Tri_Sec"] <= 999))].copy()
            df_eng = df_eng.drop(columns=["Num_Tri_Sec"])
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
            tous_numeros_autorises_asaf = set(df_eng["N°"].unique())

            def trouver_index_colonne_titre(df, chaine_recherche):
                for c_idx in range(len(df.columns)):
                    if chaine_recherche.upper() in str(df.iloc[1, c_idx]).strip().upper(): return c_idx
                return None

            def extraire_manche_selon_regles_asaf(df_arr_raw, nom_manche, label_cat):
                d_manche = {}
                col_dossard = trouver_index_colonne_titre(df_arr_raw, f"{nom_manche} {label_cat}")
                if col_dossard is None: return d_manche
                for r_idx in range(2, len(df_arr_raw)):
                    nv = nettoyer_numero(df_arr_raw.iloc[r_idx, col_dossard])
                    if nv in tous_numeros_autorises_asaf:
                        d_manche[nv] = {
                            "h_dep": df_arr_raw.iloc[r_idx, col_dossard + 1] if pd.notna(df_arr_raw.iloc[r_idx, col_dossard + 1]) else None, 
                            "h_arr": df_arr_raw.iloc[r_idx, col_dossard + 2] if pd.notna(df_arr_raw.iloc[r_idx, col_dossard + 2]) else None, 
                            "sec": convertir_en_secondes(df_arr_raw.iloc[r_idx, col_dossard + 3])
                        }
                return d_manche

            dict_c1 = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "ASAF")
            dict_c1.update({k: v for k, v in extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 1", "RACB").items() if k not in dict_c1 or dict_c1[k]["sec"] is None})
            dict_c2 = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "ASAF")
            dict_c2.update({k: v for k, v in extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 2", "RACB").items() if k not in dict_c2 or dict_c2[k]["sec"] is None})
            
            if not df_eng.empty:
                rows_data = []
                for _, pilot in df_eng.iterrows():
                    num = pilot["N°"]
                    rows_data.append({
                        "N°": num, "Nom_Prenom": pilot["Nom_Prenom"], "Voiture": pilot["Voiture"], "Division": pilot["Division"], "Classe": pilot["Classe"],
                        "Heure_Depart_3": dict_c2.get(num, {}).get("h_dep"), "Heure_Arrivee_3": dict_c2.get(num, {}).get("h_arr"),
                        "Calc_Sec_1": dict_c1.get(num, {}).get("sec"), "Calc_Sec_2": dict_c2.get(num, {}).get("sec")
                    })
                base = pd.DataFrame(rows_data)
                
                if len(base) > 0:
                    base_c3 = base[base["Heure_Depart_3"].notna()].copy()
                    if "Heure_Depart_3" in base.columns and base["Heure_Depart_3"].notna().any():
                        base_c3["Chrono réalisé"] = base_c3.apply(lambda r: calculer_statut_chrono_live(r["Calc_Sec_2"]) if pd.notna(r["Calc_Sec_2"]) else ("🟠 EN PISTE" if pd.isna(r["Heure_Arrivee_3"]) else "No Time"), axis=1)
                        base_c3["Départ"] = base_c3["Heure_Depart_3"].apply(formater_heure_ecran)
                        base_c3["Arrivée"] = base_c3["Heure_Arrivee_3"].apply(formater_heure_ecran)
                        df_live = base_c3.sort_values(by="Heure_Depart_3", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                    df_partants = base_c3.sort_values(by="Heure_Depart_3", ascending=False).copy()
                    df_hb = df_partants.iloc[5:].copy()
                    
                    html_hist = "<div class='zone-defilement-tactile'><table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Div</th><th>Cl</th><th>Course 1</th><th>Chrono</th></tr></thead><tbody>"
                    for idx, row in df_hb.iterrows():
                        t1, t2 = row["Calc_Sec_1"], row["Calc_Sec_2"]
                        txt_c1 = format_final_chrono(t1)
                        
                        if pd.isna(t1) or t1 <= 0 or pd.isna(t2) or t2 <= 0:
                            symbole = "&nbsp;<span style='color: #9CA3AF; font-size: 1.1rem; display: inline-block; line-height: 1; vertical-align: -1px;'>◆</span>"
                        elif t2 < t1:
                            symbole = "&nbsp;<span style='color: #22C55E; font-size: 1.1rem; display: inline-block; line-height: 1; vertical-align: -1px;'>▲</span>"
                        else:
                            symbole = "&nbsp;<span style='color: #EF4444; font-size: 1.1rem; display: inline-block; line-height: 1; vertical-align: -1px;'>▼</span>"
                        
                        txt_c2 = f"{format_final_chrono(t2)}{symbole}" if t2 else f"No Time{symbole}"
                        html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Division']}</td><td>{row['Classe']}</td><td>{txt_c1}</td><td>{txt_c2}</td></tr>"
                    html_hist += "</tbody></table></div>"
