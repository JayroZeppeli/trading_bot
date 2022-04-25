from donnees import extracteur_de_donnees
from automate.parametres import strategie_a_appliquer, taille_des_positions_en_dollars


date_de_debut = '2022-01-01'  # Enlever 14 jours pour l'établissement des moyennes

marge_supposee = 10
nombre_de_tour_a_skip = 0


def doctorat():
    performance = {0: {}, 1: {}}
    global date_de_debut
    for j in range(2):
        for i in range(1, 10):
            date_de_debut = f'202{j}-0{i}-01'
            performance[j][i] = etudiant()
        for i in range(10, 13):
            date_de_debut = f'202{j}-{i}-01'
            performance[j][i] = etudiant()
    return performance


def etudiant(affiche=True):
    if affiche:
        print("Lancement de l'étude.\nCréation de la table...")
    table_sans_indicateur = extracteur_de_donnees.extraction(date_de_debut)
    table = strategie_a_appliquer.calcul_indicateurs(table_sans_indicateur)
    gain_total, stop_loss, take_profit = 0, 0, 0
    en_position, sens, trade_ambitieux = False, None, None
    skip = []
    trades = []
    for i in range(15, len(table)):
        if i in skip:
            continue
        table_coupee = table.head(i)
        if not en_position:
            signal, sens, take_profit, stop_loss = strategie_a_appliquer.signal(table_coupee)
            if signal:
                en_position = True
                if affiche:
                    print(f"Je rentre en position {['short', 'long'][sens]} le {table_coupee['Close Time'].iloc[-1]} à {table_coupee['Close'].iloc[-1]}$")
            else:
                if affiche:
                    print(".")
        else:
            plus_bas, plus_haut = table_coupee["Low"].iloc[-1], table_coupee["High"].iloc[-1]
            if sens:
                bool_tp_et_sl = plus_bas < stop_loss and plus_haut > take_profit
                bool_sl = plus_bas < stop_loss
                bool_tp = plus_haut > take_profit
            else:
                bool_tp_et_sl = plus_bas < take_profit and plus_haut > stop_loss
                bool_sl = plus_haut > stop_loss
                bool_tp = plus_bas < take_profit
            if bool_tp_et_sl:
                print(f"Take profit et Stop loss touché sur la même bougie le {table_coupee['Close Time'].iloc[-1]}...")
                en_position = False
                skip += [i + nombre_de_tour_a_skip]
            elif bool_sl:
                perte_en_pourcentage = strategie_a_appliquer.pourcentage_stop_loss
                perte_en_dollars = taille_des_positions_en_dollars * perte_en_pourcentage
                if affiche:
                    print(f"Stop loss atteint le {table_coupee['Open Time'].iloc[-1]}, à {stop_loss}, perte de {perte_en_dollars}$.. ")
                gain_total -= perte_en_dollars
                en_position = False
                skip += [i + nombre_de_tour_a_skip]
                trades.append(-1)
            elif bool_tp:
                gain_en_pourcentage = strategie_a_appliquer.pourcentage_take_profit
                gain_en_dollars = taille_des_positions_en_dollars * gain_en_pourcentage
                if affiche:
                    print(f"Take profit atteint le {table_coupee['Close Time'].iloc[-1]} à {take_profit}, gain de {gain_en_dollars}$.")
                gain_total += gain_en_dollars
                en_position = False
                skip += [i + nombre_de_tour_a_skip]
                trades.append(1)
    return gain_total, trades


def resultats(affiche=False):
    gain, tout_trades = etudiant(affiche)
    print(f"\n\nLes revenus en appliquant la {strategie_a_appliquer.nom}\n"
          f"avec un capital de {taille_des_positions_en_dollars/marge_supposee}$\n"
          f"du {date_de_debut} à aujourd’hui\n"
          f"auraient été de {gain}$")
    victoire, total = 0, 0
    for trade in tout_trades:
        total += 1
        if trade == 1:
            victoire += 1
    print(f"\nWinrate de {round(victoire/total*100, 2)}%.\n{victoire} victoires pour {total-victoire} défaites.\nUn total de {total} trades.\n")


resultats()
