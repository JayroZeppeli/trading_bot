from datetime import timedelta
import pandas as pd
from donnees.strategies.indicateurs import rsi, ema


pd.options.mode.chained_assignment = None


nom = "Stratégie RSI"
nombre_de_jours_necessaires = timedelta(days=30)
longueur_rsi = 13  # Il faut retirer 1 à la valeur que l'on souhaite
longueur_sma = 14
longueur_ema = 200
pourcentages_take_profit = [0.125, 0.2]
pourcentages_stop_loss = [0.07, 0.1]


def calcul_indicateurs(table):
    table = rsi.calcul_rsi_et_sma_du_rsi(table, longueur_rsi, longueur_sma, ["RSI", "SMA"])
    return ema.calcul_ema(table, longueur_ema, "EMA")


def signal(table):
    difference_minimale_pour_juger_breakout = 1
    prix_actuel = table["Close"].iloc[-1]
    valeur_ema = table["EMA"].iloc[-1]
    ancien_rsi, ancien_sma = table["RSI"].iloc[len(table)-2], table["SMA"].iloc[len(table)-2]
    rsi_actuel, sma_actuel = table["RSI"].iloc[len(table)-1], table["SMA"].iloc[len(table)-1]
    if ancien_rsi < ancien_sma and rsi_actuel > sma_actuel and abs(rsi_actuel - sma_actuel) > difference_minimale_pour_juger_breakout:
        take_profit, stop_loss = prix_actuel * (1 + pourcentages_take_profit[prix_actuel > valeur_ema]), prix_actuel * (1 - pourcentages_stop_loss[prix_actuel > valeur_ema])
        return True, True, take_profit, stop_loss, bool(prix_actuel > valeur_ema)
    if ancien_rsi > ancien_sma and rsi_actuel < sma_actuel and abs(rsi_actuel - sma_actuel) > difference_minimale_pour_juger_breakout:
        take_profit, stop_loss = prix_actuel * (1 - pourcentages_take_profit[prix_actuel < valeur_ema]), prix_actuel * (1 + pourcentages_stop_loss[prix_actuel < valeur_ema])
        return True, False, take_profit, stop_loss, bool(prix_actuel < valeur_ema)
    return False, None, None, None, None
