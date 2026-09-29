import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import time

st.set_page_config(layout="wide")
st.cache_data.clear()

# --- DESIGN SCIENTIFIQUE RIGIDE ET CONFIGURATION DES STYLES ---
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
    
    /* VERT PASTEL REPOSANT ET TEXTE EN NOIR POUR LE MEILLEUR TEMPS */
    .table-compacte td.meilleur-temps { 
        background-color: #D9FCEC !important; 
        color: #000000 !important;
        font-weight: bold !important; 
    }
    
    /* ALTERNANCE BLEU CIEL UNE LIGNE SUR DEUX UNIQUEMENT POUR LE SCRATCH GENERAL (TABLE-CLASS-ROBUSTE) */
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

# Définition initiale obligatoire des dossiers de fichiers
BASE_DIR = "C:/Dropbox/Dropbox"
FILE_ARRIVEE = os.path.join(BASE_DIR, "LIVE_Temps_ARRIVEE.xlsm")
FILE_ENGAGES = os.path.join(BASE_DIR, "LIVE_Liste_ENGAGES_ASAF.xlsm")
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

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    
    if classe_specifique == "table-class-groupes" and "Classe" in df.columns:
        cols_a_retirer = ["Cl_Tri_Num", "Cl_Tri_Suff"]
        colonnes_visibles = [c for c in df.columns if c not in cols_a_retirer]
        
        html = f"<table class='table-compacte table-class-groupes'><thead><tr>"
        for col in colonnes_visibles:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        
        for idx in range(len(df)):
            classe_row = ""
            if idx < len(df) - 1:
                if str(df.iloc[idx]["Classe"]) != str(df.iloc[idx + 1]["Classe"]):
                    classe_row = "class='ligne-separation-classe'"
            
            html += f"<tr {classe_row}>"
            for col in colonnes_visibles:
                html += f"<td>{df.iloc[idx][col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

def decomposer_classe_pour_tri(valeur_classe):
    s = str(valeur_classe).strip().upper()
    if s.endswith(".0"): s = s[:-2]
    chiffres = ""
    for char in s:
        if char.isdigit(): chiffres += char
        else: break
    if chiffres:
        return int(chiffres), s[len(chiffres):].strip()
    return 999, s
# Re-sécurisation de la variable globale au niveau de la boucle infinie
BASE_DIR = "C:/Dropbox/Dropbox"
FILE_ARRIVEE = os.path.join(BASE_DIR, "LIVE_Temps_ARRIVEE.xlsm")
FILE_ENGAGES = os.path.join(BASE_DIR, "LIVE_Liste_ENGAGES_ASAF.xlsm")

cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course 1", "Course 2", "Chrono réalisé"]
affichage_dynamique = st.empty()

