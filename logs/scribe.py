import csv
import datetime
import platform
import gspread
from logs import interaction_mail

booleen_os = platform.system() != 'Windows'
emplacement_csv = ('../logs/rapport.csv', '/home/diavolo/Téléchargements/trading_bot-main/logs/rapport.csv')
emplacement_txt = ('../automate/palier_actuel.txt', '/home/diavolo/Téléchargements/trading_bot-main/automate/palier_actuel.txt')
emplacement_a_utiliser_csv = emplacement_csv[booleen_os]
emplacement_a_utiliser_txt = emplacement_txt[booleen_os]


def definire_palier_actuel():
    fichier = open(emplacement_a_utiliser_txt, "r")
    return int(fichier.read())


def modifier_palier_actuel(palier):
    ecrit_rapport(f"Changement de palier, l'automate va commencer à trader avec {palier}")
    try:
        interaction_mail.envoyer_mail("Changement tailles de position",
                                      "Le portfolio de l'automate a atteint une taille consequente. "
                                      f"A partir de maintenant, il va trader avec {palier}$.")
    except Exception:
        print(f"Echec de l'envoi du mail de changement de palier, nous passons à des trades de {palier}$.")
    fichier = open(emplacement_a_utiliser_txt, "w")
    fichier.write(str(int(palier)))


def definire_taille_fichier():
    with open(emplacement_a_utiliser_csv, "r") as rapport_brut:
        taille_fichier = len(list(csv.reader(rapport_brut)))
    return taille_fichier


def ecrit_rapport(information, initialisation=False):
    information = information.replace('\n', ' ')
    initialisation = initialisation or definire_taille_fichier() >= 400
    mot_de_lecture = ['a', 'w'][initialisation]
    with open(emplacement_a_utiliser_csv, mot_de_lecture) as rapport_brut:
        colonnes = ["Date", "Information"]
        rapport = csv.DictWriter(rapport_brut, fieldnames=colonnes, quotechar='', quoting=csv.QUOTE_NONE)
        if initialisation:
            rapport.writeheader()
            archivage_des_logs(True)
        rapport.writerow({"Date": datetime.datetime.now().strftime("%d %b %Y a %H:%M:%S"), "Information": information})


def etat(numero):
    etats = ['Sommeil', 'Lecture et analyse', 'Ouverture de position', 'Position ouverte', 'Position close',
             'Pas de signal']
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
        with open(emplacement_a_utiliser_csv, "r") as rapport_brut:
            rapport = csv.DictReader(rapport_brut)
            dates_informations = [['Date', 'Information']]
            for ligne in rapport:
                dates_informations.append([ligne['Date'], ligne['Information']])
            feuille.update(f"A1:B{len(dates_informations) + 1}", dates_informations)
    except Exception:
        erreur = "Problème de connexion à l'API Google Sheet"
        ecrit_rapport(erreur)
        print(erreur)
