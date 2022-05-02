from interaction_binance.communication import obtenir_coins_dispo_marge


paires_stables_de_paires_stables = []

liste_stable = ['USDT', "USDC", 'BUSD', 'DAI', "UST"]

for premier_stable in liste_stable:
    for second_stable in liste_stable:
        if premier_stable != second_stable and [second_stable, premier_stable] not in paires_stables_de_paires_stables:
            paires_stables_de_paires_stables.append([premier_stable, second_stable])

coins = obtenir_coins_dispo_marge()

arbitrage_taille_des_positions_en_dollars = 13

seuil_de_rentabilite_pourcentage = 0.25/100  # Les frais étant de 0.1/24 + 0.075 * 3

time_frame_arbitrage = '1m'

temps_entre_chaque_check_en_min = 5

