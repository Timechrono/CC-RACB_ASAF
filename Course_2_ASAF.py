import streamlit as st
import pandas as pd
import datetime
import requests
import io

# ==============================================================================
# ⚙️ CONFIGURATION DES HAUTEURS VISUELLES SUR PC (en pixels)
# ==============================================================================
HAUTEURS_TABLEAUX_PC = {
    "HISTORIQUE": "487px",       # ⬅️ Colonne de gauche (Historique des temps)
    "RACB": "213px",             # ➡️ Haut de la colonne droite (Classement Général RACB)
    "ASAF_123": "147px",         # ➡️ Milieu de la colonne droite (Classement par Groupe / Classe)
    "ASAF_4": "215px"              # ➡️ Bas de la colonne droite (0px car inutilisé sur cette feuille)
}

# --- ENCODAGE NUMÉRIQUE INTERNE ANTI-CENSURE ---
C = [100, 108, 46, 100, 114, 111, 112, 98, 111, 120, 117, 115, 101, 114]
D = [99, 111, 110, 116, 101, 110, 116, 46, 99, 111, 109]
HOTE_PROT = "".join(chr(x) for x in (C + D))

# Adresses internet assemblées
FILE_ARRIVEE = f"https://{HOTE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_DEPART  = f"https://{HOTE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&st=mcibn3xx&dl=1"

# Les deux adresses d'engagés distinctes intégrées
FILE_ENGAGES_ASAF = f"https://{HOTE_PROT}/scl/fi/wyof20d4bg4lbmnv0c7m5/LIVE_Liste_ENGAGES_ASAF.xlsm?rlkey=8q59lu88046nxu8mr8gs5ufvc&st=vny281ln&dl=1"
FILE_ENGAGES_RACB = f"https://{HOTE_PROT}/scl/fi/69zkwsb45bpiw3ys3kk4c/LIVE_Liste_ENGAGES_RACB.xlsm?rlkey=qpjrlmbxhcskifnabs84veqh8&st=0snuv3e7&dl=1"

