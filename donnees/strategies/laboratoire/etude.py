from automate.parametres import strategie_a_appliquer, symboles_existants
from donnees import extracteur_de_donnees, trader

portfolio_de_depart = 4000
portfolio = portfolio_de_depart
taille_des_positions_en_dollars = round(10 * portfolio / 4, 2)


date_de_debut = '2021-01-01'  # Enlever 14 jours pour l'établissement des moyennes

marge_supposee = 10
nombre_de_tour_a_skip = 0


def etudiant(symbole_a_tester, affiche=True):
    global portfolio
    global taille_des_positions_en_dollars
    if affiche:
        print("Lancement de l'étude.\nCréation de la table...")
    table_sans_indicateur = extracteur_de_donnees.extraction_de_test(symbole_a_tester, date_de_debut)
    table = strategie_a_appliquer.calcul_indicateurs(table_sans_indicateur)
    table = trader.enleve_debut_des_donnees(table)
    stop_loss, take_profit = 0, 0
    en_position, sens, trade_ambitieux = False, None, None
    trades = []
    indecis = 0
    for indice in range(len(table)):
        if portfolio * 2 >= taille_des_positions_en_dollars:  # le meilleur palier pour l'instant c'est 2
            taille_des_positions_en_dollars = round(10 * portfolio / 4, 2)
        table_coupee = table.head(indice)
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
                # booléen qui détermine si le take profit et le stop loss ont été touchés en même temps
                bool_sl = plus_bas < stop_loss
                bool_tp = plus_haut > take_profit
                bool_tp_et_sl = bool_sl and bool_tp
            else:
                bool_sl = plus_haut > stop_loss
                bool_tp = plus_bas < take_profit
                bool_tp_et_sl = bool_sl and bool_tp
            if bool_tp_et_sl:
                en_position = False
                indecis += 1
            elif bool_sl:
                perte_en_pourcentage = strategie_a_appliquer.pourcentage_stop_loss
                perte_en_dollars = taille_des_positions_en_dollars * perte_en_pourcentage
                if affiche:
                    print(f"Stop loss atteint le {table_coupee['Open Time'].iloc[-1]}, à {stop_loss}, perte de {perte_en_dollars}$.. ")
                portfolio -= perte_en_dollars
                en_position = False
                trades.append(-1)
            elif bool_tp:
                gain_en_pourcentage = strategie_a_appliquer.pourcentage_take_profit
                gain_en_dollars = taille_des_positions_en_dollars * gain_en_pourcentage
                if affiche:
                    print(f"Take profit atteint le {table_coupee['Close Time'].iloc[-1]} à {take_profit}, gain de {gain_en_dollars}$.")
                portfolio += gain_en_dollars
                en_position = False
                trades.append(1)
    print(f"{indecis} trades indécis où le tp et le sl ont été touché sur la même bougie.")
    gain_total = round(portfolio - portfolio_de_depart, 2)
    return gain_total, trades


def statistiques(table_des_trades, rien_afficher_du_tout=False):
    victoire, total = 0, 0
    nb_defaites_de_suite, nb_defaites_de_suite_maximum = 0, 0
    for trade in table_des_trades:
        total += 1
        if trade == 1:
            victoire += 1
            if nb_defaites_de_suite > nb_defaites_de_suite_maximum:
                nb_defaites_de_suite_maximum = nb_defaites_de_suite
            nb_defaites_de_suite = 0
        else:
            nb_defaites_de_suite += 1
    winrate = round(victoire / total * 100, 2)
    if not rien_afficher_du_tout:
        print(f"\nWinrate de {winrate}%.\n{victoire} victoires pour {total - victoire} défaites.\n"
              f"Un total de {total} trades.\n{nb_defaites_de_suite_maximum} défaites de suites maximum.")
    return winrate, nb_defaites_de_suite


def resultats(symbole_a_tester, affiche=False, rien_afficher_du_tout=False):
    gain, table_des_trades = etudiant(symbole_a_tester, affiche)
    if not rien_afficher_du_tout:
        print(f"Les revenus en appliquant la {strategie_a_appliquer.nom}\n"
              f"avec un capital de {portfolio_de_depart}$\n"
              f"du {date_de_debut} à aujourd’hui\n"
              f"auraient été de {gain}$")
    winrate, defaites_de_suite = statistiques(table_des_trades, rien_afficher_du_tout)
    return gain, winrate


def doctorat():
    table_resultats = {}
    for symbole_a_tester in symboles_existants:
        table_resultats[symbole_a_tester] = resultats(symbole_a_tester, rien_afficher_du_tout=True)
    return table_resultats


def analyse_des_resultats():
    dictionnaire_des_resultats = {'ETH': (31.5, 36.62), 'BTC': (-4.5, 32.76), 'BNB': (4.5, 33.85), 'TRX': (51.0, 40.51), 'LINK': (51.0, 37.12),
     'XLM': (49.5, 38.03), 'ADA': (43.5, 36.64), 'XMR': (3.0, 33.55), 'DASH': (24.0, 34.97), 'ATOM': (19.5, 34.59),
     'BAT': (43.5, 36.36), 'ALGO': (7.5, 33.87), 'DOGE': (27.0, 35.48), 'SNX': (66.0, 36.79), 'SUSHI': (25.5, 34.89),
     'SOL': (6.0, 33.71), 'BCH': (0.0, 33.33), 'DOT': (15.0, 34.45), 'VET': (34.5, 35.46), 'ETC': (-1.5, 33.24),
     'LTC': (21.0, 35.16), 'XRP': (46.5, 37.77), 'EOS': (25.5, 35.42), 'THETA': (48.0, 36.04), 'AVAX': (54.0, 36.78),
     'UNI': (-22.5, 31.86), 'AAVE': (73.5, 37.85), 'LUNA': (10.5, 33.94)}
    classement = [(None, 0)]
    for symbole_actuel in dictionnaire_des_resultats:
        for indice in range(len(classement)):
            element = classement[indice]
            if dictionnaire_des_resultats[symbole_actuel][0] > element[1]:
                classement.insert(indice, (symbole_actuel, dictionnaire_des_resultats[symbole_actuel][0]))
                break
            classement.append((symbole_actuel, dictionnaire_des_resultats[symbole_actuel][0]))
    return classement
