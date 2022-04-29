from datetime import datetime, timedelta

import matplotlib.pyplot as plt

from automate.parametres import *
from donnees.extracteur_de_donnees import extraction, graphique, usdt_dispo
from logs.scribe import modifier_palier_actuel


def enleve_debut_des_donnees(table):
    """Enleve le début des données où les indicateurs ne sont pas encore initialisés"""
    return table.iloc[int((nb_jours_initialisation_indicateurs * nb_de_bougie_par_jour)):]


def enleve_bougie_non_terminee(table):
    if table["Close Time"].iloc[-1] > datetime.now():
        return table.head(len(table) - 1)


def determine_debut_des_donnees():
    date_du_jour = datetime.now()
    date_de_debut = date_du_jour - timedelta(days=nb_jours_initialisation_indicateurs)
    return date_de_debut.strftime("%Y-%m-%d")


def determine_taille_position():
    taille_du_portfolio = usdt_dispo()
    taille_positions = definire_palier_actuel()
    if taille_du_portfolio * 2 >= taille_positions:  # le meilleur palier pour l'instant c'est 2
        taille_positions = round(10 * taille_du_portfolio / 4, 2)
        modifier_palier_actuel(taille_positions)
    return taille_positions


def choix_position():
    table = extraction(determine_debut_des_donnees())
    prix_actuel = table["Close"].iloc[-1]
    table = strategie_a_appliquer.calcul_indicateurs(table)
    table = enleve_debut_des_donnees(table)
    table = enleve_bougie_non_terminee(table)
    return strategie_a_appliquer.signal(table), determine_taille_position() / prix_actuel


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
