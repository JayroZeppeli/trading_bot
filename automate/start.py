import sys
# sys.path.append('/home/diavolo/Documents/trading_bot')

from logs.scribe import ecrit_rapport, etat
from temps.horloger import attendre_prochaine_bougie, attendre_quelques_minutes
from interaction_binance.communication import ouvrir_position
from interaction_binance.tour_de_guet import guet
from donnees.trader import choix_position


def automate():
    ecrit_rapport("L'automate est lancé.", initialisation=True)
    while True:
        attendre_prochaine_bougie(True)
        [position, sens, take_profit, stop_loss], quantite = choix_position()
        if not position:
            etat(6)
            attendre_quelques_minutes()
            continue
        ouvrir_position(sens, take_profit, stop_loss, quantite)
        guet()


automate()














