import streamlit as st
import pandas as pd
import datetime
import requests
import io

# --- PROTOCOLE RÉSEAU INVISIBLE ANTI-RABOTAGE ---
DOMAINE_PROT = "://dropboxusercontent.com"

# Reconstruction sécurisée des adresses
FILE_ARRIVEE = f"https://{DOMAINE_PROT}/scl/fi/7uu9cmlpzglx0ngvbklpt/LIVE_Temps_ARRIVEE.xlsm?rlkey=g9urz4v3jr36h0apzt45ognm6&st=0d9mpgfw&dl=1"
FILE_DEPART  = f"https://{DOMAINE_PROT}/scl/fi/gbkaq01qzjujc8nq3zj28/LIVE_Temps_DEPART.xlsm?rlkey=4x4rvvlfyzz8v59gqbxn80a4d&st=mcibn3xx&dl=1"
FILE_ENGAGES = f"https://{DOMAINE_PROT}/scl/fi/wyof20d4bg4lbmnv0c7m5/LIVE_Liste_ENGAGES_ASAF.xlsm?rlkey=8q59lu88046nxu8mr8gs5ufvc&st=vny281ln&dl=1"

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

def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course 1", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_dep = telecharger_excel(FILE_DEPART)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(flux_dep, header=None, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

        def ext_div(txt):
            if pd.isna(txt) or txt is None: return "-"
            s = str(txt).strip()
            if s.endswith(".0"): s = s[:-2]
            ch = [c for c in s if c.isdigit()]
            return "".join(ch) if ch else s

        df_eng = pd.DataFrame({
            "N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
            "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
            "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
            "Division": df_eng_raw.iloc[:, 5].apply(ext_div),
            "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)
        })
        df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
        df_eng = df_eng[df_eng["Division"].isin(["1", "2", "3", "4"])].copy()
        
        num_123 = set(df_eng[df_eng["Division"].isin(["1", "2", "3"])]["N°"].unique())
        num_4 = set(df_eng[df_eng["Division"] == "4"]["N°"].unique())
        tous_num = num_123.union(num_4)

        def col_titre(df, search):
            for c_idx in range(len(df.columns)):
                if search.upper() in str(df.iloc[1, c_idx]).strip().upper(): return c_idx
            return None

        def ext_manche(df_arr_raw, nom_m, label_cat):
            d_m = {}
            col_dos = col_titre(df_arr_raw, f"{nom_m} {label_cat}")
            if col_dos is None: return d_m
            for r_idx in range(2, len(df_arr_raw)):
                nv = nettoyer_numero(df_arr_raw.iloc[r_idx, col_dos])
                if nv == "" or nv == "NAN" or nv not in tous_num: continue
                s_calc = convertir_en_secondes(df_arr_raw.iloc[r_idx, col_dos + 3])
                d_m[nv] = {"h_dep": df_arr_raw.iloc[r_idx, col_dos + 1], "h_arr": df_arr_raw.iloc[r_idx, col_dos + 2], "sec": s_calc}
            return d_m

        dict_c1_asaf = ext_manche(df_arr_raw, "COURSE 1", "ASAF")
        dict_c1_racb = ext_manche(df_arr_raw, "COURSE 1", "RACB")
        dict_c2_asaf = ext_manche(df_arr_raw, "COURSE 2", "ASAF")
        dict_c2_racb = ext_manche(df_arr_raw, "COURSE 2", "RACB")

        def fusion_m(d_asaf, d_racb):
            d_f = d_asaf.copy()
            for k, v in d_racb.items():
                if k not in d_f or d_f[k]["sec"] is None: d_f[k] = v
            return d_f

        dict_c1 = fusion_m(dict_c1_asaf, dict_c1_racb)
        dict_c2 = fusion_m(dict_c2_asaf, dict_c2_racb)
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
        base = base[base["N°"].isin(tous_num)].copy()

        if len(base) > 0:
            base["Course_1_Txt"] = base["Calc_Sec_1"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))

            # LIVE MODE
            if "Heure_Depart_2" in base.columns and base["Heure_Depart_2"].notna().any():
                base_c2 = base[base["Heure_Depart_2"].notna()].copy()
                def cal_st_live(r):
                    if pd.notna(r["Calc_Sec_2"]) and r["Calc_Sec_2"] > 0: return format_final_chrono(r["Calc_Sec_2"])
                    if pd.notna(r["Heure_Depart_2"]) and pd.isna(r["Heure_Arrivee_2"]): return "<span class='vrai-gyrophare'>🚨</span> EN PISTE"
                    return "No Time"
                base_c2["Chrono réalisé"] = base_c2.apply(cal_st_live, axis=1)
                base_c2["Départ"] = base_c2["Heure_Depart_2"].apply(formater_heure_ecran)
                base_c2["Arrivée"] = base_c2["Heure_Arrivee_2"].apply(formater_heure_ecran)
                df_live = base_c2.sort_values(by="Heure_Depart_2", ascending=False).head(5)[["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]]

            # HISTORIQUE MODE WITH DELTA FLÈCHES
            df_hist_base = base[base["Calc_Sec_1"].notna() | base["Calc_Sec_2"].notna()].copy()
            df_hist_base = df_hist_base.sort_values(by="Heure_Depart_2", ascending=False, na_position="last")
            def cal_st_hist(r):
                t2 = r["Calc_Sec_2"]; t1 = r["Calc_Sec_1"]
                if pd.notna(r["Heure_Depart_2"]) and pd.isna(r["Heure_Arrivee_2"]): return "En Piste"
                if pd.isna(t2) or t2 <= 0: return "No Time"
                txt_c2 = format_final_chrono(t2)
                if pd.notna(t1) and t1 > 0 and pd.notna(t2) and t2 > 0:
                    if t2 < t1: return f"{txt_c2} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                    elif t2 > t1: return f"{txt_c2} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                return txt_c2
            df_hist_base["Chrono réalisé"] = df_hist_base.apply(cal_st_hist, axis=1)
            df_hist = df_hist_base[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Course_1_Txt", "Chrono réalisé"]].rename(columns={"Course_1_Txt": "Course 1"})

            # GENERAL CUMULATIVE CLASSEMENTS
            val_cum = base[(base["Calc_Sec_1"].notna() & (base["Calc_Sec_1"] > 0)) & (base["Calc_Sec_2"].notna() & (base["Calc_Sec_2"] > 0))].copy()
            if len(val_cum) > 0:
                val_cum["Cumul_Sec"] = val_cum["Calc_Sec_1"] + val_cum["Calc_Sec_2"]
                scr = val_cum.sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                
                asaf123 = scr[scr["N°"].isin(num_123)].head(25).copy()
                if len(asaf123) > 0:
                    asaf123["Pos"] = range(1, len(asaf123) + 1)
                    asaf123["Chrono"] = asaf123["Cumul_Sec"].apply(format_final_chrono)
                    df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                
                asaf4 = scr[scr["N°"].isin(num_4)].head(10).copy()
                if len(asaf4) > 0:
                    asaf4["Pos"] = range(1, len(asaf4) + 1)
                    asaf4["Chrono"] = asaf4["Cumul_Sec"].apply(format_final_chrono)
                    df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                
                scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                df_grouped = scr.sort_values(by=["Division", "Classe_Num", "Cumul_Sec"]).groupby(["Division", "Classe_Num"]).head(3).copy()
                if len(df_grouped) > 0:
                    df_grouped["Pos"] = df_grouped.groupby(["Division", "Classe_Num"]).cumcount() + 1
                    df_grouped["Chrono"] = df_grouped["Cumul_Sec"].apply(format_final_chrono)
                    df_divisions = df_grouped[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
    except Exception: pass

    return df_live, df_hist, df_asaf123, df_asaf4, df_divisions
