import sys
import platform

if platform.system() != 'Windows':
    sys.path.append('/home/diavolo/Téléchargements/trading_bot-main')

from logs.scribe import ecrit_rapport, etat, archivage_des_logs
from temps.horloger import attendre_prochaine_bougie, attendre_quelques_minutes
from interaction_binance.communication import ouvrir_position
from interaction_binance.tour_de_guet import guet
from donnees.trader import choix_position


def automate(deja_en_position=False):
    ecrit_rapport("Lancement...", initialisation=True)
    while True:
        if deja_en_position:
            guet()
        attendre_prochaine_bougie(True)
        [position, sens, take_profit, stop_loss], quantite = choix_position()
        if not position:
            etat(5)
            attendre_quelques_minutes()
            continue
        ouvrir_position(sens, take_profit, stop_loss, quantite)
        guet()


automate()














