# https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1
import streamlit as st
import pandas as pd
import time
import requests
import io
import Essais

# ==============================================================================
# ⚠️ METTEZ VOTRE LIEN DROPBOX ICI (Assurez-vous qu'il se termine bien par dl=1)
# ==============================================================================
LIEN_DROPBOX_LOGO = "https://www.dropbox.com/scl/fi/hi24fjo0vbal4oiiwt9jl/logo-TimeC.png?rlkey=xlw0oqk9gdnq6v5dgahi0klg0&st=y86yrn6y&dl=1"

# --- DÉTECTION DES SCRIPTS DE COURSE DISPONIBLES ---
try:
    import Course_1_ASAF
    course1_disponible = True
except ModuleNotFoundError:
    course1_disponible = False

try:
    import Course_2_ASAF
    course2_disponible = True
except ModuleNotFoundError:
    course2_disponible = False

try:
    import Course_3_ASAF
    course3_disponible = True
except ModuleNotFoundError:
    course3_disponible = False

try:
    import Course_1_RACB
    course1_racb_disponible = True
except ModuleNotFoundError:
    course1_racb_disponible = False

try:
    import Course_2_RACB
    course2_racb_disponible = True
except ModuleNotFoundError:
    course2_racb_disponible = False

try:
    import Course_3_RACB
    course3_racb_disponible = True
except ModuleNotFoundError:
    course3_racb_disponible = False

st.set_page_config(page_title="Live", layout="wide")

# --- CONCEPTION GRAPHIQUE GÉOMÉTRIQUE UNIFIÉE ---
st.markdown(f"""
<style>
[data-testid="stHeader"] {{ display: none !important; }}
button:focus, div:focus, input:focus, select:focus {{
    outline: none !important; border-color: transparent !important; box-shadow: none !important;
}}
.block-container {{ 
    padding-top: 5px !important; 
    padding-bottom: 0rem !important; 
    padding-left: 0.5rem !important; 
    padding-right: 0.5rem !important; 
}}
div[data-testid="stMainBlockContainer"] {{
    padding-top: 5px !important;
    margin-top: 0px !important;
}}
div[data-testid="stVerticalBlock"] {{
    gap: 0rem !important;
    padding-top: 0px !important;
}}
div.stElementContainer {{
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}}
.titre-live, .titre-hist, .titre-classement {{
    color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: bold !important;
    padding: 4px 8px !important; border-radius: 3px !important;
    width: 100% !important; display: block !important; clear: both !important;
}}
.titre-live {{ background-color: #15803D !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

/* AJUSTEMENT DU BLOC TITRE : Remplacé en bloc physique pour éviter le chevauchement */
.titre-hist {{ background-color: #475569 !important; margin-top: 25px !important; margin-bottom: 8px !important; }}

.titre-classement {{ background-color: #1E3A8A !important; margin-top: 0px !important; margin-bottom: 6px !important; }}

/* Style en gras sur la dernière colonne de l'historique */
.table-hist td:last-child {{ 
    font-weight: bold !important; 
    color: #0F172A !important; 
}}

/* Cadre vert très foncé, texte BLANC et NON GRAS */
.refresh-bleu-clair-historique {{
    color: #FFFFFF !important;
    font-weight: normal !important;
    background-color: #064E3B !important;
    border: 1px solid #00FF00 !important;
    padding: 1px 6px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-left: 4px !important;
}}

.espace-classement-suivant {{
    margin-top: 25px !important;
}}

.table-responsive-container {{
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin-bottom: 10px !important;
}}

.table-compacte {{
    width: 100% !important; margin-bottom: 0px !important;
    border-collapse: collapse !important; table-layout: auto !important;
}}
.table-compacte tr {{ height: 18px !important; }}
.table-compacte th, .table-compacte td {{ 
    height: 18px !important; padding: 1px 5px !important; line-height: 1.1 !important; 
    font-size: 0.85rem !important; color: #000000 !important; vertical-align: middle !important; 
    white-space: nowrap !important; 
}}
.table-compacte td {{ border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }}
.table-compacte th {{ font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }}
.table-live td:last-child, .table-class-robuste td:last-child {{ font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important; }}
.table-hist tr:nth-child(odd) td {{ background-color: #E0F2FE !important; }}

/* Signature alignée en bleu foncé avec pointillés assortis */
.signature-fin-page {{
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 12px !important;
    text-align: center !important;
    color: #1E3A8A !important;
    font-size: 0.92rem !important;
    font-weight: bold !important;
    padding-top: 8px !important;
    margin-top: 35px !important;
    border-top: 1px dashed #1E3A8A !important;
    width: 100% !important;
}}

.logo-signature {{
    height: 42px !important;
    width: auto !important;
    vertical-align: middle !important;
}}

@media (max-width: 768px) {{
    .block-container {{ padding-left: 2px !important; padding-right: 2px !important; }}
    .titre-live, .titre-hist, .titre-classement {{ font-size: 0.85rem !important; padding: 3px 6px !important; }}
    .table-compacte th, .table-compacte td {{ font-size: 0.65rem !important; padding: 1px 2px !important; }}
    
    /* OPTIMISATION OPTIQUE : Limite la colonne Gr/Div ou Groupe à 4 caractères max sur smartphone */
    .table-hist td:nth-child(4) {{
        max-width: 32px !important;
        overflow: hidden !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
    }}
    
    .table-live td:last-child, .table-class-robuste td:last-child {{ font-size: 0.70rem !important; }}
    .signature-fin-page {{ font-size: 0.75rem !important; padding-top: 4px !important; }}
    .logo-signature {{ height: 32px !important; }}
}}

/* Force la ligne bleue sur le BAS des cellules */
.table-class-robuste tr.ligne-bleue-separation td {{
    box-shadow: inset 0 -3px 0 0 #1E3A8A !important;
}}
</style>
""", unsafe_allow_html=True)

