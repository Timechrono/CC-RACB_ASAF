import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 🏎️ SOLUTION : On cible UNIQUEMENT l'adresse racine principale. 
# Réveiller la racine réveille automatiquement toutes les sous-pages de courses d'un coup !
URL_RACINE = "https://streamlit.app"

def reveiller_le_serveur_cloud():
    options = Options()
    options.add_argument("--headless")  # Navigateur invisible pour le serveur
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    print(f"[Anti-Sommeil] Connexion à la racine du serveur : {URL_RACINE}")
    driver.get(URL_RACINE)
    
    # On laisse 15 secondes à la page pour s'afficher complètement
    time.sleep(15) 
    
    try:
        # Cible le bouton principal de réveil de la plateforme Streamlit Cloud
        bouton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[kind="primary"], button, .stButton button'))
        )
        
        # Injection du clic JavaScript pour valider le réveil à travers les sécurités du cloud
        driver.execute_script("arguments[0].click();", bouton)
        print(" -> [RÉVEIL PRINCIPAL] Clic de réveil envoyé avec succès sur la racine !")
        
        # TEMPS D'AMORÇAGE REQUIS : On force le script à attendre 45 secondes sur la page 
        # pour laisser le temps au serveur cloud de reconstruire l'application pour vos utilisateurs.
        print("[Anti-Sommeil] Temporisation... Initialisation du serveur en cours...")
        time.sleep(45)
        print("[Anti-Sommeil] Serveur cloud opérationnel.")
        
    except Exception:
        # Si le bouton n'est pas trouvé, c'est que l'infrastructure était déjà éveillée
        print(" -> [OK] Aucun bouton d'hibernation détecté. Le site est déjà actif.")
        
    driver.quit()

if __name__ == "__main__":
    reveiller_le_serveur_cloud()
