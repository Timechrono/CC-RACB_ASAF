import streamlit as st
import pandas as pd
import datetime
import os
import requests
import io

CSS_RACB = """
<style>
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

.table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; }
.table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }

.table-class-groupes tr.ligne-separation-classe td { 
    border-bottom: 2px solid #1E3A8A !important; 
}

/* COLORIAGE ALTERNÉ HISTORIQUE */
.table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }
.table-hist tr:nth-child(even) td { background-color: #FFFFFF !important; }

/* ========================================================================= */
/* 🖥️ CONFIGURATION PC (ORDINATEUR) : LARGEURS ÉQUILIBRÉES                  */
/* ========================================================================= */
@media (min-width: 769px) {
    /* DIRECT PC */
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 40px !important; }
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: auto !important; }
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 150px !important; }
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 80px !important; }
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 80px !important; }
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 110px !important; }

    /* HISTORIQUE PC */
    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 40px !important; }   
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: auto !important; }  
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 140px !important; }  
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 70px !important; }   
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 40px !important; }   
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 75px !important; }  
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 75px !important; }  
    .table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 100px !important; }  

    /* SCRATCH & CLASSES PC */
    .table-scratch-robuste th:nth-child(1), .table-scratch-robuste td:nth-child(1),
    .table-class-groupes th:nth-child(1), .table-class-groupes td:nth-child(1) { width: 40px !important; }
    .table-scratch-robuste th:nth-child(2), .table-scratch-robuste td:nth-child(2),
    .table-class-groupes th:nth-child(2), .table-class-groupes td:nth-child(2) { width: 40px !important; }
    .table-scratch-robuste th:nth-child(4), .table-scratch-robuste td:nth-child(4),
    .table-class-groupes th:nth-child(4), .table-class-groupes td:nth-child(4) { width: 70px !important; }
    .table-scratch-robuste th:nth-child(5), .table-scratch-robuste td:nth-child(5),
    .table-class-groupes th:nth-child(5), .table-class-groupes td:nth-child(5) { width: 50px !important; }
    .table-scratch-robuste th:nth-child(6), .table-scratch-robuste td:nth-child(6),
    .table-class-groupes th:nth-child(6), .table-class-groupes td:nth-child(6) { width: 90px !important; text-align: right !important; }
    .table-scratch-robuste th:nth-child(3), .table-scratch-robuste td:nth-child(3),
    .table-class-groupes th:nth-child(3), .table-class-groupes td:nth-child(3) { width: auto !important; }
}

/* ========================================================================= */
/* 📱 REGLAGE RIGIDE AVEC SCROLL TECHNIQUE INTÉGRAL SUR SMARTPHONE           */
/* ========================================================================= */
@media (max-width: 768px) {
    .table-compacte th, .table-compacte td { 
        font-size: 0.65rem !important; 
        padding: 1px 2px !important; 
    }

    /* EN DIRECT SMARTPHONE */
    .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 25px !important; } /* N° resserré */
    .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 110px !important; } /* Nom calé au plus large */
    .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 60px !important; }  /* Voiture réduit */
    .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 40px !important; }  /* Départ */
    .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 40px !important; }  /* Arrivée */
    .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 55px !important; font-size: 0.58rem !important; font-weight: bold !important; }

    /* HISTORIQUE SMARTPHONE */
    .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 25px !important; } /* N° resserré */
    .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 110px !important; } /* Nom coupé net après le plus large */
    .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 40px !important; }  /* Voiture réduit */
    .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 35px !important; }  /* Groupe réduit */
    .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 20px !important; }  /* Cl réduit */
    .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 48px !important; }  /* C1 */
    .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 48px !important; }  /* C2 */
    .table-hist th:nth-child(8), .table-hist td:nth-child(8) { width: 58px !important; }  /* Chrono */

    /* SCRATCH & CLASSE SMARTPHONE */
    .table-scratch-robuste th:nth-child(1), .table-scratch-robuste td:nth-child(1),
    .table-class-groupes th:nth-child(1), .table-class-groupes td:nth-child(1) { width: 22px !important; } /* Pos */
    .table-scratch-robuste th:nth-child(2), .table-scratch-robuste td:nth-child(2),
    .table-class-groupes th:nth-child(2), .table-class-groupes td:nth-child(2) { width: 25px !important; } /* N° resserré */
    .table-scratch-robuste th:nth-child(4), .table-scratch-robuste td:nth-child(4),
    .table-class-groupes th:nth-child(4), .table-class-groupes td:nth-child(4) { width: 35px !important; } /* Groupe réduit */
    .table-scratch-robuste th:nth-child(5), .table-scratch-robuste td:nth-child(5),
    .table-class-groupes th:nth-child(5), .table-class-groupes td:nth-child(5) { width: 20px !important; } /* Cl réduit */
    .table-scratch-robuste th:nth-child(6), .table-scratch-robuste td:nth-child(6),
    .table-class-groupes th:nth-child(6), .table-class-groupes td:nth-child(6) { width: 55px !important; text-align: right !important; }

    /* NOM_PRENOM AJUSTÉ AU PIXEL : Visualisation intégrale garantie sans espace résiduel */
    .table-scratch-robuste th:nth-child(3), .table-scratch-robuste td:nth-child(3),
    .table-class-groupes th:nth-child(3), .table-class-groupes td:nth-child(3) {
        width: 110px !important;
        max-width: 110px !important;
    }
}

/* CONTENEUR DE SENS TACTILE ACTIF SUR TOUS LES TABLEAUX POUR SMARTPHONE */
.zone-defilement-tactile {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    display: block !important;
}
</style>
"""

