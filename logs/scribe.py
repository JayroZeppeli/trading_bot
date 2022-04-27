import datetime
import gspread
import csv
from automate.parametres import raspberry

emplacement = ('../logs/rapport.csv', '/home/diavolo/Téléchargements/trading_bot-main/rapport.csv')
emplacement_a_utiliser = emplacement[raspberry]


def ecrit_rapport(information, initialisation=False):
    mot_de_lecture = ['a', 'w'][initialisation]
    with open(emplacement_a_utiliser, mot_de_lecture) as rapport_brut:
        colonnes = ["Date", "Information"]
        rapport = csv.DictWriter(rapport_brut, fieldnames=colonnes, quotechar='', quoting=csv.QUOTE_NONE)
        if initialisation:
            rapport.writeheader()
        rapport.writerow({"Date": datetime.datetime.now().strftime("%d %b %Y a %H:%M:%S"), "Information": information})


def etat(numero):
    etats = ['lancement', 'sommeil', 'lecture et analyse', "ouverture de position",
             'position ouverte', 'position close', 'pas de signal']
    ecrit_rapport(f"L'automate entre dans l'état : {etats[numero]}.")


def archivage_des_logs():
    compte_service = gspread.service_account(filename="service_account.json")
    fichier = compte_service.open("logs_digitaux")
    feuille = fichier.worksheet("data")
    nombre_colonnes = 1
    with open(emplacement_a_utiliser, "r") as rapport_brut:
        rapport = csv.DictReader(rapport_brut)
        dates_informations = []
        for ligne in rapport:
            dates_informations.append([ligne['Date'], ligne['Information']])
        feuille.update(f"A{nombre_colonnes+1}:B{len(dates_informations)+nombre_colonnes}", dates_informations)







