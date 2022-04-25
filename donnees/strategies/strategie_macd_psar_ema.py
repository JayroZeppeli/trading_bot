from donnees.strategies.indicateurs import macd, sar, ema


nom = "Stratégie MACD"

longueurs_macd = [12, 26, 9]
longueur_ema = 200
pourcentage_take_profit = 0.03
pourcentage_stop_loss = 0.015


def calcul_indicateurs(table):
    table = macd.calcul_macd(table, longueurs_macd[0], longueurs_macd[1], longueurs_macd[2])
    table = sar.calcul_psar(table)
    table = ema.calcul_ema(table, longueur_ema, "EMA 200")
    return table


def signal(table):
    prix_actuel = table["Close"].iloc[-1]
    valeur_histogramme = table["MACD"].iloc[-1] - table["Signal"].iloc[-1]
    valeur_ema = table["EMA 200"].iloc[-1]
    valeur_psar = table["PSAR"].iloc[-1]
    if prix_actuel > valeur_ema and prix_actuel > valeur_psar and valeur_histogramme > 0:
        return True, True, prix_actuel*(1+pourcentage_take_profit), prix_actuel*(1-pourcentage_stop_loss)
    if prix_actuel < valeur_ema and prix_actuel < valeur_psar and valeur_histogramme < 0:
        return True, False, prix_actuel * (1 - pourcentage_take_profit), prix_actuel * (1 + pourcentage_stop_loss)
    return False, None, None, None
