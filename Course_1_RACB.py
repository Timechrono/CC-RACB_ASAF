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

def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_dep = telecharger_excel(FILE_DEPART)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(flux_dep, header=None, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

        idx_dep_1, idx_arr_1 = None, None
        for c_idx in range(len(df_dep_raw.columns)):
            val = str(df_dep_raw.iloc[1, c_idx]).strip().upper()
            if "COURSE 1 RACB" in val: idx_dep_1 = c_idx
        for c_idx in range(len(df_arr_raw.columns)):
            val = str(df_arr_raw.iloc[1, c_idx]).strip().upper()
            if "COURSE 1 RACB" in val: idx_arr_1 = c_idx

        df_dep = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_1].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_1 + 1]}) if idx_dep_1 is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
        df_arr = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_1].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_1 + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_1 + 3]}) if idx_arr_1 is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
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

def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    cols_hist = ["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_dep = telecharger_excel(FILE_DEPART)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(flux_dep, header=None, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

        idx_dep_1, idx_arr_1 = None, None
        for c_idx in range(len(df_dep_raw.columns)):
            val = str(df_dep_raw.iloc[1, c_idx]).strip().upper()
            if "COURSE 1 RACB" in val: idx_dep_1 = c_idx
        for c_idx in range(len(df_arr_raw.columns)):
            val = str(df_arr_raw.iloc[1, c_idx]).strip().upper()
            if "COURSE 1 RACB" in val: idx_arr_1 = c_idx

        df_dep = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_1].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep_1 + 1]}) if idx_dep_1 is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
        df_arr = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_1].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr_1 + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr_1 + 3]}) if idx_arr_1 is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
        df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
        df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                               "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                               "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                               "Groupe": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                               "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})

        df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
        df_dep = df_dep[(df_dep["N°"] != "NAN") & (df_dep["N°"] != "")]

        for d in [df_dep, df_arr]:
            if len(d) > 0:
                d["N°"] = d["N°"].astype(str)
                d["Run_Index"] = d.groupby("N°").cumcount() + 1

        if len(df_dep) > 0: df_dep["Sec_Dep"] = df_dep["Heure_Depart"].apply(convertir_en_secondes)
        if len(df_arr) > 0: df_arr["Sec_Arr"] = df_arr["Heure_Arrivee"].apply(convertir_en_secondes)
        if len(df_arr) > 0: df_arr["Sec_Excel"] = df_arr["Chrono_Excel"].apply(convertir_en_secondes)

        base_runs = pd.DataFrame(columns=["N°", "Run_Index"])
        if len(df_dep) > 0: base_runs = pd.concat([base_runs, df_dep[["N°", "Run_Index"]]], ignore_index=True)
        if len(base_runs) == 0:
            base_runs = df_eng[["N°"]].copy(); base_runs["Run_Index"] = 1
        else:
            base_runs = base_runs.drop_duplicates(subset=["N°", "Run_Index"])

        base = pd.merge(base_runs, df_eng, on="N°", how="inner")
        if len(df_dep) > 0: base = pd.merge(base, df_dep, on=["N°", "Run_Index"], how="left")
        if len(df_arr) > 0: base = pd.merge(base, df_arr, on=["N°", "Run_Index"], how="left")
        
        if len(base) > 0:
            base["Calc_Sec"] = base["Sec_Excel"].fillna((base["Sec_Arr"] - base["Sec_Dep"]).apply(lambda x: x + 3600 if (x is not None and x < 0) else x))
            base["Départ_C1"] = base["Heure_Depart"].apply(formater_heure_ecran)

            if "Heure_Depart" in base.columns and base["Heure_Depart"].notna().any():
                base_c1 = base[base["Heure_Depart"].notna()].copy()
                base_c1["Ordre_Live"] = range(len(base_c1))
                df_live_base = base_c1.sort_values(by="Ordre_Live", ascending=False).head(5).copy()
                df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                df_live_base["Arrivée_Brute"] = df_live_base["Heure_Arrivee"].apply(formater_heure_ecran)
                df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_C1", "Arrivée_Brute", "Chrono réalisé"]].rename(columns={"Départ_C1": "Départ", "Arrivée_Brute": "Arrivée"})

            base["Chrono_C1_Visual_Hist"] = base.apply(lambda r: "En Piste" if pd.notna(r["Heure_Depart"]) and pd.isna(r["Heure_Arrivee"]) and pd.isna(r["Sec_Excel"]) else format_final_chrono(r["Calc_Sec"]) if pd.notna(r["Calc_Sec"]) and r["Calc_Sec"] > 0 else "No Time", axis=1)
            base["Ordre_Saisie"] = range(len(base))
            df_hist = base.sort_values(by="Ordre_Saisie", ascending=False)[["N°", "Nom_Prenom", "Voiture", "Groupe", "Classe", "Chrono_C1_Visual_Hist"]].rename(columns={"Chrono_C1_Visual_Hist": "Chrono réalisé"})

            valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
            if len(valides) > 0:
                scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                scr = scr[~scr["Groupe"].astype(str).str.strip().str.startswith(('1', '2', '3', '4'), na=False)]
                
                racb = scr.head(30).copy()
                if len(racb) > 0:
                    racb["Pos"] = range(1, len(racb) + 1)
                    racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                    df_racb = racb[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
                
                scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                df_grouped = scr.sort_values(by=["Groupe", "Classe_Num", "Calc_Sec"]).groupby(["Groupe", "Classe_Num"]).head(3).copy()
                if len(df_grouped) > 0:
                    df_grouped["Pos"] = df_grouped.groupby(["Groupe", "Classe_Num"]).cumcount() + 1
                    df_grouped["Chrono"] = df_grouped["Calc_Sec"].apply(format_final_chrono)
                    df_divisions = df_grouped[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
    except Exception: pass

    return df_live, df_hist, df_racb, df_divisions
