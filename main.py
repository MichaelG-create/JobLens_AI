from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurer le driver
driver = webdriver.Chrome()
# Chargez votre fichier HTML local
# driver.get(r"file:///home/micha/T%C3%A9l%C3%A9chargements/20970%20postes%20pour%20Data%20-%20jobs.ch.html")
page_num=1
driver.get(r"https://www.jobs.ch/fr/offres-emplois/?page=" + str(page_num) + "&term=data+engineer")

# https://www.jobs.ch/fr/offres-emplois/?page=2&term=data+engineer

# Trouver les conteneurs principaux des offres
offers = driver.find_elements(By.XPATH, "//*[@data-feat='searched_jobs']")  # Adaptez si nécessaire

# Extraire les détails
for offer in offers:
    try:
        title = offer.find_element(By.CLASS_NAME, "mb_s8").text  # Titre
        date_published = offer.find_elements(By.CLASS_NAME, "mb_s12")[0].text  # Localisation (2e élément)
        location = offer.find_elements(By.CLASS_NAME, "mb_s12")[1].text  # Localisation (2e élément)
        full_time = offer.find_elements(By.CLASS_NAME, "mb_s12")[2].text  # Contrat (3e élément)
        contract = offer.find_elements(By.CLASS_NAME, "mb_s12")[3].text  # Contrat (3e élément)
        company = offer.find_elements(By.CLASS_NAME, "mb_s12")[4].text  # Entreprise (1er élément)

        print(f"Titre: {title}, " 
              f"date_published: {date_published}, "
              f"Localisation: {location}, "
              f"full_time: {full_time}, "
              f"Contrat: {contract}, "
              f"Entreprise: {company}, "
        )


    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")

driver.quit()