def gen_html(df, cl):
    if isinstance(df, str): return df 
    if df is None or (isinstance(df, pd.DataFrame) and df.empty): 
        return f"<div class='table-responsive-container'><table class='table-compacte {cl}'><tr><td style='text-align: center; padding: 10px;'>Données indisponibles (Vérifiez Dropbox)</td></tr></table></div>"
    
    html_table = df.to_html(index=False, classes=f"table-compacte {cl}", escape=False, border=0)
    return f"<div class='table-responsive-container'>{html_table}</div>"

# --- LECTURE DU PARAMÈTRE DE COURSE DEPUIS L'URL ---
query_params = st.query_params
choix_course_url = query_params.get("course", "essais").lower()
# fin bloc 1
def recuperer_donnees_course():
    # En-têtes configurés proprement
    df_live = pd.DataFrame(columns=["N°", "Nom_Prenom", "Voiture", "Départ", "Arrivée", "Chrono"])
    df_hist = pd.DataFrame(columns=["N°", "Nom_Prenom", "Voiture", "Gr/Div", "Cl", "Chrono"])
    df_racb = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Gr/Div", "Cl", "Chrono"])
    df_asaf123 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Gr/Div", "Cl", "Chrono"])
    df_asaf4 = pd.DataFrame(columns=["Pos", "N°", "Nom_Prenom", "Gr/Div", "Cl", "Chrono"])

    try:
        flux_eng = telecharger_excel(FILE_ENGAGES)
        flux_dep = telecharger_excel(FILE_DEPART)
        flux_arr = telecharger_excel(FILE_ARRIVEE)
        
        df_eng_raw = pd.read_excel(flux_eng, skiprows=1, engine='openpyxl')
        df_dep_raw = pd.read_excel(flux_dep, header=None, engine='openpyxl')
        df_arr_raw = pd.read_excel(flux_arr, header=None, engine='openpyxl')

        idx_dep, idx_arr = None, None
        for c_idx in range(len(df_dep_raw.columns)):
            val = str(df_dep_raw.iloc[1, c_idx]).strip().upper()
            if "ESSAIS" in val or "ENTRAINEMENT" in val: idx_dep = c_idx
        for c_idx in range(len(df_arr_raw.columns)):
            val = str(df_arr_raw.iloc[1, c_idx]).strip().upper()
            if "ESSAIS" in val or "ENTRAINEMENT" in val: idx_arr = c_idx

        df_dep = pd.DataFrame({"N°": df_dep_raw.iloc[2:, idx_dep].apply(nettoyer_numero), "Heure_Depart": df_dep_raw.iloc[2:, idx_dep + 1]}) if idx_dep is not None else pd.DataFrame(columns=["N°", "Heure_Depart"])
        df_arr = pd.DataFrame({"N°": df_arr_raw.iloc[2:, idx_arr].apply(nettoyer_numero), "Heure_Arrivee": df_arr_raw.iloc[2:, idx_arr + 2], "Chrono_Excel": df_arr_raw.iloc[2:, idx_arr + 3]}) if idx_arr is not None else pd.DataFrame(columns=["N°", "Heure_Arrivee", "Chrono_Excel"])

        df_eng_raw.columns = df_eng_raw.columns.astype(str).str.strip().str.upper()
        df_eng = pd.DataFrame({"N°": df_eng_raw.iloc[:, 0].apply(nettoyer_numero), 
                               "Nom_Prenom": df_eng_raw.iloc[:, 1].fillna("Pilote Inconnu").astype(str).str.strip(),
                               "Voiture": df_eng_raw.iloc[:, 4].fillna("").astype(str).str.strip(),
                               "Division": df_eng_raw.iloc[:, 5].apply(lambda x: "-" if pd.isna(x) else str(x).strip()[:-2] if str(x).strip().endswith(".0") else str(x).strip()),
                               "Classe": df_eng_raw.iloc[:, 6].fillna("-").astype(str).str.strip().apply(lambda x: x[:-2] if x.endswith(".0") else x)})

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
                df_live_base["Chrono"] = df_live_base.apply(lambda r: calculer_statut_chrono_essais(r, est_dans_le_live=True), axis=1)
                df_live_base["Arrivée_Brute"] = df_live_base["Heure_Arrivee"].apply(formater_heure_ecran); df_live_base["Départ_Brute"] = df_live_base["Heure_Depart"].apply(formater_heure_ecran)
                df_live = df_live_base[["N°", "Nom_Prenom", "Voiture", "Départ_Brute", "Arrivée_Brute", "Chrono"]].rename(columns={"Départ_Brute": "Départ", "Arrivée_Brute": "Arrivée"})

            base["Chrono_Visual_Hist"] = base.apply(lambda r: "En Piste" if pd.notna(r["Heure_Depart"]) and pd.isna(r["Heure_Arrivee"]) and pd.isna(r["Sec_Excel"]) else format_final_chrono(r["Calc_Sec"]) if pd.notna(r["Calc_Sec"]) and r["Calc_Sec"] > 0 else "No Time", axis=1)
            base["Ordre_Saisie"] = range(len(base))
            df_hist = base.sort_values(by="Ordre_Saisie", ascending=False)[["N°", "Nom_Prenom", "Voiture", "Division", "Classe", "Chrono_Visual_Hist"]].rename(columns={"Chrono_Visual_Hist": "Chrono", "Division": "Gr/Div", "Classe": "Cl"})

            valides = base[base["Calc_Sec"].notna() & (base["Calc_Sec"] > 0)].copy()
            if len(valides) > 0:
                scr = valides.sort_values(by="Calc_Sec").drop_duplicates(subset=["N°"], keep="first").copy()
                scr["Division_Clean"] = scr["Division"].astype(str).str.strip()
                
                exclus_asaf = ["1", "2", "3", "4", "1.0", "2.0", "3.0", "4.0"]
                racb = scr[~scr["Division_Clean"].isin(exclus_asaf)].head(15).copy()
                if len(racb) > 0: 
                    racb["Pos"] = range(1, len(racb) + 1)
                    racb["Chrono"] = racb["Calc_Sec"].apply(format_final_chrono)
                    df_racb = racb[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Gr/Div", "Classe": "Cl"})
                
                asaf123 = scr[scr["Division_Clean"].isin(["1", "2", "3", "1.0", "2.0", "3.0"])].head(15).copy()
                if len(asaf123) > 0: 
                    asaf123["Pos"] = range(1, len(asaf123) + 1)
                    asaf123["Chrono"] = asaf123["Calc_Sec"].apply(format_final_chrono)
                    df_asaf123 = asaf123[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Gr/Div", "Classe": "Cl"})
                
                asaf4 = scr[scr["Division_Clean"].isin(["4", "4.0"])].head(10).copy()
                if len(asaf4) > 0: 
                    asaf4["Pos"] = range(1, len(asaf4) + 1)
                    asaf4["Chrono"] = asaf4["Calc_Sec"].apply(format_final_chrono)
                    df_asaf4 = asaf4[["Pos", "N°", "Nom_Prenom", "Division", "Classe", "Chrono"]].rename(columns={"Division": "Gr/Div", "Classe": "Cl"})
    except Exception: pass

    # CORRECTION : Suppression totale de la variable CSS_ESSAIS d'ici
    t_live = "🏎️ EN DIRECT / Derniers concurrents partis"
    t_hist = "🕒 HISTORIQUE DES TEMPS / ENTRAINEMENTS ASAF & RACB"
    t_racb = "🏆 CLASSEMENT EVOLUTIF DES ESSAIS RACB (Top 15)"
    t_as123 = "🏆 CLASSEMENT EVOLUTIF DES ESSAIS Division 123 (Top 15)"
    t_as4 = "🏆 CLASSEMENT EVOLUTIF DES ESSAIS Division 4 (Top 10)"

    return df_live, df_hist, df_asaf123, df_asaf4, df_racb, t_live, t_hist, t_racb, t_as123, t_as4
