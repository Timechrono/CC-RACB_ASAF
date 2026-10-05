# ==============================================================================
# PARTIE 1 : CONFIGURATIONS, DESIGN ET FONCTIONS DE CONVERSION
# ==============================================================================
import streamlit as st
import pandas as pd
import datetime
import os
import time
import requests  
import io        

def injecter_styles_css():
    st.markdown("""
        <style>
        [data-testid="stHeader"] { display: none !important; }
        .coche-verte { color: #22C55E !important; font-weight: bold !important; font-size: 1.1rem !important; margin-right: 6px; }
        .coche-rouge { color: #EF4444 !important; font-weight: bold !important; font-size: 1.1rem !important; margin-right: 6px; }
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
        .table-compacte td { font-weight: normal !important; border-bottom: 1px solid #E0E0E0 !important; background-color: #FFFFFF !important; }
        .table-compacte th { font-weight: bold !important; background-color: #F5F5F5 !important; border-bottom: 2px solid #CCCCCC !important; text-align: left !important; }
        .table-compacte td.meilleur-temps { background-color: #d9fcec !important; color: #000000 !important; font-weight: bold !important; }
        .table-class-robuste tr:nth-child(odd) td { background-color: #E0F2FE !important; }
        .ligne-separation-classe td { border-bottom: 2px solid #1E3A8A !important; }
        .table-hist td:nth-last-child(2), .table-hist td:last-child, .table-live td:last-child, .table-class-robuste td:last-child {
            font-weight: bold !important; font-size: 0.94rem !important; color: #0F172A !important;
        }
        .table-live th:nth-child(1), .table-live td:nth-child(1) { width: 8% !important; }
        .table-live th:nth-child(2), .table-live td:nth-child(2) { width: 26% !important; }
        .table-live th:nth-child(3), .table-live td:nth-child(3) { width: 18% !important; }
        .table-live th:nth-child(4), .table-live td:nth-child(4) { width: 13% !important; }
        .table-live th:nth-child(5), .table-live td:nth-child(5) { width: 13% !important; }
        .table-live th:nth-child(6), .table-live td:nth-child(6) { width: 22% !important; }
        .table-hist th:nth-child(1), .table-hist td:nth-child(1) { width: 7% !important; }   
        .table-hist th:nth-child(2), .table-hist td:nth-child(2) { width: 23% !important; }  
        .table-hist th:nth-child(3), .table-hist td:nth-child(3) { width: 25% !important; }  
        .table-hist th:nth-child(4), .table-hist td:nth-child(4) { width: 10% !important; }   
        .table-hist th:nth-child(5), .table-hist td:nth-child(5) { width: 7% !important; }   
        .table-hist th:nth-child(6), .table-hist td:nth-child(6) { width: 14% !important; }  
        .table-hist th:nth-child(7), .table-hist td:nth-child(7) { width: 14% !important; }  
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
        .block-container { padding-top: 0.3rem !important; padding-bottom: 0rem !important; }
        div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
        hr { margin: 6px 0px !important; border: 0 !important; height: 0 !important; }
        </style>
    """, unsafe_allow_html=True)

def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    reponse = requests.get(url, headers=entetes, timeout=12)
    reponse.raise_for_status()
    return io.BytesIO(reponse.content)

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

def calculer_statut_chrono(row, est_dans_le_live=True):
    if "Calc_Sec_2" in row and pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0:
        chrono_txt = format_final_chrono(row["Calc_Sec_2"])
        if est_dans_le_live:
            if row["Calc_Sec_2"] >= 240:
                return f"<span class='coche-rouge'>✗</span> {chrono_txt}"
            else:
                return f"<span class='coche-verte'>✓</span> {chrono_txt}"
        return chrono_txt
    if "Heure_Depart_2" in row and pd.notna(row["Heure_Depart_2"]) and ("Heure_Arrivee_2" in row and pd.isna(row["Heure_Arrivee_2"])):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    if classe_specifique == "table-class-groupes" and "Classe" in df.columns:
        cols_a_retirer = ["Cl_Tri_Num", "Cl_Tri_Suff"]
        colonnes_visibles = [c for c in df.columns if c not in cols_a_retirer]
        html = f"<table class='table-compacte table-class-groupes'><thead><tr>"
        for col in colonnes_visibles: html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for idx in range(len(df)):
            classe_row = "class='ligne-separation-classe'" if idx < len(df) - 1 and str(df.iloc[idx]["Classe"]) != str(df.iloc[idx + 1]["Classe"]) else ""
            html += f"<tr {classe_row}>"
            for col in colonnes_visibles: html += f"<td>{df.iloc[idx][col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

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
def telecharger_excel(url):
    entetes = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    reponse = requests.get(url, headers=entetes, timeout=12)
    reponse.raise_for_status()
    return io.BytesIO(reponse.content)

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
def calculer_statut_chrono(row, est_dans_le_live=True):
    if "Calc_Sec_2" in row and pd.notna(row["Calc_Sec_2"]) and row["Calc_Sec_2"] > 0:
        chrono_txt = format_final_chrono(row["Calc_Sec_2"])
        if est_dans_le_live:
            if row["Calc_Sec_2"] >= 240:
                return f"<span class='coche-rouge'>✗</span> {chrono_txt}"
            else:
                return f"<span class='coche-verte'>✓</span> {chrono_txt}"
        return chrono_txt
    if "Heure_Depart_2" in row and pd.notna(row["Heure_Depart_2"]) and ("Heure_Arrivee_2" in row and pd.isna(row["Heure_Arrivee_2"])):
        return "<span class='vrai-gyrophare'>🚨</span> EN PISTE" if est_dans_le_live else "En Piste"
    return "No Time"

def generer_tableau_html(df, classe_specifique):
    if df.empty: 
        return f"<table class='table-compacte {classe_specifique}'><tr><td style='text-align: center; padding: 10px;'>Aucune donnée disponible</td></tr></table>"
    if classe_specifique == "table-class-groupes" and "Classe" in df.columns:
        cols_a_retirer = ["Cl_Tri_Num", "Cl_Tri_Suff"]
        colonnes_visibles = [c for c in df.columns if c not in cols_a_retirer]
        html = f"<table class='table-compacte table-class-groupes'><thead><tr>"
        for col in colonnes_visibles: html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for idx in range(len(df)):
            classe_row = "class='ligne-separation-classe'" if idx < len(df) - 1 and str(df.iloc[idx]["Classe"]) != str(df.iloc[idx + 1]["Classe"]) else ""
            html += f"<tr {classe_row}>"
            for col in colonnes_visibles: html += f"<td>{df.iloc[idx][col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html
    return df.to_html(index=False, classes=f"table-compacte {classe_specifique}", escape=False, border=0)

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
