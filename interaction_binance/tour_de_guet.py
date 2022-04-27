from interaction_binance import communication
from temps import horloger
from logs.scribe import etat


def affiche_ordres(liste_ordres):
    print("Les ordres ouverts sont :")
    for ordre in liste_ordres:
        print(f"Ordre {ordre['type']} {ordre['side']} sur {ordre['symbol']} à {ordre['price']}$ (stop price de {ordre['stopPrice']}$).")
    print("\n\n")


def guet():
    etat(3)
    liste_ordres = communication.ordres_ouverts()
    while len(liste_ordres) >= 2:
        horloger.attendre_quelques_minutes()
        horloger.attendre_prochaine_bougie(True)
        liste_ordres = communication.ordres_ouverts()
    communication.fermer_tout_les_ordres()
    etat(4)
