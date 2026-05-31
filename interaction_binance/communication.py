from binance.client import Client
from binance.enums import *

from demarrage import parametres
from interaction_binance import gestion_des_positions

api_key = ''  # you have to put your own API keys
api_secret = ''

client = Client(api_key, api_secret)
symbole = parametres.symbole_a_utiliser + 'USDT'


# client.API_URL = "https://fapi.binance.com"


def determine_echange_stables(paire_stable):
    liste_symboles = client.get_all_isolated_margin_symbols()
    informations_compte = client.get_margin_account()
    symboles_arbitrage = [None]
    sens = None
    quantite = None
    symbole_arbitrage = None
    for symbole_recherche in liste_symboles:
        if paire_stable[0] in symbole_recherche['symbol'] and paire_stable[1] in symbole_recherche['symbol']:
            symboles_arbitrage += [symbole_recherche['symbol']]
    for symbole_arbitrage_test in symboles_arbitrage:
        if symbole_arbitrage_test == paire_stable[0] + paire_stable[1]:
            symbole_arbitrage = symbole_arbitrage_test
            sens = SIDE_SELL
        elif symbole_arbitrage_test == paire_stable[1] + paire_stable[0]:
            symbole_arbitrage = symbole_arbitrage_test
            sens = SIDE_BUY
    if symbole_arbitrage is None:
        raise Exception("Impossible de trouver la paire de stables.")
    for asset in informations_compte['userAssets']:
        if asset['asset'] == paire_stable[0]:
            quantite = asset['free']
    if quantite is None:
        raise Exception("Impossible de trouver les stables dans les assets du compte.")
    return symbole_arbitrage, sens, quantite


def obtenir_coins_dispo_marge():
    coins = ["ALPACA", 'QNT', "ANC", "GMT", "AAVE", "ADA", "ACA", "1INCH", "EGLD", "AUDIO"]
    assets = client.get_all_isolated_margin_symbols()
    for asset in assets:
        if asset["base"] not in coins and "DOWN" not in asset["base"]:
            coins.append(asset["base"])
    return coins


def ordres_ouverts():
    return client.futures_get_open_orders()


def fermer_tout_les_ordres():
    client.futures_cancel_all_open_orders(symbol=symbole)


def ouvrir_position(sens, take_profit, stop_loss, quantite):  # long = True et short = False
    client.futures_change_leverage(symbol=symbole, leverage=parametres.effet_de_levier)
    gestion_des_positions.entre_en_position(client, sens, symbole, take_profit, stop_loss, quantite)


def achat_revente_arbitrage(paire_stable, coin, quantite):
    stable_1, stable_2 = paire_stable[0], paire_stable[1]
    try:
        client.get_margin_symbol(symbol=coin+stable_1)
        client.get_margin_symbol(symbol=coin + stable_2)
    except Exception:
        return
    client.create_margin_loan(asset=coin, amount=quantite)
    client.create_margin_order(symbol=coin+stable_1, side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                               quantity=quantite)
    symbole_entre_stables, sens_entre_stables, quantite_stables = determine_echange_stables(paire_stable)
    client.create_margin_order(symbol=symbole_entre_stables, side=sens_entre_stables, type=ORDER_TYPE_MARKET,
                               quantity=round(float(quantite_stables), 2))
    client.create_margin_order(symbol=coin+stable_2, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                               quantity=quantite)
    client.repay_margin_loan(asset=coin, amount=quantite)



