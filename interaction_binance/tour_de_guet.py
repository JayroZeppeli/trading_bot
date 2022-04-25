from interaction_binance import communication
from temps import horloger
from logs.scribe import etat


def guet():
    etat(4)
    while len(communication.ordres_ouverts()) >= 2:
        print('Les ordres ouverts sont :', communication.ordres_ouverts())
        horloger.attendre_quelques_minutes()
        horloger.attendre_prochaine_bougie(True)
    communication.fermer_tout_les_ordres()
    etat(5)