while True:
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb_gen = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    FILE_ENGAGES_RACB = os.path.join(BASE_DIR, "LIVE_Liste_ENGAGES_RACB.xlsm")
    fichiers_prets = os.path.exists(FILE_ENGAGES_RACB) and os.path.exists(FILE_ARRIVEE)

    if fichiers_prets and os.path.getsize(FILE_ENGAGES_RACB) > 0 and os.path.getsize(FILE_ARRIVEE) > 0:
        try:
            df_eng_raw = pd.read_excel(FILE_ENGAGES_RACB, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(FILE_ARRIVEE, header=None, engine='openpyxl')

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
                    val = str(df.iloc[1, c_idx]).strip().upper()
                    if chaine_recherche.upper() in val:
                        return c_idx
                return None

            def extraire_manche_selon_regles_racb(df_arr_raw, nom_manche, label_categorie):
                d_manche = {}
                col_dossard = trouver_index_colonne_titre(df_arr_raw, f"{nom_manche} {label_categorie}")
                if col_dossard is None: 
                    return d_manche
                
                for r_idx in range(2, len(df_arr_raw)):
                    nv = nettoyer_numero(df_arr_raw.iloc[r_idx, col_dossard])
                    if nv == "" or nv == "NAN" or nv == "NONE": 
                        continue
                    if nv not in tous_numeros_autorises_racb:
                        continue
                        
                    val_dep = df_arr_raw.iloc[r_idx, col_dossard + 1]
                    val_arr = df_arr_raw.iloc[r_idx, col_dossard + 2]
                    val_calc = df_arr_raw.iloc[r_idx, col_dossard + 3]
                    
                    s_calc = convertir_en_secondes(val_calc)
                    d_manche[nv] = {
                        "h_dep": val_dep if pd.notna(val_dep) else None, 
                        "h_arr": val_arr if pd.notna(val_arr) else None, 
                        "sec": s_calc
                    }
                return d_manche

            dict_c1_racb = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 1", "RACB")
            dict_c1_asaf = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 1", "ASAF")
            dict_c2_racb = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 2", "RACB")
            dict_c2_asaf = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 2", "ASAF")
            dict_c3_racb = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 3", "RACB")
            dict_c3_asaf = extraire_manche_selon_regles_racb(df_arr_raw, "COURSE 3", "ASAF")

            def fusionner_temps_manches_inverse(dict_racb, dict_asaf):
                d_fusion = dict_racb.copy()
                for k, v in dict_asaf.items():
                    if k not in d_fusion or d_fusion[k]["sec"] is None:
                        d_fusion[k] = v
                return d_fusion

            dict_c1 = fusionner_temps_manches_inverse(dict_c1_racb, dict_c1_asaf)
            dict_c2 = fusionner_temps_manches_inverse(dict_c2_racb, dict_c2_asaf)
            dict_c3 = fusionner_temps_manches_inverse(dict_c3_racb, dict_c3_asaf)
        except Exception as e:
            pass
        # Continuité directe du bloc 'if' du bloc 3
        if not df_eng.empty:
            try:
                html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible pour le plateau RACB</td></tr></table>"
                
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
                base = base[base["N°"].isin(tous_numeros_autorises_racb)].copy()

                if len(base) > 0:
                    base["Course_1_Txt"] = base["Calc_Sec_1"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))
                    base["Course_2_Txt"] = base["Calc_Sec_2"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))

                    # --- LIVE EN DIRECT ---
                    df_live = pd.DataFrame(columns=cols_live)
                    if "Heure_Depart_3" in base.columns and base["Heure_Depart_3"].notna().any():
                        base_c3 = base[base["Heure_Depart_3"].notna()].copy()
                        
                        def calculer_statut_live(row):
                            if pd.notna(row["Calc_Sec_3"]) and row["Calc_Sec_3"] > 0: return format_final_chrono(row["Calc_Sec_3"])
                            if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): return "<span class='vrai-gyrophare'>🚨</span> EN PISTE"
                            return "No Time"
                            
                        base_c3["Chrono réalisé"] = base_c3.apply(calculer_statut_live, axis=1)
                        base_c3["Départ"] = base_c3["Heure_Depart_3"].apply(formater_heure_ecran)
                        base_c3["Arrivée"] = base_c3["Heure_Arrivee_3"].apply(formater_heure_ecran)
                        base_c3_trie = base_c3.sort_values(by="Heure_Depart_3", ascending=False)
                        df_live = base_c3_trie.head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                    # --- HISTORIQUE DE GAUCHE AVEC CELLULE MEILLEUR TEMPS EN VERT ---
                    a_couru = base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna() | base["Calc_Sec_3"].notna()
                    df_hist_base = base[a_couru].copy()
                    
                    if not df_hist_base.empty:
                        df_hist_base = df_hist_base.sort_values(by="Heure_Depart_3", ascending=False, na_position="last")
                        
                        html_hist = "<table class='table-compacte table-hist'><thead><tr>"
                        for col in ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course 1", "Course 2", "Chrono réalisé"] :
                            html_hist += f"<th>{col}</th>"
                        html_hist += "</tr></thead><tbody>"

                        for idx, row in df_hist_base.iterrows():
                            t1, t2, t3 = row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]
                            
                            valeurs_valides = [v for v in [t1, t2, t3] if pd.notna(v) and v > 0]
                            meilleur_sec = min(valeurs_valides) if valeurs_valides else None

                            # Attribution sécurisée de la classe de couleur verte pastel doux sans conflit
                            s1 = "class='meilleur-temps'" if (meilleur_sec and t1 == meilleur_sec) else ""
                            s2 = "class='meilleur-temps'" if (meilleur_sec and t2 == meilleur_sec) else ""
                            s3 = "class='meilleur-temps'" if (meilleur_sec and t3 == meilleur_sec) else ""

                            if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]):
                                txt_c3_visuel = "En Piste"
                                s3 = "" 
                            elif pd.isna(t3) or t3 <= 0:
                                txt_c3_visuel = "No Time"
                            else:
                                txt_c3 = format_final_chrono(t3)
                                temps_precedents = [t for t in [t1, t2] if pd.notna(t) and t > 0]
                                if temps_precedents:
                                    meilleur_precedent = min(temps_precedents)
                                    if t3 < meilleur_precedent: txt_c3_visuel = f"{txt_c3} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                                    elif t3 > meilleur_precedent: txt_c3_visuel = f"{txt_c3} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                                    else: txt_c3_visuel = txt_c3
                                else:
                                    txt_c3_visuel = txt_c3

                            txt_c1_visuel = format_final_chrono(t1)
                            txt_c2_visuel = format_final_chrono(t2)

                            html_hist += f"<tr>"
                            html_hist += f"<td>{row['N°']}</td>"
                            html_hist += f"<td>{row['Nom_Prenom']}</td>"
                            html_hist += f"<td>{row['Voiture']}</td>"
                            html_hist += f"<td>{row['Division']}</td>"
                            html_hist += f"<td>{row['Classe']}</td>"
                            html_hist += f"<td {s1}>{txt_c1_visuel}</td>"
                            html_hist += f"<td {s2}>{txt_c2_visuel}</td>"
                            html_hist += f"<td {s3}>{txt_c3_visuel}</td>"
                            html_hist += f"</tr>"
                        html_hist += "</tbody></table>"

                    # --- CALCUL DU MEILLEUR TEMPS (STRICT 2 MANCHES) ---
                    def calculer_meilleur_temps_strict_deux_manches_racb(row):
                        temps = []
                        if pd.notna(row["Calc_Sec_1"]) and row["Calc_Sec_1"] > 0: temps.append(row["Calc_Sec_1"])
                        if pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0: temps.append(row["Calc_Sec_2"])
                        if pd.notna(row["Calc_Sec_3"]) and row["Calc_Sec_3"] > 0: temps.append(row["Calc_Sec_3"])
                        if len(temps) < 2: return float('inf')
                        return float(min(temps))

                    base["Cumul_Sec"] = base.apply(calculer_meilleur_temps_strict_deux_manches_racb, axis=1)
                    valides = base[base["Cumul_Sec"] < float('inf')].copy()
                    if len(valides) > 0:
                        scr = valides.sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                        
                        # --- 1. CLASSEMENT GENERAL SCRATCH ---
                        racb_gen = scr.head(25).copy()
                        if len(racb_gen) > 0:
                            racb_gen["Pos"] = range(1, len(racb_gen) + 1)
                            racb_gen["Chrono"] = racb_gen["Cumul_Sec"].apply(format_final_chrono)
                            df_racb_gen = racb_gen[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                        
                        # --- 2. CLASSEMENT PAR CLASSE ---
                        scr["Cl_Tri_Num"] = scr["Classe"].apply(lambda x: decomposer_classe_pour_tri(x))
                        scr["Cl_Tri_Suff"] = scr["Classe"].apply(lambda x: decomposer_classe_pour_tri(x))
                        
                        scr_trie = scr.sort_values(by=["Cl_Tri_Num", "Cl_Tri_Suff", "Cumul_Sec"])
                        df_grouped = scr_trie.groupby("Classe", sort=False).head(3).copy()
                        df_grouped = df_grouped.sort_values(by=["Cl_Tri_Num", "Cl_Tri_Suff", "Cumul_Sec"])
                        
                        if len(df_grouped) > 0:
                            df_grouped["Pos"] = df_grouped.groupby("Classe", sort=False).cumcount() + 1
                            df_grouped["Chrono"] = df_grouped["Cumul_Sec"].apply(format_final_chrono)
                            df_divisions = df_grouped[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono", "Cl_Tri_Num", "Cl_Tri_Suff"]]
            except Exception as e:
                st.sidebar.error(f"Incident technique : {str(e)}")
                pass

    with affichage_dynamique.container():
        if not fichiers_prets:
            st.warning(f"⚠️ En attente des fichiers Excel dans le dossier : {BASE_DIR}")
        else:
            cg, cd = st.columns([1.3, 0.9])
            with cg:
                st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers Concurrents partis</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_live, "table-live"), unsafe_allow_html=True)
                st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-hist'>🕒 HISTORIQUE DES TEMPS / 3ème COURSE / Concurrents RACB</span>", unsafe_allow_html=True)
                st.markdown(html_hist, unsafe_allow_html=True) 
            with cd:
                st.markdown("<span class='titre-classement'>🏆 CLASSEMENT GENERAL OFFICIEUX (Top 25)</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_racb_gen, "table-class-robuste"), unsafe_allow_html=True)
                st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
                st.markdown("<span class='titre-classement'>📊 CLASSEMENT OFFICIEUX PAR Groupe/Classe (Top 3)</span>", unsafe_allow_html=True)
                st.markdown(generer_tableau_html(df_divisions, "table-class-groupes"), unsafe_allow_html=True)
    time.sleep(1)
