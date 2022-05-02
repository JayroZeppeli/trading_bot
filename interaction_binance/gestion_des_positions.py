from binance.enums import *

from demarrage.parametres import precision_apres_virgule_du_coin, distance_entre_stop_et_limit_pour_stop_loss
from logs.scribe import ecrit_rapport


def entre_en_position(client, sens, symbole, take_profit, stop_loss, quantite):
    entree = [SIDE_SELL, SIDE_BUY][sens]
    sortie = [SIDE_BUY, SIDE_SELL][sens]
    quantite = round(quantite, precision_apres_virgule_du_coin)
    market_order = client.futures_create_order(symbol=symbole,
                                               side=entree,
                                               type=ORDER_TYPE_MARKET,
                                               quantity=quantite)
    ecrit_rapport(f'Position {["short", "long"][sens]} au cours actuel ouverte.')
    take_profit, stop_loss = round(take_profit, 2), round(stop_loss, 2)
    ordre_stop_limite_perte = client.futures_create_order(symbol=symbole,
                                                          side=sortie,
                                                          type=FUTURE_ORDER_TYPE_STOP,
                                                          timeInForce=TIME_IN_FORCE_GTC,
                                                          quantity=quantite,
                                                          stopPrice=stop_loss,
                                                          price=stop_loss + distance_entre_stop_et_limit_pour_stop_loss - (
                                                                      2 * distance_entre_stop_et_limit_pour_stop_loss * sens),
                                                          reduceOnly='true')
    ecrit_rapport(f'Stop loss placé à {stop_loss}$.')
    ordre_limite_profit = client.futures_create_order(symbol=symbole,
                                                      side=sortie,
                                                      type=FUTURE_ORDER_TYPE_LIMIT,
                                                      timeInForce=TIME_IN_FORCE_GTC,
                                                      quantity=quantite,
                                                      price=take_profit,
                                                      reduceOnly='true')
    ecrit_rapport(f'Take profit placé à {take_profit}$.')
