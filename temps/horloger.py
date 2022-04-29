import time
from datetime import datetime
from logs.scribe import ecrit_rapport
from automate import parametres


def horloge():
    date = datetime.now()
    heures = int(date.strftime("%H"))
    minutes = int(date.strftime("%M")) / 60
    secondes = int(date.strftime("%S")) / 3600
    return heures + minutes + secondes


def definire_heure_la_plus_proche(heure_actuelle, heures_possibles):
    for heure in heures_possibles:
        if heure_actuelle < heure or heure_actuelle < (heure + parametres.marge_erreur_horloger_en_heure):
            return heure
    return parametres.premiere_bougie_de_la_journee[parametres.time_frame_a_utiliser]


def attendre_quelques_minutes():
    time.sleep(parametres.marge_erreur_horloger_en_heure * 3600 + 10)


def attendre_prochaine_bougie(tout_de_suite=True):
    heures_possibles = parametres.fractionnement_des_heures[parametres.time_frame_a_utiliser]
    heure_actuelle = horloge()
    heure_de_reveil = definire_heure_la_plus_proche(heure_actuelle, heures_possibles) + parametres.unite_time_frame_en_h * (not tout_de_suite)
    if not (heure_de_reveil <= heure_actuelle <= (heure_de_reveil + parametres.marge_erreur_horloger_en_heure + 0.03)):
        if heure_actuelle < heure_de_reveil:
            temps_repos = heure_de_reveil - heure_actuelle
        else:
            temps_repos = 24 - heure_actuelle + heure_de_reveil
        temps_repos = round(temps_repos * 60 + parametres.temps_decalage_update_base_de_donnee_binance_en_minute, 4)
        ecrit_rapport(f"L'automate s'endort pour {round(temps_repos, 2)} bonnes minutes de repos.")
        # on convertit les heures en minutes puis en secondes car time.sleep ne prend que des minutes en argument
        time.sleep(temps_repos * 60)
    ecrit_rapport("Réveil.")
