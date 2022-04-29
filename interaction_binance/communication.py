from binance.client import Client
from interaction_binance import gestion_des_positions
from automate import parametres


api_key = 'LC5RxUjNaW9yI66wCQ4uxP2zvAuS1rlhmBTIO5IUFXskF7QwlegWgLaaBwUviw4P'
api_secret = 'q8wPz0g090alkOEPt11QTliaNc9gsQRTHEgYohbj8zKDczipgWmxYhcrKSY0weLG'

client = Client(api_key, api_secret)
symbole = parametres.symbole_a_utiliser + 'USDT'


# client.API_URL = "https://fapi.binance.com"


def usdt_dispo():
    return round(float(client.futures_account_balance()[6]['balance']) * 0.975, 2)


def ordres_ouverts():
    return client.futures_get_open_orders()


def fermer_tout_les_ordres():
    client.futures_cancel_all_open_orders(symbol=symbole)


def ouvrir_position(sens, take_profit, stop_loss, quantite):  # long = True et short = False
    client.futures_change_leverage(symbol=symbole, leverage=parametres.effet_de_levier)
    gestion_des_positions.entre_en_position(client, sens, symbole, take_profit, stop_loss, quantite)
