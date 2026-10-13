import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Liste de vos 8 pages de course à surveiller
COURSES = [
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app",
    "https://streamlit.app"
]

def reveiller_les_courses():
    # Configuration du navigateur invisible Chrome pour le serveur GitHub
    options = Options()
    options.add_argument("--headless")  # Exécution sans fenêtre
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for url in COURSES:
        print(f"[Anti-Sommeil] Navigation vers : {url}")
        driver.get(url)
        time.sleep(10)  # Laisse la page se charger
        
        try:
            # Recherche du bouton de réveil Streamlit Cloud par son texte
            # (Il contient le texte "Yes, get this app back up!")
            bouton = driver.find_element(By.XPATH, "//*[contains(text(), 'get this app back up')]")
            bouton.click()
            print(f" -> [SUCCÈS] Bouton détecté et cliqué ! Réveil en cours...")
            time.sleep(5)  # Attend la validation du clic
        except Exception:
            # Si le bouton n'est pas là, c'est que l'application était déjà réveillée
            print(" -> [OK] L'application est déjà en ligne et éveillée.")
            
    driver.quit()

if __name__ == "__main__":
    reveiller_les_courses()
