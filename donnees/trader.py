from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from donnees.extracteur_de_donnees import extraction, graphique
from logs.scribe import etat
from automate.parametres import *


def enleve_debut_des_donnees(table):
    """Enleve le début des données où les indicateurs ne sont pas encore initialisés"""
    return table.iloc[(nb_jours_initialisation_indicateurs*nb_de_bougie_par_jour):]


def determine_debut_des_donnees():
    date_du_jour = datetime.now()
    date_de_debut = date_du_jour - strategie_a_appliquer.nombre_de_jours_necessaires - timedelta(days=nb_jours_initialisation_indicateurs)
    return date_de_debut.strftime("%Y-%m-%d")


def choix_position():
    etat(2)
    table = extraction(determine_debut_des_donnees())
    prix_actuel = table["Close"].iloc[-1]
    table = strategie_a_appliquer.calcul_indicateurs(table)
    table = enleve_debut_des_donnees(table)
    return strategie_a_appliquer.signal(table), taille_des_positions_en_dollars / prix_actuel


def observer_les_cours():
    table = extraction(determine_debut_des_donnees())
    graphique(enleve_debut_des_donnees(table))


def observer_indicateurs_strategie(table_indicateurs, table_prete, table=extraction(determine_debut_des_donnees())):
    if not table_prete:
        table = strategie_a_appliquer.calcul_indicateurs(table)
    table = enleve_debut_des_donnees(table)
    for indicateur in table_indicateurs:
        plt.plot(table["Close Time"], table[indicateur])
    plt.show()





