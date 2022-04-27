import time
from datetime import datetime
from logs.scribe import ecrit_rapport, etat
from automate import parametres


def horloge():
    heures = int(datetime.now().strftime("%H"))
    minutes = round(int(datetime.now().strftime("%M")) / 60, 2)
    return heures + minutes


def definire_heure_la_plus_proche(heure_actuelle, heures_possibles):
    for heure in heures_possibles:
        if heure_actuelle < heure or heure_actuelle < (heure + parametres.marge_erreur_horloger_en_heure):
            return heure
    return parametres.premiere_bougie_de_la_journee[parametres.time_frame_a_utiliser]


def attendre_quelques_minutes():
    time.sleep(parametres.marge_erreur_horloger_en_heure * 60 + 10)


def attendre_prochaine_bougie(tout_de_suite):
    etat(0)
    heures_possibles = parametres.fractionnement_des_heures[parametres.time_frame_a_utiliser]
    heure_actuelle = horloge()
    heure_de_reveil = definire_heure_la_plus_proche(heure_actuelle, heures_possibles) + parametres.unite_time_frame_en_h * (not tout_de_suite)
    if not (heure_de_reveil <= heure_actuelle <= (heure_de_reveil + parametres.marge_erreur_horloger_en_heure + 0.03)):
        if heure_actuelle < heure_de_reveil:
            temps_repos = round(heure_de_reveil - heure_actuelle, 2) * 60
        else:
            temps_repos = round(24 - heure_actuelle + heure_de_reveil, 2) * 60
        ecrit_rapport("L'automate s'endort. Il ne se réveillera pas avant " + str(
            round(temps_repos, 2) + parametres.temps_avant_initialisation_nouvelle_bougie_binance_data) + " bonnes minutes de repos.")
        # on convertit les heures en minutes puis en secondes car time.sleep ne prend que des minutes en argument
        time.sleep((temps_repos + parametres.temps_avant_initialisation_nouvelle_bougie_binance_data) * 60)
    ecrit_rapport("Reveil. La bougie vient de fermer.")



