import streamlit as st
import pandas as pd
import datetime
import requests
import io
import time

# --- CONFIGURATION INTERNET AVEC VOS VRAIS LIENS FONCTIONNELS REPRIS MOT POUR MOT ---
FILE_ARRIVEE = "https://dropboxusercontent.com"
FILE_DEPART  = "https://dropboxusercontent.com"
FILE_ENGAGES = "https://dropboxusercontent.com"

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
    if "Calc_Sec" in row and pd.notna(row["Calc_Sec"]) and row["Calc_Sec"] > 0:
        return format_final_chrono(row["Calc_Sec"])
    if "Heure_Depart" in row and pd.notna(row["Heure_Depart"]) and ("Heure_Arrivee" in row and pd.isna(row["Heure_Arrivee"])):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)
def afficher_ecran_complet():
    st.markdown("""
        <style>
        .titre-live, .titre-hist, .titre-classement {
            color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
            padding: 4px 8px !important; border-radius: 3px !important; margin-bottom: 6px !important;
            width: 100% !important; display: block !important; clear: both !important;
        }
        .titre-live { background-color: #15803D !important; }
        .titre-hist { background-color: #475569 !important; }
        .titre-classement { background-color: #1E3A8A !important; }
        .table-compacte { width: 100% !important; margin-bottom: 0px !important; border-collapse: collapse !important; table-layout: fixed !important; }
        .table-compacte tr { height: 18px !important; }
        .table-compacte th, .table-compacte td { 
            height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; font-size: 0.85rem !important; color: #000000 !important; 
            vertical-align: middle !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; 
        }
        .table-compacte td { border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
        .table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
        .table-hist tr:nth-child(odd) td { background-color: #E0F2FE !important; }
        .table-hist td:last-child, .table-live td:last-child, .table-class-robuste td:last-child { font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }
        .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
        .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
        .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
        .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
        .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
        .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }
        .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; }   
        .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
        .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 22% !important; }  
        .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; }   
        .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 10% !important; }   
        .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }  
        </style>
    """, unsafe_allow_html=True)
    @st.fragment(run_every=30)
    def rafraichir_essais():
        st.cache_data.clear()
        df_live, df_hist = pd.DataFrame(columns=["N°","Nom_Prenom","Voiture","Départ","Arrivée","Chrono réalisé"]), pd.DataFrame(columns=["N°","Nom_Prenom","Voiture","Division","Classe","Chrono réalisé"])
        df_racb, df_asaf123, df_asaf4 = pd.DataFrame(columns=["Pos","N°","Nom_Prenom","Division","Classe","Chrono"]), pd.DataFrame(columns=["Pos","N°","Nom_Prenom","Division","Classe","Chrono"]), pd.DataFrame(columns=["Pos","N°","Nom_Prenom","Division","Classe","Chrono"])
        try:
            df_eng_raw = pd.read_excel(telecharger_excel(FILE_ENGAGES), skiprows=1, engine='openpyxl')
            df_dep_raw = pd.read_excel(telecharger_excel(FILE_DEPART), header=None, engine='openpyxl')
            df_arr_raw = pd.read_excel(telecharger_excel(FILE_ARRIVEE), header=None, engine='openpyxl')
            idx_dep, idx_arr = None, None
            for c_idx in range(len(df_dep_raw.columns)):
                if "ESSAIS" in str(df_dep_raw.iloc[1, c_idx]).strip().upper(): idx_dep = c_idx
            for c_idx in range(len(df_arr_raw.columns)):
                if "ESSAIS" in str(df_arr_raw.iloc[1, c_idx]).strip().upper(): idx_arr = c_idx
            df_dep = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep + 1]}) if idx_dep is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
            df_arr = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr + 3]}) if idx_arr is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])
            df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
            df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(), "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(), "Division": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()), "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})
            df_eng = df_eng[df_eng["N°"] != "NAN"].drop_duplicates(subset=["N°"])
            df_dep = df_dep[(df_dep["N°"] != "NAN") & (df_dep["N°"] != "")]
            for d in [df_dep, df_arr]:
                if len(d) > 0: d["N°"] = d["N°"].astype(str); d["Run_Index"] = d.groupby("N°").cumcount() + 1
            if len(df_dep) > 0: df_dep["Sec_Dep"] = df_dep["Heure_Depart"].apply(convertir_en_secondes)
            if len(df_arr) > 0: df_arr["Sec_Arr"] = df_arr["Heure_Arrivee"].apply(convertir_en_secondes); df_arr["Sec_Excel"] = df_arr["Chrono_Excel"].apply(convertir_en_secondes)
            base_runs = pd.DataFrame(columns=["N°", "Run_Index"])
            if len(df_dep) > 0: base_runs = pd.concat([base_runs, df_dep[["N°", "Run_Index"]]], ignore_index=True)
            if len(base_runs) == 0: base_runs = df_eng[["N°"]].copy(); base_runs["Run_Index"] = 1
            else: base_runs = base_runs.drop_duplicates(subset=["N°", "Run_Index"])
            base = pd.merge(base_runs, df_eng, on="N°", how="inner")
            if len(df_dep) > 0: base = pd.merge(base, df_dep, on=["N°", "Run_Index"], how="left")
            if len(df_arr) > 0: base = pd.merge(base, df_arr, on=["N°", "Run_Index"], how="left")
            if len(base) > 0:
                base["Calc_Sec"] = base["Sec_Excel"].fillna((base["Sec_Arr"] - base["Sec_Dep"]).apply(lambda x: x + 3600 if (x is not None and x < 0) else x))
                if "Heure_Depart" in base.columns and base["Heure_Depart"].notna().any():
                    base_c1 = base[base["Heure_Depart"].notna()].copy(); base_c1["Ordre_Live"] = range(len(base_c1))
                    df_live_base = base_c1.sort_values(by="Ordre_Live", ascending=False).head(5).copy()
                    df_live_base["Chrono réalisé"] = df_live_base.apply(lambda r: calculer_statut_chrono(r, est_dans_le_live=True), axis=1)
                    df_live_base["Arrivée_Brute"] = df_live_base["Heure_Arrivee"].apply(formater_heure_ecran); df_live_base["Départ_Brute"] = df_live_base["Heure_Depart"].apply(formater_heure_ecran)
                    df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_Brute", "Arrivée_Brute", "Chrono réalisé"]].rename(columns={"Départ_Brute": "Départ", "Arrivée_Brute": "Arrivée"})
                base["Chrono_Visual_Hist"] = base.apply(lambda r: "En Piste" if pd.notna(r["Heure_Depart"]) and pd.isna(r["Heure_Arrivee"]) and pd.isna(r["Sec_Excel"]) else format_final_chrono(r["Calc_Sec"]) if pd.notna(r["Calc_Sec"]) and r["Calc_Sec"] > 0 else "No Time", axis=1)
                base["Ordre_Saisie"] = range(len(base))
                df_hist = base.sort_values(by="Ordre_Saisie", ascending=False)[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Chrono_Visual_Hist"]].rename(columns={"Chrono_Visual_Hist": "Chrono réalisé"})
                valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
                if len(valides) > 0:
                    scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy(); scr["Division_Clean"] = scr["Division"].astype(str).str.strip()
                    racb = scr[scr["Division_Clean"].str.upper() == "RACB"].head(20).copy()
                    if len(racb) > 0: racb["Pos"] = range(1, len(racb) + 1); racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono); df_racb = racb[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    asaf123 = scr[scr["Division_Clean"].isin(["1", "2", "3", "1.0", "2.0", "3.0"])].head(25).copy()
                    if len(asaf123) > 0: asaf123["Pos"] = range(1, len(asaf123) + 1); asaf123["Chrono"] = asaf123["Calc_Sec"].apply(format_final_chrono); df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
                    asaf4 = scr[scr["Division_Clean"].isin(["4", "4.0"])].head(10).copy()
                    if len(asaf4) > 0: asaf4["Pos"] = range(1, len(asaf4) + 1); asaf4["Chrono"] = asaf4["Calc_Sec"].apply(format_final_chrono); df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]]
        except Exception: pass

        cg, cd = st.columns([1.3, 0.9])
        with cg:
            st.markdown("<span class='titre-live'>🏎️ EN DIRECT / Derniers concurrents partis</span>", unsafe_allow_html=True)
            st.markdown(generer_tableau_html(df_live, "table-live"), unsafe_allow_html=True)
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-hist'>🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB</span>", unsafe_allow_html=True)
            st.markdown(generer_tableau_html(df_hist, "table-hist"), unsafe_allow_html=True)
        with cd:
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 20)</span>", unsafe_allow_html=True)
            st.markdown(generer_tableau_html(df_racb, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS ASAF DIV 1-2-3 (Top 25)</span>", unsafe_allow_html=True)
            st.markdown(generer_tableau_html(df_asaf123, "table-class-robuste"), unsafe_allow_html=True)
            st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)
            st.markdown("<span class='titre-classement'>🏆 CLASSEMENT EVOLUTIF DES ESSAIS ASAF DIV 4 (Top 10)</span>", unsafe_allow_html=True)
            st.markdown(generer_tableau_html(df_asaf4, "table-class-robuste"), unsafe_allow_html=True)

    rafraichir_essais()
