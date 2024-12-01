from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurer le driver Selenium
driver = webdriver.Chrome()

# Charger la page cible
url = "https://www.jobs.ch/fr/offres-emplois/?term=data"
driver.get(url)

# Attendre que la page se charge complètement
driver.implicitly_wait(10)

# Trouver les offres d'emploi dans la page
job_elements = driver.find_elements(By.XPATH, '//article[contains(@class, "sc-")]')

# Parcourir chaque élément pour extraire les informations
for job in job_elements:
    try:
        # Nom du poste
        job_title = job.find_element(By.XPATH, './/h2').text

        # Nom de l'entreprise (plus générique)
        company_name = job.find_element(By.XPATH, './/p[contains(@class, "sc-")]').text

        # Lien vers l'offre
        job_link = job.find_element(By.XPATH, './/a').get_attribute('href')

        # Affichage des résultats
        print(f"Poste : {job_title}")
        print(f"Entreprise : {company_name}")
        print(f"Lien : {job_link}")
        print("-" * 50)
    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")

# Fermer le driver
driver.quit()
