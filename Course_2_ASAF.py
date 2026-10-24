import streamlit as st
import pandas as pd
import datetime
import requests  
import io        

# ==============================================================================
# ⚙️ CONFIGURATION DES HAUTEURS VISUELLES SUR PC (en pixels)
# ==============================================================================
HAUTEURS_TABLEAUX_PC = {
    "HISTORIQUE": "485px",       # ⬅️ Colonne de gauche (Historique des temps)
    "RACB": "213px",             # ➡️ Haut de la colonne droite (Classement Général RACB)
    "ASAF_123": "147px",         # ➡️ Milieu de la colonne droite (Classement par Groupe / Classe)
    "ASAF_4": "215px"            # ➡️ Bas de la colonne droite (0px car inutilisé sur cette feuille)
}


CSS_RIGIDE_ORIGINE = """
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

/* COLORIAGE ALTERNÉ 1 LIGNE SUR 2 DANS L'HISTORIQUE */
.table-hist tr:nth-child(odd) td { 
    background-color: #E0F2FE !important; 
}
.table-hist tr:nth-child(even) td { 
    background-color: #FFFFFF !important; 
}

.table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; }
.table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }

.table-class-groupes tr.ligne-separation-classe td { 
    border-bottom: 2px solid #1E3A8A !important; 
}

.table-hist td:nth-last-child(2), .table-hist td:last-child,
.table-live td:last-child, .table-class-robuste td:last-child {
    font-size: 0.94rem !important; color: #0F172A !important;
}

/* LARGEURS STRICTES PC REPARÉES */
.table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
.table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
.table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
.table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
.table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
.table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }

.table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 6% !important; }   
.table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 22% !important; }  
.table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; }  
.table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 13% !important; }   
.table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 6% !important; }   
.table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }  
.table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 17% !important; }  

.table-class-robuste th:nth-child(1), .table-class-robuste td:nth-child(1) { width: 9% !important; }
.table-class-robuste th:nth-child(2), .table-class-robuste td:nth-child(2) { width: 11% !important; }
.table-class-robuste th:nth-child(3), .table-class-robuste td:nth-child(3) { width: 33% !important; }
.table-class-robuste th:nth-child(4), .table-class-robuste td:nth-child(4) { width: 23% !important; }
.table-class-robuste th:nth-child(5), .table-class-robuste td:nth-child(5) { width: 6% !important; }
.table-class-robuste th:nth-child(6), .table-class-robuste td:nth-child(6) { width: 18% !important; text-align: right !important; }

.table-class-groupes th:nth-child(1), .table-class-groupes td:nth-child(1) { width: 5% !important; }   
.table-class-groupes th:nth-child(2), .table-class-groupes td:nth-child(2) { width: 8% !important; }   
.table-class-groupes th:nth-child(3), .table-class-groupes td:nth-child(3) { width: 35% !important; }  
.table-class-groupes th:nth-child(4), .table-class-groupes td:nth-child(4) { width: 21% !important; }  
.table-class-groupes th:nth-child(5), .table-class-groupes td:nth-child(5) { width: 11% !important; }  
.table-class-groupes th:nth-child(6), .table-class-groupes td:nth-child(6) { width: 14% !important; text-align: right !important; } 
.table-class-groupes tr td { background-color: #FFFFFF !important; }

/* STYLE EXCLUSIF DE DEFILEMENT POUR SENS TACTILE SMARTPHONE */
.zone-defilement-tactile {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
}
</style>
"""
# SÉCURISATION BRIDAGE : 10 secondes maximum pour protéger Dropbox contre les blocages de 11h
@st.cache_data(ttl=30)
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
    if "Calc_Sec_2" in row and pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0:
        chrono_txt = format_final_chrono(row["Calc_Sec_2"])
        if est_dans_le_live:
            if row["Calc_Sec_2"] >= 240:
                return f"{chrono_txt} &nbsp;<span style='color: #EF4444; font-weight: bold;'>✗</span>"
            else:
                return f"{chrono_txt} &nbsp;<span style='color: #22C55E; font-weight: bold;'>✓</span>"
        return chrono_txt
    if "Heure_Depart_2" in row and pd.notna(row["Heure_Depart_2"]) and ("Heure_Arrivee_2" in row and pd.isna(row["Heure_Arrivee_2"])):
        return "<span class='vrai-gyrophare'>🟠</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    
    html_brut = df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)
    if "table-live" in classe_specifique:
        return f"<div class='zone-defilement-tactile'>{html_brut}</div>"
    return html_brut

