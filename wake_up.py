import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

URL_RACINE = "https://streamlit.app"

def reveiller_le_serveur_cloud():
    options = Options()
    options.add_argument("--headless")  # Navigateur virtuel invisible
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # On définit une taille d'écran fixe pour que le milieu de l'écran soit toujours le même
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    print(f"[Anti-Sommeil] Connexion à la racine du serveur : {URL_RACINE}")
    driver.get(URL_RACINE)
    
    # ÉTAPE 1 : On laisse 20 secondes à la page pour s'afficher complètement
    print("[Anti-Sommeil] Attente du chargement de la page de veille...")
    time.sleep(20) 
    
    try:
        # ÉTAPE 2 : CLIC PHYSIQUE AU CENTRE (Méthode Anti-Sélecteur)
        # Sur la page d'accueil Streamlit, le bouton "Yes, get this app back up!" 
        # est pile au centre de l'écran. On force un clic à ces coordonnées exactes.
        print("[Anti-Sommeil] Simulation d'un clic de souris au centre exact de l'écran...")
        actions = ActionChains(driver)
        # On se déplace au centre d'une fenêtre 1920x1080 (X=960, Y=540) et on clique
        actions.move_by_offset(960, 540).click().perform()
        print(" -> [RÉVEIL COMMANDÉ] Le clic physique a été envoyé !")
        
        # ÉTAPE 3 : On attend 45 secondes sur la page pour laisser le conteneur démarrer
        print("[Anti-Sommeil] Temporisation... Démarrage du serveur Cloud en cours...")
        time.sleep(45)
        print("[Anti-Sommeil] Le cycle de réveil est terminé.")
        
    except Exception as e:
        print(f" -> [ERREUR] Impossible d'envoyer le clic : {e}")
        
    driver.quit()

if __name__ == "__main__":
    reveiller_le_serveur_cloud()