C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_ENGAGES_RACB = f"https://{HOTE_PROT}/scl/fi/69zkwsb45bpiw3ys3kk4c/LIVE_Liste_ENGAGES_RACB.xlsm?rlkey=qpjrlmbxhcskifnabs84veqh8&st=0snuv3e7&dl=1"

# SÉCURISATION BRIDAGE : 10 secondes maximum pour protéger Dropbox contre les blocages de 11h
@st.cache_data(ttl=15)
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
def calculer_statut_chrono_live(valeur_sec):
    if pd.isna(valeur_sec) or valeur_sec <= 0:
        return "No Time"
    chrono_txt = format_final_chrono(valeur_sec)
    if valeur_sec >= 240:
        return f"{chrono_txt} &nbsp;<span style='color: #EF4444; font-weight: bold;'>✗</span>"
    else:
        return f"{chrono_txt} &nbsp;<span style='color: #22C55E; font-weight: bold;'>✓</span>"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<div class='zone-defilement-tactile'><table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table></div>"
    
    html_brut = df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)
    # LE SCROLL EST DÉSORMAIS FORCÉ SUR TOUS VOS TABLEAUX POUR LE FORMAT MOBILE
    return f"<div class='zone-defilement-tactile'>{html_brut}</div>"
def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    html_hist = "<div class='zone-defilement-tactile'><table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table></div>"
    
    html_scratch = "<div class='zone-defilement-tactile'><table class='table-compacte table-scratch-robuste'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table></div>"
    html_class_div = "<div class='zone-defilement-tactile'><table class='table-compacte table-class-groupes'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table></div>"

    t_live = "🏎️ EN DIRECT / Derniers concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 3ème COURSE / Concurrents RACB"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX (Top 25)"
    t_milieu = "📊 CLASSEMENT EVOLUTIF OFFICIEUX PAR Classe (Top 3)"
    t_bas = ""

    data_engages = telecharger_excel(FILE_ENGAGES_RACB)
    data_arrivee = telecharger_excel(FILE_ARRIVEE)

    if data_engages and data_arrivee:
        try:
            df_eng_raw = pd.read_excel(data_engages, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(data_arrivee, header=None, engine='openpyxl')

            # RE-PARAMÉTRAGE STRICT DES EN-TÊTES EXIGÉES : Groupe à la place de Division, Cl à la place de Classe
            df_eng = pd.DataFrame({
                "N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                "Groupe": df_eng_raw.iloc[:, 5].fillna("-").astype(str).str.strip(),
                "Cl": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
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
                        "Groupe": pilot["Groupe"], "Cl": pilot["Cl"],
                        "Heure_Depart_3": c3["h_dep"], "Heure_Arrivee_3": c3["h_arr"],
                        "Calc_Sec_1": c1["sec"], "Calc_Sec_2": c2["sec"], "Calc_Sec_3": c3["sec"]
                    })
                base = pd.DataFrame(rows_data)

                if len(base) > 0:
                    if "Heure_Depart_3" in base.columns and base["Heure_Depart_3"].notna().any():
                        base_c3 = base[base["Heure_Depart_3"].notna()].copy()
                        base_c3["Chrono réalisé"] = base_c3.apply(lambda r: calculer_statut_chrono_live(r["Calc_Sec_3"]) if pd.notna(r["Calc_Sec_3"]) else ("<span class='vrai-gyrophare'>🚨</span> EN PISTE" if pd.isna(r["Heure_Arrivee_3"]) else "No Time"), axis=1)
                        base_c3["Départ"] = base_c3["Heure_Depart_3"].apply(formater_heure_ecran)
                        base_c3["Arrivée"] = base_c3["Heure_Arrivee_3"].apply(formater_heure_ecran)
                        df_live = base_c3.sort_values(by="Heure_Depart_3", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

                    df_hist_base = base[(base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna() | base["Calc_Sec_3"].notna())].copy()
                    if not df_hist_base.empty:
                        df_hist_base = df_hist_base.sort_values(by="Heure_Depart_3", ascending=False, na_position="last")
                        
                        # EMBAREQUEMENT STRICT DANS LE CONTENEUR TACTILE POUR L'HISTORIQUE SANS GRAS
                        html_hist = "<div class='zone-defilement-tactile'>"
                        html_hist += "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Groupe</th><th>Cl</th><th>Course 1</th><th>Course 2</th><th>Chrono réalisé</th></tr></thead><tbody>"

                        for idx, row in df_hist_base.iterrows():
                            t1, t2, t3 = row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]
                            valeurs_valides = [v for v in [t1, t2, t3] if pd.notna(v) and v > 0]
                            meilleur_sec = min(valeurs_valides) if valeurs_valides else None

                            txt_c1_visuel = f"<span style='color: #22C55E;'>•</span>&nbsp;{format_final_chrono(t1)}" if (meilleur_sec and t1 == meilleur_sec) else format_final_chrono(t1)
                            txt_c2_visuel = f"<span style='color: #22C55E;'>•</span>&nbsp;{format_final_chrono(t2)}" if (meilleur_sec and t2 == meilleur_sec) else format_final_chrono(t2)

                            if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): 
                                txt_c3_visuel = "En Piste"
                            elif pd.isna(t3) or t3 <= 0: 
                                txt_c3_visuel = "No Time"
                            else:
                                txt_c3 = format_final_chrono(t3)
                                txt_c3_base = f"<span style='color: #22C55E;'>•</span>&nbsp;{txt_c3}" if (meilleur_sec and t3 == meilleur_sec) else txt_c3
                                temps_precedents = [t for t in [t1, t2] if pd.notna(t) and t > 0]
                                
                                if temps_precedents and t3 < min(temps_precedents): 
                                    txt_c3_visuel = f"{txt_c3_base} &nbsp;<span style='color: #22C55E; font-size: 1.25rem; vertical-align: middle; display: inline-block; line-height: 1;'>▲</span>"
                                elif temps_precedents and t3 > min(temps_precedents): 
                                    txt_c3_visuel = f"{txt_c3_base} &nbsp;<span style='color: #EF4444; font-size: 1.25rem; vertical-align: middle; display: inline-block; line-height: 1;'>▼</span>"
                                else: 
                                    txt_c3_visuel = txt_c3_base

                            html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Groupe']}</td><td>{row['Cl']}</td><td>{txt_c1_visuel}</td><td>{txt_c2_visuel}</td><td>{txt_c3_visuel}</td></tr>"
                        html_hist += "</tbody></table></div>"

                    # REGLEMENT MEILLEUR DES 3 MANCHES : Participation à 2 courses achevées minimum
                    def verifier_quota_et_extraire_meilleur(row):
                        temps_manches = [v for v in [row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]] if pd.notna(v) and v > 0]
                        if len(temps_manches) >= 2:
                            return float(min(temps_manches)) # Retient uniquement la meilleure performance individuelle
                        return float('inf')

                    base["Meilleur_Resultat_Sec"] = base.apply(verifier_quota_et_extraire_meilleur, axis=1)
                    valides = base[base["Meilleur_Resultat_Sec"] < float('inf')].copy()
                    
                    if len(valides) > 0:
                        # 1. RENDU HTML DU CLASSEMENT GENERAL SCRATCH (TOP 25) - INTÉGRATION DU SCROLL FORCE
                        scr = valides.sort_values(by="Meilleur_Resultat_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                        racb_gen = scr.head(25).copy()
                        if len(racb_gen) > 0:
                            racb_gen["Pos"] = range(1, len(racb_gen) + 1)
                            racb_gen["Chrono"] = racb_gen["Meilleur_Resultat_Sec"].apply(format_final_chrono)
                            df_scratch_raw = racb_gen[["Pos", "N°", "Nom_Prenom", "Groupe", "Cl", "Chrono"]]
                            
                            html_scratch = "<div class='zone-defilement-tactile'>"
                            html_scratch += "<table class='table-compacte table-scratch-robuste'><thead><tr><th>Pos</th><th>N°</th><th>Nom_Prenom</th><th>Groupe</th><th>Cl</th><th>Chrono</th></tr></thead><tbody>"
                            for idx_s in range(len(df_scratch_raw)):
                                html_scratch += f"<tr><td>{df_scratch_raw.iloc[idx_s]['Pos']}</td><td>{df_scratch_raw.iloc[idx_s]['N°']}</td><td>{df_scratch_raw.iloc[idx_s]['Nom_Prenom']}</td><td>{df_scratch_raw.iloc[idx_s]['Groupe']}</td><td>{df_scratch_raw.iloc[idx_s]['Cl']}</td><td>{df_scratch_raw.iloc[idx_s]['Chrono']}</td></tr>"
                            html_scratch += "</tbody></table></div>"
                        
                        # 2. RENDU HTML DU CLASSEMENT EVOLUTIF PAR CLASSE (TOP 3) - INTÉGRATION DU SCROLL FORCE
                        def trier_classe_numerique(c):
                            digits = "".join([char for char in str(c) if char.isdigit()])
                            return int(digits) if digits else 999

                        scr["Classe_Tri"] = scr["Cl"].apply(trier_classe_numerique)
                        df_grouped = scr.sort_values(by=["Classe_Tri", "Cl", "Meilleur_Resultat_Sec"]).groupby("Cl", sort=False).head(3).copy()
                        df_grouped = df_grouped.sort_values(by=["Classe_Tri", "Cl", "Meilleur_Resultat_Sec"])
                        
                        if len(df_grouped) > 0:
                            df_grouped["Pos"] = df_grouped.groupby("Cl", sort=False).cumcount() + 1
                            df_grouped["Chrono"] = df_grouped["Meilleur_Resultat_Sec"].apply(format_final_chrono)
                            df_divisions_raw = df_grouped[["Pos", "N°", "Nom_Prenom", "Groupe", "Cl", "Chrono"]]
                            
                            html_class_div = "<div class='zone-defilement-tactile'>"
                            html_class_div += "<table class='table-compacte table-class-groupes'><thead><tr><th>Pos</th><th>N°</th><th>Nom_Prenom</th><th>Groupe</th><th>Cl</th><th>Chrono</th></tr></thead><tbody>"
                            for idx in range(len(df_divisions_raw)):
                                classe_row = ""
                                if idx < len(df_divisions_raw) - 1:
                                    if str(df_divisions_raw.iloc[idx]["Cl"]) != str(df_divisions_raw.iloc[idx + 1]["Cl"]):
                                        classe_row = "class='ligne-separation-classe'"
                                html_class_div += f"<tr {classe_row}><td>{df_divisions_raw.iloc[idx]['Pos']}</td><td>{df_divisions_raw.iloc[idx]['N°']}</td><td>{df_divisions_raw.iloc[idx]['Nom_Prenom']}</td><td>{df_divisions_raw.iloc[idx]['Groupe']}</td><td>{df_divisions_raw.iloc[idx]['Cl']}</td><td>{df_divisions_raw.iloc[idx]['Chrono']}</td></tr>"
                            html_class_div += "</tbody></table></div>"
        except Exception: pass

    return df_live, html_hist, html_scratch, html_class_div, pd.DataFrame(), t_live, t_his, t_haut, t_milieu, t_bas
