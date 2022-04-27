import datetime


def ecrit_rapport(information, initialisation=False, saut_de_ligne="\n"):
    emplacement_pc = '../logs/rapport.txt'
    emplacement_raspberry = '/home/diavolo/Documents/trading_bot/rapport.txt'
    emplacement_a_utiliser = emplacement_pc
    if initialisation:
        document_confidentiel = open(emplacement_a_utiliser, "w")
        etat(0)
    document_confidentiel = open(emplacement_a_utiliser, "a")
    document_confidentiel.write(f"{saut_de_ligne}Le {datetime.datetime.now()} {information}\n")


def etat(numero):
    etats = ['lancement', 'sommeil', 'lecture et analyse', "ouverture de position",
             'position ouverte', 'position close', 'pas de signal']
    ecrit_rapport(f"L'automate entre dans l'état : {etats[numero]}.")