# Injection globale des styles CSS standards
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
    .table-class-robuste tr:nth-child(odd) td { background-color: #E0F2FE !important; }
    </style>
""", unsafe_allow_html=True)
@st.cache_data(ttl=30)
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
    if "Calc_Sec" in row and pd.notna(row["ANALOG_Sec" if "ANALOG_Sec" in row else "Calc_Sec"]) and row["Calc_Sec"] > 0:
        temps_formate = format_final_chrono(row["Calc_Sec"])
        if est_dans_le_live:
            if row["Calc_Sec"] > 240:
                coche = "<span style='color: #DC2626; font-weight: bold;'>✔</span>"
            else:
                coche = "<span style='color: #16A34A; font-weight: bold;'>✔</span>"
            return f"{temps_formate}&nbsp;&nbsp;&nbsp;{coche}"
        return temps_formate
    if "Heure_Depart" in row and pd.notna(row["Heure_Depart"]) and ("Heure_Arrivee" in row and pd.isna(row["Heure_Arrivee"])):
        return "<span class='vrai-gyrophare'>🟠</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def extraire_engages(flux):
    df_raw = pd.read_excel(flux, engine='openpyxl')
    df_raw.columns = df_raw.columns.astype(str).str.strip().str.upper()
    df_clean = pd.DataFrame({
        "N°": df_raw.iloc[:, 0].apply(nettoyer_numero), 
        "Nom_Prenom": df_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
        "Voiture": df_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
        "Division": df_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
        "Classe": df_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
    })
    return df_clean[df_clean["N°"] != "NAN"]
        # 1. Extraction des Départs ASAF et RACB (Ordre naturel du fichier)
        d_asaf = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_asaf].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_asaf + 1]}) if idx_dep_asaf is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
        d_asaf = d_asaf[d_asaf["N°"].isin(liste_numeros_asaf)].copy()
        
        d_racb = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_racb].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_racb + 1]}) if idx_dep_racb is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
        d_racb = d_racb[d_racb["N°"].isin(liste_numeros_asaf)].copy()

        df_dep = pd.concat([d_asaf, d_racb])
        df_dep = df_dep[(df_dep["N°"] != "NAN") & (df_dep["N°"] != "")]
        
        # On calcule l'index de passage (Run 1, Run 2) sur l'ordre chronologique réel
        df_dep["Run_Index"] = df_dep.groupby("N°").cumcount() + 1

        # 2. Extraction des Arrivées
        a_asaf = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_asaf].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_asaf + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_asaf + 3]}) if idx_arr_asaf is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
        a_asaf = a_asaf[a_asaf["N°"].isin(liste_numeros_asaf)]

        a_racb = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_racb].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_racb + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_racb + 3]}) if idx_arr_racb is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
        a_racb = a_racb[a_racb["N°"].isin(liste_numeros_asaf)]

        df_arr = pd.concat([a_asaf, a_racb]).drop_duplicates(subset=["N°", "Heure_Arrivee"])
        if len(df_arr) > 0:
            df_arr["N°"] = df_arr["N°"].astype(str)
            df_arr["Run_Index"] = df_arr.groupby("N°").cumcount() + 1

        if len(df_dep) > 0: df_dep["Sec_Dep"] = df_dep["Heure_Depart"].apply(convertir_en_secondes)
        if len(df_arr) > 0:
            df_arr["Sec_Arr"] = df_arr["Heure_Arrivee"].apply(convertir_en_secondes)
            df_arr["Sec_Excel"] = df_arr["Chrono_Excel"].apply(convertir_en_secondes)

        # Assemblage final
        base = pd.merge(df_dep[["N°", "Run_Index", "Heure_Depart", "Sec_Dep"]], df_eng, on="N°", how="inner") if len(df_dep) > 0 else pd.DataFrame()
        if len(base) > 0 and len(df_arr) > 0:
            base = pd.merge(base, df_arr, on=["N°", "Run_Index"], how="left")
        
        if len(base) > 0:
            base["Calc_Sec"] = base["Sec_Excel"].fillna((base["Sec_Arr"] - base["Sec_Dep"]).apply(lambda x: x + 3600 if (x is not None and not pd.isna(x) and x < 0) else x))
            base["Départ_C1"] = base["Heure_Depart"].apply(formater_heure_ecran)

            # --- LA CLÉ DE L'AFFICHAGE REPRÉNSENTATIF ---
            # On trie TOUT le tableau par l'heure de départ numérique décroissante (le plus récent en haut)
            # Cela garantit que les couples départ/arrivée restent soudés, mais l'affichage s'empile correctement.
            base_affichage = base.sort_values(by="Sec_Dep", ascending=False)

            # 🏎️ SECTION EN DIRECT (Les 5 premiers de la liste affichée)
            df_live_base = base_affichage.head(5).copy()
            df_live_base["Chrono"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
            df_live_base["Arrivée_Brute"] = df_live_base["Heure_Arrivee"].apply(formater_heure_ecran)
            df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_C1", "Arrivée_Brute", "Chrono"]].rename(columns={"Départ_C1": "Départ", "Arrivée_Brute": "Arrivée"})

            # 🕒 SECTION HISTORIQUE (Le reste de la liste, préservant l'ordre chronologique inverse)
            base_historique = base_affichage.iloc[5:].copy()
            base_historique["Chrono_C1_Visual_Hist"] = base_historique.apply(lambda r: "En Piste" if pd.notna(r["Heure_Depart"]) and pd.isna(r["Heure_Arrivee"]) and pd.isna(r["Sec_Excel"]) else format_final_chrono(r["Calc_Sec"]) if pd.notna(r["Calc_Sec"]) and r["Calc_Sec"] > 0 else "No Time", axis=1)
            df_hist = base_historique[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Chrono_C1_Visual_Hist"]].rename(columns={"Chrono_C1_Visual_Hist": "Chrono", "Division": "Division", "Classe": "Cl"})
            # Traitement inchangé des classements officieux
            valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
            if len(valides) > 0:
                scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                scr["Division_Clean"] = scr["Division"].astype(str).str.strip()
                
                asaf123 = scr[scr["Division_Clean"].isin(["1", "2", "3", "1.0", "2.0", "3.0"])].copy()
                if len(asaf123) > 0:
                    asaf123["Pos"] = range(1, len(asaf123) + 1)
                    asaf123["Chrono"] = asaf123["Calc_Sec"].apply(format_final_chrono)
                    df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Division", "Classe": "Cl"})
                
                asaf4 = scr[scr["Division_Clean"].isin(["4", "4.0"])].copy()
                if len(asaf4) > 0:
                    asaf4["Pos"] = range(1, len(asaf4) + 1)
                    asaf4["Chrono"] = asaf4["Calc_Sec"].apply(format_final_chrono)
                    df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Division", "Classe": "Cl"})

                scr_div_filtree = scr[scr["Division_Clean"].isin(["1", "2", "3", "4", "1.0", "2.0", "3.0", "4.0"])].copy()
                if len(scr_div_filtree) > 0:
                    scr_div_filtree["Classe_Num"] = pd.to_numeric(scr_div_filtree["Classe"], errors='coerce').fillna(999)
                    
                    df_grouped = scr_div_filtree.sort_values(by=["Division_Clean", "Classe_Num", "Calc_Sec"])
                    df_grouped = df_grouped.groupby(["Division_Clean", "Classe_Num"]).head(3).copy()
                    
                    if len(df_grouped) > 0:
                        html_blocs = []
                        html_blocs.append("<table class='table-compacte'><thead><tr><th>Pos</th><th>N°</th><th>Nom_Prenom</th><th>Division</th><th>Cl</th><th>Chrono</th></tr></thead><tbody>")
                        
                        liste_lignes = []
                        for (div, cl_num), group in df_grouped.groupby(["Division_Clean", "Classe_Num"], sort=False):
                            group = group.copy()
                            group["Pos"] = range(1, len(group) + 1)
                            group["Chrono"] = group["Calc_Sec"].apply(format_final_chrono)
                            sub_df = group[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Division", "Classe": "Cl"})
                            for _, r_data in sub_df.iterrows():
                                liste_lignes.append((r_data, cl_num))

                        caractere_trait_plat = "\u25AC" * 160
                        separateur_bleu = f"<span style='color: #1E3A8A; font-size: 4px !important; line-height: 4px !important; display: block !important;'>{caractere_trait_plat}</span>"

                        for i in range(len(liste_lignes)):
                            r_data, cl_actuelle = liste_lignes[i]
                            
                            if i > 0:
                                _, cl_precedente = liste_lignes[i - 1]
                                if cl_actuelle != cl_precedente:
                                    html_blocs.append(f"<tr><td colspan='6' style='padding: 0px !important; margin: 0px !important; line-height: 4px !important; height: 4px !important; font-size: 4px !important; background-color: #FFFFFF !important;'>{separateur_bleu}</td></tr>")
                            
                            html_blocs.append("<tr>")
                            for cell in r_data:
                                html_blocs.append(f"<td>{cell}</td>")
                            html_blocs.append("</tr>")
                            
                        html_blocs.append("</tbody></table>")
                        html_divisions = "".join(html_blocs)
    except Exception: pass

    t_live = "🏎️ EN DIRECT / Derniers Concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 2ème Course / Concurrents ASAF<span>↕️</span>"
    t_haut = "🏆 CLASSEMENT EVOLUTIF OFFICIEUX Division 123<span>↕️</span>"
    t_milieu = "🏆 CLASSEMENT EVOLUTIF OFFICIEUX Division 4<span>↕️</span>"
    t_bas = "🏆 CLASSEMENT EVOLUTIF OFFICIEUX PAR Div/Cl (Top 3)<span>↕️</span>"

    return df_live, df_hist, df_asaf123, df_asaf4, html_divisions, t_live, t_his, t_haut, t_milieu, t_bas
