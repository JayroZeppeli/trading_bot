import datetime
import gspread
import csv
import platform

emplacement = ('../logs/rapport.csv', '/home/diavolo/Téléchargements/trading_bot-main/logs/rapport.csv')
emplacement_a_utiliser = emplacement[platform.system() != 'Windows']


def definire_taille_fichier():
    with open(emplacement_a_utiliser, "r") as rapport_brut:
        taille_fichier = len(list(csv.reader(rapport_brut)))
    return taille_fichier


def ecrit_rapport(information, initialisation=False):
    information = information.replace('\n', ' ')
    initialisation = initialisation or definire_taille_fichier() >= 400
    mot_de_lecture = ['a', 'w'][initialisation]
    with open(emplacement_a_utiliser, mot_de_lecture) as rapport_brut:
        colonnes = ["Date", "Information"]
        rapport = csv.DictWriter(rapport_brut, fieldnames=colonnes, quotechar='', quoting=csv.QUOTE_NONE)
        if initialisation:
            rapport.writeheader()
            archivage_des_logs(True)
        rapport.writerow({"Date": datetime.datetime.now().strftime("%d %b %Y a %H:%M:%S"), "Information": information})


def etat(numero):
    etats = ['Sommeil', 'Lecture et analyse', 'Ouverture de position', 'Position ouverte', 'Position close', 'Pas de signal']
    ecrit_rapport(f"État : {etats[numero]}")
    if numero in [3, 5]:
        archivage_des_logs()


def archivage_des_logs(vider_la_feuille=False):
    try:
        if platform.system() != 'Windows':
            chemin = '/home/diavolo/Téléchargements/trading_bot-main/logs/service_account.json'
        else:
            chemin = 'E:/Documents/Utilitaire/Trading/algorithme_ultime/logs/service_account.json'
        compte_service = gspread.service_account(filename=chemin)
        fichier = compte_service.open("logs_digitaux")
        feuille = fichier.worksheet("data")
        if vider_la_feuille:
            feuille.clear()
        with open(emplacement_a_utiliser, "r") as rapport_brut:
            rapport = csv.DictReader(rapport_brut)
            dates_informations = [['Date', 'Information']]
            for ligne in rapport:
                dates_informations.append([ligne['Date'], ligne['Information']])
            feuille.update(f"A1:B{len(dates_informations)+1}", dates_informations)
    except Exception:
        erreur = "Problème de connexion à l'API Google Sheet"
        ecrit_rapport(erreur)
        print(erreur)