def decomposer_classe_pour_tri(valeur_classe):
    s = str(valeur_classe).strip().upper()
    if s.endswith(".0"): s = s[:-2]
    chiffres = "".join([c for c in s if c.isdigit()])
    return int(chiffres) if chiffres else 999

def extraire_suffixe_pour_tri(valeur_classe):
    s = str(valeur_classe).strip().upper()
    if s.endswith(".0"): s = s[:-2]
    chiffres = "".join([c for c in s if c.isdigit()])
    return s[len(chiffres):].strip()
def recuperer_donnees_course():
    C = [119, 119, 119, 46, 100, 114, 111, 112, 98, 111, 120]
    D = [46, 99, 111, 109]
    HOTE_PROT = "".join(chr(x) for x in (C + D))

    FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&dl=1"
    FILE_DEPART  = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&dl=1"
    FILE_ENGAGES_ASAF = f"https://{HOTE_PROT}/scl/fi/wyof20d4bg4lbmnv0c7m5/LIVE_Liste_ENGAGES_ASAF.xlsm?rlkey=8q59lu88046nxu8mr8gs5ufvc&st=vny281ln&dl=1"

    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Course 1", "Chrono réalisé"]
    df_live, df_hist = pd.DataFrame(columns=cols_live), pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    t_live = "🏎️ EN DIRECT / Derniers concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 2ème COURSE / Concurrents ASAF<span>↕️</span>"
    t_haut = "🏆 CLASSEMENT EVOLUTIF OFFICIEUX Division 123 ASAF<span>↕️</span>"
    t_milieu = "🏆 CLASSEMENT EVOLUTIF OFFICIEUX Division 4 ASAF<span>↕️</span>"
    t_bas = "📊 CLASSEMENT EVOLUTIF OFFICIEUX PAR Classe (Top 3)<span>↕️</span>"

    fichiers_prets = False
    try:
        file_engages_bytes = telecharger_excel(FILE_ENGAGES_ASAF)
        file_depart_bytes = telecharger_excel(FILE_DEPART)
        file_arrivee_bytes = telecharger_excel(FILE_ARRIVEE)
        fichiers_prets = True
    except:
        pass

    if fichiers_prets:
        try:
            df_eng_raw = pd.read_excel(file_engages_bytes, header=1, engine='openpyxl')
            df_dep_raw = pd.read_excel(file_depart_bytes, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(file_arrivee_bytes, header=None, engine='openpyxl')
            
            df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
            df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                                   "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                                   "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                                   "Groupe": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                                   "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])

            dep1_list, arr1_list, dep2_list, arr2_list = [], [], [], []

            for c_idx in range(len(df_dep_raw.columns)):
                val = str(df_dep_raw.iloc[1, c_idx]).strip().upper()
                if "COURSE 1 ASAF" in val or "COURSE 1 RACB" in val:
                    dep1_list.append(pd.DataFrame({"N°": df_dep_raw.iloc[2:, c_idx].apply(nettoyer_numero), "Heure_Depart_1": df_dep_raw.iloc[2:, c_idx + 1]}))
                elif "COURSE 2 ASAF" in val or "COURSE 2 RACB" in val:
                    dep2_list.append(pd.DataFrame({"N°": df_dep_raw.iloc[2:, c_idx].apply(nettoyer_numero), "Heure_Depart_2": df_dep_raw.iloc[2:, c_idx + 1]}))

            for c_idx in range(len(df_arr_raw.columns)):
                val = str(df_arr_raw.iloc[1, c_idx]).strip().upper()
                if "COURSE 1 ASAF" in val or "COURSE 1 RACB" in val:
                    arr1_list.append(pd.DataFrame({"N°": df_arr_raw.iloc[2:, c_idx].apply(nettoyer_numero), "Heure_Arrivee_1": df_arr_raw.iloc[2:, c_idx + 2]}))
                elif "COURSE 2 ASAF" in val or "COURSE 2 RACB" in val:
                    arr2_list.append(pd.DataFrame({"N°": df_arr_raw.iloc[2:, c_idx].apply(nettoyer_numero), "Heure_Arrivee_2": df_arr_raw.iloc[2:, c_idx + 2]}))

            df_dep1 = pd.concat(dep1_list, ignore_index=True) if dep1_list else pd.DataFrame(columns=["N°", "Heure_Depart_1"])
            df_arr1 = pd.concat(arr1_list, ignore_index=True) if arr1_list else pd.DataFrame(columns=["N°", "Heure_Arrivee_1"])
            df_dep2 = pd.concat(dep2_list, ignore_index=True) if dep2_list else pd.DataFrame(columns=["N°", "Heure_Depart_2"])
            df_arr2 = pd.concat(arr2_list, ignore_index=True) if arr2_list else pd.DataFrame(columns=["N°", "Heure_Arrivee_2"])
            
            # --- NETTOYAGE ET SÉCURISATION DES DONNÉES ---
            # Correction : On nettoie d'abord les fichiers pour ne garder QUE la dernière action valide de chaque voiture
            df_dep1 = df_dep1[(df_dep1["N°"] != "NAN") & (df_dep1["N°"] != "")].drop_duplicates(subset=["N°"], keep="last")
            df_arr1 = df_arr1[(df_arr1["N°"] != "NAN") & (df_arr1["N°"] != "")].drop_duplicates(subset=["N°"], keep="last")
            df_dep2 = df_dep2[(df_dep2["N°"] != "NAN") & (df_dep2["N°"] != "")].drop_duplicates(subset=["N°"], keep="last")
            df_arr2 = df_arr2[(df_arr2["N°"] != "NAN") & (df_arr2["N°"] != "")].drop_duplicates(subset=["N°"], keep="last")

            if len(df_dep1) > 0: df_dep1["Sec_Dep_1"] = df_dep1["Heure_Depart_1"].apply(convertir_en_secondes)
            if len(df_arr1) > 0: df_arr1["Sec_Arr_1"] = df_arr1["Heure_Arrivee_1"].apply(convertir_en_secondes)
            if len(df_dep2) > 0: df_dep2["Sec_Dep_2"] = df_dep2["Heure_Depart_2"].apply(convertir_en_secondes)
            if len(df_arr2) > 0: df_arr2["Sec_Arr_2"] = df_arr2["Heure_Arrivee_2"].apply(convertir_en_secondes)

            # Identification de la manche active
            est_en_c2 = "Heure_Depart_2" in df_dep2.columns and len(df_dep2) > 0
            df_actif = df_dep2 if est_en_c2 else df_dep1

            if len(df_actif) > 0:
                df_actif = df_actif.copy()
                # On marque l'ordre physique global de saisie de l'Excel nettoyé
                df_actif["Ordre_Passage"] = range(len(df_actif))

                # 1. Base globale regroupée (ASAF + RACB) pour les classements officieux de droite
                base = pd.merge(df_actif, df_eng, on="N°", how="inner")
                
                # 2. Base restreinte : Exclure strictement les lignes RACB de l'affichage visuel de gauche
                mot_cle_tri = "COURSE 2 ASAF" if est_en_c2 else "COURSE 1 ASAF"
                liste_asaf_numeros = []
                for c_idx in range(len(df_dep_raw.columns)):
                    if mot_cle_tri in str(df_dep_raw.iloc[1, c_idx]).strip().upper():
                        liste_asaf_numeros = df_dep_raw.iloc[2:, c_idx].apply(nettoyer_numero).dropna().tolist()
                        break
                
                df_actif_asaf = df_actif[df_actif["N°"].isin(liste_asaf_numeros)].copy()
                base_visuelle_gauche = pd.merge(df_actif_asaf, df_eng, on="N°", how="inner")

                if est_en_c2 and len(df_arr2) > 0: base = pd.merge(base, df_arr2, on="N°", how="left")
                if not est_en_c2 and len(df_arr1) > 0: base = pd.merge(base, df_arr1, on="N°", how="left")
                
                if est_en_c2 and len(df_dep1) > 0: base = pd.merge(base, df_dep1.drop_duplicates('N°', keep='last'), on="N°", how="left")
                if est_en_c2 and len(df_arr1) > 0: base = pd.merge(base, df_arr1.drop_duplicates('N°', keep='last'), on="N°", how="left")

                base["Calc_Sec_1"] = (base.get("Sec_Arr_1", pd.Series(dtype=float)) - base.get("Sec_Dep_1", pd.Series(dtype=float))).apply(lambda x: x + 3600 if (x is not None and x < 0) else x) if "Sec_Arr_1" in base.columns else None
                base["Calc_Sec_2"] = (base.get("Sec_Arr_2", pd.Series(dtype=float)) - base.get("Sec_Dep_2", pd.Series(dtype=float))).apply(lambda x: x + 3600 if (x is not None and x < 0) else x) if "Sec_Arr_2" in base.columns else None

                # Injection des données d'Arrivée nettoyées pour le tableau visuel de gauche
                if est_en_c2 and len(df_arr2) > 0:
                    base_visuelle_gauche = pd.merge(base_visuelle_gauche, df_arr2, on="N°", how="left")
                elif not est_en_c2 and len(df_arr1) > 0:
                    base_visuelle_gauche = pd.merge(base_visuelle_gauche, df_arr1, on="N°", how="left")
                
                base_visuelle_gauche = pd.merge(base_visuelle_gauche, base[["N°", "Calc_Sec_1", "Calc_Sec_2"]], on="N°", how="left")

                df_hist_base = pd.DataFrame(columns=base_visuelle_gauche.columns)
                df_live = pd.DataFrame(columns=["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"])

                # Inversion de la pile EXCLUSIVE ASAF unique pour l'affichage en direct
                pile_inversee = base_visuelle_gauche.sort_values(by="Ordre_Passage", ascending=False).copy()

                # EN DIRECT : Reçoit les 5 derniers concurrents ASAF uniques partis
                df_live_base = pile_inversee.head(5).copy()
                df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                
                h_dep_col = "Heure_Depart_2" if est_en_c2 else "Heure_Depart_1"
                h_arr_col = "Heure_Arrivee_2" if est_en_c2 else "Heure_Arrivee_1"
                df_live_base["Départ_Visuel"] = df_live_base[h_dep_col].apply(formater_heure_ecran) if h_dep_col in df_live_base.columns else "-"
                df_live_base["Arrivée_Visuel"] = df_live_base[h_arr_col].apply(formater_heure_ecran) if h_arr_col in df_live_base.columns else "-"
                df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_Visuel", "Arrivée_Visuel", "Chrono réalisé"]].rename(columns={"Départ_Visuel": "Départ", "Arrivée_Visuel": "Arrivée"})

                # HISTORIQUE : Les concurrents ASAF uniques poussés au-delà du Top 5 (sans doublons, sans RACB)
                df_hist_base = pile_inversee.iloc[5:].copy() if len(pile_inversee) > 5 else pd.DataFrame(columns=pile_inversee.columns)
                # --- GÉNÉRATION DU FLUX HTML EXCLUSIF ASAF ---
                html_hist = "<div class='zone-defilement-tactile'>"
                html_hist += "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Groupe</th><th>Cl</th><th>Course 1</th><th>Chrono</th></tr></thead><tbody>"

                for idx, row in df_hist_base.iterrows():
                    t1 = row.get("Calc_Sec_1", None)
                    t2 = row.get("Calc_Sec_2", None)
                    has_t1 = pd.notna(t1) and isinstance(t1, (int, float)) and t1 > 0
                    has_t2 = pd.notna(t2) and isinstance(t2, (int, float)) and t2 > 0
                    
                    txt_c1_visuel = format_final_chrono(t1)
                    txt_c2_brut = format_final_chrono(t2)

                    if est_en_c2:
                        if not has_t2:
                            # Correction d'affichage pour l'Historique : Si pas d'arrivée, on force "No Time"
                            txt_c2_visuel = f"No Time &nbsp;<span style='color: #9CA3AF; font-size: 1.05rem; vertical-align: middle; display: inline-block; line-height: 1;'>◆</span>"
                        else:
                            if not has_t1:
                                txt_c2_visuel = f"{txt_c2_brut} &nbsp;<span style='color: #9CA3AF; font-size: 1.05rem; vertical-align: middle; display: inline-block; line-height: 1;'>◆</span>"
                            else:
                                if t2 < t1:
                                    txt_c2_visuel = f"{txt_c2_brut} &nbsp;<span style='color: #22C55E; font-size: 1.25rem; vertical-align: middle; display: inline-block; line-height: 1;'>▲</span>"
                                elif t2 > t1:
                                    txt_c2_visuel = f"{txt_c2_brut} &nbsp;<span style='color: #EF4444; font-size: 1.25rem; vertical-align: middle; display: inline-block; line-height: 1;'>▼</span>"
                                else:
                                    txt_c2_visuel = txt_c2_brut
                        txt_chrono_final = txt_c2_visuel
                    else:
                        # Idem pour la course 1 si elle est active
                        if not has_t1:
                            txt_chrono_final = "No Time"
                        else:
                            txt_chrono_final = txt_c1_visuel

                    html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Groupe']}</td><td>{row['Classe']}</td><td>{txt_c1_visuel}</td><td>{txt_chrono_final}</td></tr>"
                html_hist += "</tbody></table></div>"
                
                # --- CLASSEMENTS COMPLÉMENTAIRES (REGROUPEMENT CLASSEMENTS DROITE : ASAF + RACB) ---
                valides = base[((base["Calc_Sec_1"].notna() & (base["Calc_Sec_1"] > 0)) | (base["Calc_Sec_2"].notna() & (base["Calc_Sec_2"] > 0)))].copy() if "Calc_Sec_1" in base.columns or "Calc_Sec_2" in base.columns else pd.DataFrame()
                df_div4_html = "" # Initialisation du conteneur pour la Division 4

                if len(valides) > 0:
                    cols_calcul = [c for c in ["Calc_Sec_1", "Calc_Sec_2"] if c in valides.columns]
                    valides["Meilleur_Sec"] = valides[cols_calcul].min(axis=1, skipna=True)
                    scr = valides.sort_values(by="Meilleur_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                    
                    # --- TABLEAU 1 DE DROITE (Division 123 ASAF) ---
                    racb = scr.copy()
                    if len(racb) > 0:
                        racb["Pos"] = range(1, len(racb) + 1); racb["Chrono"] = racb["Meilleur_Sec"].apply(format_final_chrono)
                        df_racb_brut = racb[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]].rename(columns={"Classe": "Cl", "Groupe": "Division"})
                        df_racb_brut = df_racb_brut[df_racb_brut["Division"].astype(str).str.strip() != "4"]
                        df_racb = f"<div class='zone-defilement-tactile'>{df_racb_brut.to_html(index=False, classes='table-compacte table-class-robuste', escape=False, border=0)}</div>"
                    
                    # --- TABLEAU 2 DE DROITE (Division 4 ASAF) ---
                    div4_data = scr[scr["Groupe"].astype(str).str.strip() == "4"].copy()
                    if len(div4_data) > 0:
                        div4_data["Pos"] = range(1, len(div4_data) + 1); div4_data["Chrono"] = div4_data["Meilleur_Sec"].apply(format_final_chrono)
                        df_div4_brut = div4_data[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]].rename(columns={"Classe": "Cl", "Groupe": "Division"})
                        df_div4_html = f"<div class='zone-defilement-tactile'>{df_div4_brut.to_html(index=False, classes='table-compacte table-class-robuste', escape=False, border=0)}</div>"
                    else:
                        df_div4_html = f"<table class='table-compacte table-class-groupes'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible pour la Division 4</td></tr></table>"

                    # --- TABLEAU 3 DE DROITE (Top 3 par Classe) ---
                    scr["Cl_Tri_Num"] = scr["Classe"].apply(decomposer_classe_pour_tri)
                    scr["Cl_Tri_Suff"] = scr["Classe"].apply(extraire_suffixe_pour_tri)
                    df_grouped = scr.sort_values(by=["Cl_Tri_Num", "Cl_Tri_Suff", "Groupe", "Meilleur_Sec"]).groupby("Classe", sort=False).head(3).copy()
                    df_grouped = df_grouped.sort_values(by=["Cl_Tri_Num", "Cl_Tri_Suff", "Groupe", "Meilleur_Sec"])
                    if len(df_grouped) > 0:
                        df_grouped["Pos"] = df_grouped.groupby("Classe", sort=False).cumcount() + 1; df_grouped["Chrono"] = df_grouped["Meilleur_Sec"].apply(format_final_chrono)
                        df_divisions = df_grouped[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]].rename(columns={"Classe": "Cl"})
        except Exception as e:
            pass

    if not fichiers_prets:
        html_hist = f"{CSS_RIGIDE_ORIGINE}<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible pour le plateau ASAF</td></tr></table>"
        df_div4_html = f"<table class='table-compacte table-class-groupes'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"

    if not df_divisions.empty:
        html_class_div = f"<table class='table-compacte table-class-groupes'><thead><tr><th>Pos</th><th>N°</th><th>Nom_Prenom</th><th>Groupe</th><th>Cl</th><th>Chrono</th></tr></thead><tbody>"
        for idx in range(len(df_divisions)):
            classe_row = ""
            if idx < len(df_divisions) - 1:
                if str(df_divisions.iloc[idx]["Cl"]) != str(df_divisions.iloc[idx + 1]["Cl"]):
                    classe_row = "class='ligne-separation-classe'"
            html_class_div += f"<tr {classe_row}><td>{df_divisions.iloc[idx]['Pos']}</td><td>{df_divisions.iloc[idx]['N°']}</td><td>{df_divisions.iloc[idx]['Nom_Prenom']}</td><td>{df_divisions.iloc[idx]['Groupe']}</td><td>{df_divisions.iloc[idx]['Cl']}</td><td>{df_divisions.iloc[idx]['Chrono']}</td></tr>"
        html_class_div += "</tbody></table>"
    else:
        html_class_div = f"<table class='table-compacte table-class-groupes'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"

    # L'ordre du return a été modifié pour aligner df_div4_html (2e tableau de droite) et html_class_div (3e tableau de droite)
    return df_live, html_hist, df_racb, df_div4_html, html_class_div, t_live, t_his, t_haut, t_milieu, t_bas
