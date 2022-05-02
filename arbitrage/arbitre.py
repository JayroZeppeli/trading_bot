import time

from parametres import paires_stables_de_paires_stables, coins
from donnees import trader
from interaction_binance import communication


def parcours_des_coins():
    for coin in coins:
        for paire_stable in paires_stables_de_paires_stables:
            position, paire_stable_bon_sens, quantite = trader.choix_position_arbitrage(paire_stable, coin)
            if position:
                return True, paire_stable_bon_sens, coin, quantite
    return False, None, None, None


def main():
    while True:
        position, paire_stable, coin, quantite = parcours_des_coins()
        if not position:
            print("Pas d'opportunité sur la paire")
        else:
            print("Opportunité sur ", coin, paire_stable)
            communication.achat_revente_arbitrage(paire_stable, coin, quantite)


main()



