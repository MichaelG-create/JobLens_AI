from datetime import datetime

# Dictionnaire pour convertir les mois en français en leur valeur numérique
month_translation = {
    "janvier": 1, "février": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12
}


# Fonction pour convertir la date au format désiré
def format_date(date_str):
    try:
        # Retirer la partie 'Publié:' et les retours à la ligne
        date_str = date_str.split("\n")[0].replace("Publié: ", "").strip()

        # Cas où la date est au format '09 nov.' (court)
        if len(date_str.split()) == 2:
            day, month_name = date_str.split()
            month = month_translation[month_name.lower()]
            year = datetime.now().year  # Utilise l'année actuelle si aucune année n'est donnée
            formatted_date = f"{year}/{str(month).zfill(2)}/{day.zfill(2)}"

        # Cas où la date est au format '09 novembre 2024' (complet)
        else:
            day, month_name, year = date_str.split()
            month = month_translation[month_name.lower()]
            formatted_date = f"{year}/{str(month).zfill(2)}/{day.zfill(2)}"

        return formatted_date

    except Exception as e:
        print(f"Erreur lors de la conversion de la date: {e}")
        return date_str  # Si une erreur se produit, retourner la date d'origine
