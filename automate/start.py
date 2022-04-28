import sys
import platform

if platform.system() != 'Windows':
    sys.path.append('/home/diavolo/Téléchargements/trading_bot-main')

from logs.scribe import ecrit_rapport, etat, archivage_des_logs
from logs.interaction_mail import envoyer_mail
from temps.horloger import attendre_prochaine_bougie, attendre_quelques_minutes
from interaction_binance.communication import ouvrir_position
from interaction_binance.tour_de_guet import guet
from donnees.trader import choix_position


def automate(position=False):
    ecrit_rapport("Lancement...", initialisation=True)
    while True:
        if position:
            guet()
        attendre_prochaine_bougie()
        [position, sens, take_profit, stop_loss], quantite = choix_position()
        if not position:
            etat(5)
            attendre_quelques_minutes()
            continue
        ouvrir_position(sens, take_profit, stop_loss, quantite)


try:
    automate()
except Exception as exception:
    ecrit_rapport("Erreur rencontrée. Fin du programme.")
    ecrit_rapport(f"Détails de l'erreur: {exception}")
    archivage_des_logs()
    envoyer_mail("L'automate s'est arrete", f"L'automate a rencontre une erreur. "
                                            f"Le programme a pris fin. "
                                            f"Les details de l'erreur sont consultables dans les logs")

