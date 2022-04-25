from binance.enums import *
from logs import scribe


def entre_en_position(client, sens, symbole, take_profit, stop_loss, quantite):
    entree = [SIDE_SELL, SIDE_BUY][sens]
    sortie = [SIDE_BUY, SIDE_SELL][sens]
    market_order = client.futures_create_order(symbol=symbole,
                                               side=entree,
                                               type=ORDER_TYPE_MARKET,
                                               timeInForce=TIME_IN_FORCE_GTC,
                                               quantity=quantite)
    scribe.ecrit_rapport(f'Je suis rentré en position {["short", "long"][sens]} au cours actuel.')
    quantite *= 0.99
    ordre_limite_profit = client.futures_create_order(symbol=symbole,
                                                      side=sortie,
                                                      type=ORDER_TYPE_LIMIT,
                                                      timeInForce=TIME_IN_FORCE_GTC,
                                                      quantity=quantite,
                                                      price=take_profit)
    scribe.ecrit_rapport(f'Take profit placé à {take_profit}$.')
    ordre_stop_limite_perte = client.futures_create_order(symbol=symbole,
                                                          side=sortie,
                                                          type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                          timeInForce=TIME_IN_FORCE_GTC,
                                                          quantity=quantite,
                                                          stop_price=stop_loss - 15 + (30 * sens),
                                                          limit_price=stop_loss)
    scribe.ecrit_rapport(f'Stop loss placé à {stop_loss}$.')
