import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time

# Importer la fonction format_date depuis date_utils.py
from date_utils import format_date

# Fonction pour charger les clés uniques existantes dans le CSV
def load_existing_keys(csv_file):
    existing_keys = set()
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                existing_keys.add(row[0])  # Clé unique est la première colonne
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourner un set vide
        return existing_keys
    return existing_keys

# Configurer les options pour utiliser Chrome en mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Configurer le driver avec les options headless
driver = webdriver.Chrome(options=chrome_options)

# Chargez la première page
page_num = 1
csv_file = 'job_offers.csv'
existing_keys = load_existing_keys(csv_file)

# Préparer le fichier CSV et charger les clés existantes
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Si le fichier est vide, ajouter l'en-tête
    if file.tell() == 0:
        writer.writerow(["Unique Key", "Titre", "Date Publiée", "Localisation", "Temps Plein", "Contrat", "Entreprise"])

    while page_num <= 100 :
        page_url=f"https://www.jobs.ch/fr/offres-emplois/?page={page_num}&term=data+engineer"
        print(f"analysing page : {page_url}")
        driver.get(page_url)
        time.sleep(3)  # Ajouter un délai pour permettre au contenu de se charger

        # Trouver les conteneurs principaux des offres
        offers = driver.find_elements(By.XPATH, "//*[@data-feat='searched_jobs']")

        # Si aucune offre n'est trouvée, on quitte la boucle (fin des pages)
        if not offers:
            print("Aucune offre trouvée, arrêt de la récupération des pages.")
            break

        # Extraire les détails et les enregistrer dans le fichier CSV
        for offer in offers:
            try:
                offer_link = offer.find_element(By.CSS_SELECTOR, "a[data-cy='job-link']")
                # Extraire l'attribut 'href'
                job_link = offer_link.get_attribute('href')
                # job_link = offer.find_elements(By.XPATH, "//*[@href='searched_jobs']")

                title = offer.find_element(By.CLASS_NAME, "mb_s8").text  # Titre
                date_published = format_date(offer.find_elements(By.CLASS_NAME, "mb_s12")[0].text)  # Date publiée
                location = offer.find_elements(By.CLASS_NAME, "mb_s12")[1].text  # Localisation
                full_time = offer.find_elements(By.CLASS_NAME, "mb_s12")[2].text  # Temps plein
                contract = offer.find_elements(By.CLASS_NAME, "mb_s12")[3].text  # Contrat
                company = offer.find_elements(By.CLASS_NAME, "mb_s12")[4].text  # Entreprise

                # Créer une clé unique en combinant les éléments
                unique_key = f"{title} | {company} | {date_published} | {location}"

                # Si la clé existe déjà, ignorer cette offre
                if unique_key not in existing_keys:
                    # Écrire les données dans le fichier CSV
                    writer.writerow([unique_key, title, date_published, location, full_time, contract, company, job_link])
                    existing_keys.add(unique_key)  # Ajouter la clé unique à l'ensemble pour éviter les doublons
                else:
                    print(f"Doublon trouvé, l'offre '{title}' de '{company}' est déjà présente.")

            except Exception as e:
                print(f"Erreur lors de l'extraction : {e}")

        # # Vérifier si la page suivante existe en utilisant le bouton "Next"
        # try:
        #     next_button = driver.find_element(By.CSS_SELECTOR, "span.color-palette_button.brand[title='Suivant']")
        #     # Si l'élément est trouvé, cela signifie qu'il y a plus de pages à scraper
        #     # print("Il y a encore des pages à scraper.")            # Si le bouton "Next" est cliquable, on passe à la page suivante
        #     page_num += 1
        #     print(f"Passage à la page {page_num}")
        # except Exception as e:
        #     # Si l'élément "Next" n'existe pas, on a atteint la dernière page
        #     print("Dernière page atteinte, arrêt de la récupération.")
        #     break
        page_num += 1

driver.quit()
