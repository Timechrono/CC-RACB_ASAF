def recuperer_donnees_course():
    df_live = pd.DataFrame(columns=cols_live)
    df_hist = pd.DataFrame(columns=cols_hist)
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    df_divisions = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"])
    html_hist = "<table class='table-compacte table-hist'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

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
                if nv == "" or nv == "NAN" or nv == "NONE": continue
                if nv not in tous_numeros_autorises_asaf: continue
                    
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
        dict_c3_asaf = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 3", "ASAF")
        dict_c3_racb = extraire_manche_selon_regles_asaf(df_arr_raw, "COURSE 3", "RACB")

        def fusionner_temps_manches(dict_asaf, dict_racb):
            d_fusion = dict_asaf.copy()
            for k, v in dict_racb.items():
                if k not in d_fusion or d_fusion[k]["sec"] is None: d_fusion[k] = v
            return d_fusion

        dict_c1 = fusionner_temps_manches(dict_c1_asaf, dict_c1_racb)
        dict_c2 = fusionner_temps_manches(dict_c2_asaf, dict_c2_racb)
        dict_c3 = fusionner_temps_manches(dict_c3_asaf, dict_c3_racb)
    except Exception: pass
# fin bloc 1
    if not df_eng.empty:
        try:
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
            base = base[base["N°"].isin(tous_numeros_autorises_asaf)].copy()

            if len(base) > 0:
                base["Course_1_Txt"] = base["Calc_Sec_1"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))
                base["Course_2_Txt"] = base["Calc_Sec_2"].apply(lambda x: format_final_chrono(x, fallback_statut="No Time"))

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
                    valides = [(m, i) for i, m in enumerate([t1, t2, t3]) if pd.notna(m) and m > 0]
                    valides.sort(key=lambda x: x[0])
                    indices_meilleurs = [item[1] for item in valides[:2]] if len(valides) >= 2 else [item[1] for item in valides]

                    s1 = "class='meilleur-temps'" if 0 in indices_meilleurs else ""
                    s2 = "class='meilleur-temps'" if 1 in indices_meilleurs else ""
                    s3 = "class='meilleur-temps'" if 2 in indices_meilleurs else ""

                    if pd.notna(row["Heure_Depart_3"]) and pd.isna(row["Heure_Arrivee_3"]): txt_c3_visuel = "En Piste"; s3 = ""
                    elif pd.isna(t3) or t3 <= 0: txt_c3_visuel = "No Time"
                    else:
                        txt_c3 = format_final_chrono(t3); temps_precedents = [t for t in [t1, t2] if pd.notna(t) and t > 0]
                        if temps_precedents:
                            if t3 < min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #22C55E; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▲</span>"
                            elif t3 > min(temps_precedents): txt_c3_visuel = f"{txt_c3} <span style='color: #EF4444; font-size: 1.65rem; line-height: 1; vertical-align: -0.15rem;'>▼</span>"
                            else: txt_c3_visuel = txt_c3
                        else: txt_c3_visuel = txt_c3

                    html_hist += f"<tr><td>{row['N°']}</td><td>{row['Nom_Prenom']}</td><td>{row['Voiture']}</td><td>{row['Division']}</td><td>{row['Classe']}</td><td {s1}>{format_final_chrono(t1)}</td><td {s2}>{format_final_chrono(t2)}</td><td {s3}>{txt_c3_visuel}</td></tr>"
                html_hist += "</tbody></table>"

                def calculer_cumul_deux_meilleurs_pur_python(row):
                    temps = [t for t in [row["Calc_Sec_1"], row["Calc_Sec_2"], row["Calc_Sec_3"]] if pd.notna(t) and t > 0]
                    if len(temps) < 2: return float('inf')
                    temps.sort()
                    return float(sum(temps[:2]))

                base["Cumul_Sec"] = base.apply(calculer_cumul_deux_meilleurs_pur_python, axis=1)
                scr = base[base["Cumul_Sec"] < float('inf')].sort_values(by="Cumul_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                
                if len(scr) > 0:
                    asaf123 = scr[scr["Division"].isin(["1", "2", "3"])].head(25).copy()
                    if len(asaf123) > 0: asaf123["Pos"] = range(1, len(asaf123) + 1); asaf123["Chrono"] = asaf123["Cumul_Sec"].apply(format_final_chrono); df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    asaf4 = scr[scr["Division"] == "4"].head(10).copy()
                    if len(asaf4) > 0: asaf4["Pos"] = range(1, len(asaf4) + 1); asaf4["Chrono"] = asaf4["Cumul_Sec"].apply(format_final_chrono); df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    
                    scr["Classe_Num"] = pd.to_numeric(scr["Classe"], errors='coerce').fillna(999)
                    df_divisions = scr.sort_values(by=["Division", "Classe_Num", "Cumul_Sec"]).groupby(["Division", "Classe_Num"]).head(3).copy()
                    if len(df_divisions) > 0: df_divisions["Pos"] = df_divisions.groupby(["Division", "Classe_Num"]).cumcount() + 1; df_divisions["Chrono"] = df_divisions["Cumul_Sec"].apply(format_final_chrono); df_divisions = df_divisions[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
        except Exception: pass

    # --- TITRES EXTRAITS DIRECTEMENT DE VOTRE CONFIGURATION POUR LA MANCHE 3 ---
    t_live = "🏎️ EN DIRECT / Derniers Concurrents partis"
    t_his = "🕒 HISTORIQUE DES TEMPS / 3ème COURSE / Concurrents ASAF"
    t_haut = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 123 (Top 25)"
    t_milieu = "🏆 CLASSEMENT GENERAL OFFICIEUX Division 4 (Top 10)"
    t_bas = "📊 CLASSEMENT OFFICIEUX par Division / Classe (Top 3)"

    return df_live, html_hist, df_asaf123, df_asaf4, df_divisions, t_live, t_his, t_haut, t_milieu, t_bas
