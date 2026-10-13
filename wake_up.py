import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
    options = Options()
    options.add_argument("--headless")  # Rendre Chrome invisible
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for url in COURSES:
        print(f"Vérification de : {url}")
        driver.get(url)
        time.sleep(12)  # Temps nécessaire pour que Streamlit Cloud charge l'interface
        
        try:
            # Recherche de l'élément contenant le bouton de réveil
            bouton = driver.find_element(By.XPATH, "//*[contains(text(), 'get this app back up')]")
            bouton.click()
            print(" -> [RÉVEIL DE LA PAGE] Clic effectué !")
            time.sleep(5)
        except Exception:
            print(" -> [OK] Déjà réveillée.")
            
    driver.quit()

if __name__ == "__main__":
    reveiller_les_courses()
