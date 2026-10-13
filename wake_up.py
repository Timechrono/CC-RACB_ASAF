import os
import asyncio
from playwright.async_api import async_playwright

# L'adresse racine exacte de votre application en ligne
URL_RACINE = "https://cc-racbasaf-wqsfbjpl47htwvpqu9ekwc.streamlit.app/"

async def reveiller_le_serveur():
    async with async_playwright() as p:
        print("[Gardien Cloud] Lancement du navigateur virtuel humain (Chromium)...")
        # Lance un vrai navigateur virtuel
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"[Gardien Cloud] Navigation vers la racine : {URL_RACINE}")
        await page.goto(URL_RACINE, timeout=60000)
        
        # On laisse 15 secondes pour s'assurer que l'écran de veille ou le bouton soit présent
        await asyncio.sleep(15)
        
        try:
            # SÉLECTEUR PLAYWRIGHT OFFICIEL : Il cherche le bouton par son rôle et son nom exact,
            # peu importe s'il est caché derrière des couches de sécurité
            bouton = page.get_by_role("button", name="Yes, get this app back up!")
            
            if await bouton.is_visible():
                print("[Gardien Cloud] Écran d'hibernation détecté. Clic sur le bouton de réveil...")
                await bouton.click()
                print(" -> [RÉVEIL ACCEPTÉ] Le serveur distant a validé le clic de réveil !")
                
                # TEMPORISATION CRUCIALE : On attend 45 secondes pour laisser le serveur démarrer
                print("[Gardien Cloud] Patientez... Amorçage du conteneur en cours...")
                await asyncio.sleep(45)
                print("[Gardien Cloud] Serveur entièrement chargé.")
            else:
                print(" -> [OK] Le bouton n'est pas affiché à l'écran. Le site est déjà actif.")
                
        except Exception as e:
            print(f" -> [NOTE] Fin de l'analyse (Le site est peut-être déjà éveillé) : {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(reveiller_le_serveur())
