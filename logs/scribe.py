import datetime


def ecrit_rapport(information, initialisation=False, saut_de_ligne="\n"):
    if initialisation:
        document_confidentiel = open('../logs/rapport.txt', "w")
        etat(0)
    document_confidentiel = open('../logs/rapport.txt', "a")
    document_confidentiel.write(f"{saut_de_ligne}Le {datetime.datetime.now()} {information}\n")


def etat(numero):
    etats = ['lancement', 'sommeil', 'lecture et analyse', "ouverture de position",
             'position ouverte', 'position close', 'pas de signal']
    ecrit_rapport(f"L'automate entre dans l'état : {etats[numero]}.")

