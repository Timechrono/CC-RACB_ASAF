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

def calculer_statut_chrono(row, est_dans_le_live=True):
    if "Calc_Sec_2" in row and pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0:
        return format_final_chrono(row["Calc_Sec_2"])
    if "Heure_Depart_2" in row and pd.notna(row["Heure_Depart_2"]) and pd.isna(row.get("Heure_Arrivee_2")):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"
def recuperer_donnees_course():
    cols_live = ["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono réalisé"]
    df_live = pd.DataFrame(columns=cols_live)
    html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"])

    data_engages = telecharger_excel(FILE_ENGAGES_RACB)
    data_depart = telecharger_excel(FILE_DEPART)
    data_arrivee = telecharger_excel(FILE_ARRIVEE)

    if data_engages and data_depart and data_arrivee:
        try:
            df_eng_raw = pd.read_excel(data_engages, header=1, engine='openpyxl')
            df_dep_raw = pd.read_excel(data_depart, header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(data_arrivee, header=None, engine='openpyxl')

            idx_dep_1, idx_arr_1 = None, None
            idx_dep_2, idx_arr_2 = None, None
            
            for c_idx in range(len(df_dep_raw.columns)):
                val = str(df_dep_raw.iloc[1, c_idx]).strip().upper()
                if "COURSE 1 RACB" in val: idx_dep_1 = c_idx
                elif "COURSE 2 RACB" in val: idx_dep_2 = c_idx
            for c_idx in range(len(df_arr_raw.columns)):
                val = str(df_arr_raw.iloc[1, c_idx]).strip().upper()
                if "COURSE 1 RACB" in val: idx_arr_1 = c_idx
                elif "COURSE 2 RACB" in val: idx_arr_2 = c_idx

            df_dep2 = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_2].apply(nettoyer_numero), "Heure_Depart_2": df_dep_raw.iloc[2:, idx_dep_2 + 1]}) if idx_dep_2 is not None else pd.DataFrame(columns=["N°", "Heure_Depart_2"])
            df_arr2 = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_2].apply(nettoyer_numero), "Heure_Arrivee_2": df_arr_raw.iloc[2:, idx_arr_2 + 2]}) if idx_arr_2 is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee_2"])
            df_dep1 = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep_1].apply(nettoyer_numero), "Heure_Depart_1": df_dep_raw.iloc[2:, idx_dep_1 + 1]}) if idx_dep_1 is not None else pd.DataFrame(columns=["N°", "Heure_Depart_1"])
            df_arr1 = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr_1].apply(nettoyer_numero), "Heure_Arrivee_1": df_arr_raw.iloc[2:, idx_arr_1 + 2]}) if idx_arr_1 is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee_1"])

            df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
            df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                                   "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                                   "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                                   "Groupe": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                                   "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])

            df_dep1 = df_dep1[(df_dep1["N°"] != "NAN") & (df_dep1["N°"] != "")]
            df_dep2 = df_dep2[(df_dep2["N°"] != "NAN") & (df_dep2["N°"] != "")]

            for d in [df_dep1, df_arr1, df_dep2, df_arr2]:
                if len(d) > 0:
                    d["N°"] = d["N°"].astype(str)
                    d["Run_Index"] = d.groupby("N°").cumcount() + 1

            if len(df_dep1) > 0: df_dep1["Sec_Dep_1"] = df_dep1["Heure_Depart_1"].apply(convertir_en_secondes)
            if len(df_arr1) > 0: df_arr1["Sec_Arr_1"] = df_arr1["Heure_Arrivee_1"].apply(convertir_en_secondes)
            if len(df_dep2) > 0: df_dep2["Sec_Dep_2"] = df_dep2["Heure_Depart_2"].apply(convertir_en_secondes)
            if len(df_arr2) > 0: df_arr2["Sec_Arr_2"] = df_arr2["Heure_Arrivee_2"].apply(convertir_en_secondes)

            base_runs = pd.DataFrame(columns=["N°", "Run_Index"])
            for d in [df_dep1, df_dep2]:
                if len(d) > 0: base_runs = pd.concat([base_runs, d[["N°", "Run_Index"]]], ignore_index=True)
            base_runs = df_eng[["N°"]].copy() if len(base_runs) == 0 else base_runs.drop_duplicates(subset=["N°", "Run_Index"])

            base = pd.merge(base_runs, df_eng, on="N°", how="inner")
            if len(df_dep1) > 0: base = pd.merge(base, df_dep1, on=["N°", "Run_Index"], how="left")
            if len(df_arr1) > 0: base = pd.merge(base, df_arr1, on=["N°", "Run_Index"], how="left")
            if len(df_dep2) > 0: base = pd.merge(base, df_dep2, on=["N°", "Run_Index"], how="left")
            if len(df_arr2) > 0: base = pd.merge(base, df_arr2, on=["N°", "Run_Index"], how="left")

            if len(base) > 0:
                base["Calc_Sec_1"] = (base["Sec_Arr_1"] - base["Sec_Dep_1"]).apply(lambda x: x + 3600 if (x is not None and x < 0) else x)
                base["Calc_Sec_2"] = (base["Sec_Arr_2"] - base["Sec_Dep_2"]).apply(lambda x: x + 3600 if (x is not None and x < 0) else x)

                if "Heure_Depart_2" in base.columns and base["Heure_Depart_2"].notna().any():
                    base_c2 = base[base["Heure_Depart_2"].notna()].copy()
                    base_c2["Ordre_Live"] = range(len(base_c2))
                    df_live_base = base_c2.sort_values(by="Ordre_Live", ascending=False).head(5).copy()
                    df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                    df_live_base["Départ_C2"] = df_live_base["Heure_Depart_2"].apply(formater_heure_ecran)
                    df_live_base["Arrivée_C2"] = df_live_base["Heure_Arrivee_2"].apply(formater_heure_ecran)
                    df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_C2", "Arrivée_C2", "Chrono réalisé"]].rename(columns={"Départ_C2": "Départ", "Arrivée_C2": "Arrivée"})

                df_hist_base = base.sort_values(by="Run_Index", ascending=False).copy()
                
                # RE-INJECTION DES LARGEURS DE LA C2 DANS L'HISTORIQUE HTML
                html_hist = CSS_RACB + "<table class='table-compacte table-hist'><thead><tr><th>N°</th><th>Nom_Prenom</th><th>Voiture</th><th>Groupe</th><th>Classe</th><th>Course 1</th><th>Chrono réalisé</th></tr></thead><tbody>"

                for idx, row in df_hist_base.iterrows():
                    t1, t2 = row["Calc_Sec_1"], row["Calc_Sec_2"]
                    valeurs_valides = [v for v in [t1, t2] if pd.notna(v) and v > 0]
                    meilleur_sec = min(valeurs_valides) if valeurs_valides else None

                    s1 = "class='meilleur-temps'" if (meilleur_sec and t1 == meilleur_sec) else ""
                    s2 = "class='meilleur-temps'" if (meilleur_sec and t2 == meilleur_sec) else ""

                    if pd.notna(row["Heure_Depart_2"]) and pd.isna(row["Heure_Arrivee_2"]):
                        txt_c2_visuel, s2 = "En Piste", ""
                    elif pd.isna(t2) or t2 <= 0:
                        txt_c2_visuel = "No Time"
                    else:
                        txt_c2 = format_final_chrono(t2)
                        if pd.notna(t1) and t1 > 0:
                            if t2 < t1: txt_c2_visuel = f"{txt_c2} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                            elif t2 > t1: txt_c2_visuel = f"{txt_c2} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                            else: txt_c2_visuel = txt_c2
                        else: txt_c2_visuel = txt_c2

                    html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Groupe']}</td><td>{row['Classe']}</td><td {s1}>{format_final_chrono(t1)}</td><td {s2}>{txt_c2_visuel}</td></tr>"
                html_hist += "</tbody></table>"

                valides = base[((base["Calc_Sec_1"].notna() & (base["Calc_Sec_1"] > 0)) | (base["Calc_Sec_2"].notna() & (base["Calc_Sec_2"] > 0)))].copy()
                if len(valides) > 0:
                    valides["Meilleur_Sec"] = valides[["Calc_Sec_1", "Calc_Sec_2"]].min(axis=1, skipna=True)
                    scr = valides.sort_values(by="Meilleur_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                    racb = scr.head(30).copy()
                    if len(racb) > 0:
                        racb["Pos"] = range(1, len(racb) + 1)
                        racb["Chrono"] = racb["Meilleur_Sec"].apply(format_final_chrono)
                        df_racb = racb[["Pos", "N°", "Nom_Prenom", "Groupe", "Classe", "Chrono"]]
        except Exception: pass

    return df_live, html_hist, df_racb, pd.DataFrame(), pd.DataFrame(), "🏎️ EN DIRECT / Derniers concurrents partis", "🕒 HISTORIQUE DES TEMPS / 2ème COURSE / Concurrents RACB", "🏆 CLASSEMENT EVOLUTIF OFFICIEUX RACB (Top 30)", "", ""
