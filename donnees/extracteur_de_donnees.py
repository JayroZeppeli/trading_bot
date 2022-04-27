import pandas as pd
from binance.client import Client
from automate import parametres
import mplfinance as mpf
from datetime import timedelta

# url = f"https://data.binance.vision/data/spot/daily/klines/{symbole}/{timeframe}/{symbole}-{timeframe}-{date_fin}.zip"

api_key = 'LC5RxUjNaW9yI66wCQ4uxP2zvAuS1rlhmBTIO5IUFXskF7QwlegWgLaaBwUviw4P'
api_secret = 'q8wPz0g090alkOEPt11QTliaNc9gsQRTHEgYohbj8zKDczipgWmxYhcrKSY0weLG'

client = Client(api_key, api_secret)
symbole = parametres.symbole_a_utiliser + 'USDT'
timeframe = parametres.time_frame_a_utiliser
colonnes = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
            'Number of Trades', 'TB base AV', 'TB quote AV', 'Ignore']  # TB = Taker Buy, AV = Asset Volume


def graphique(table):
    nombre_de_bougies = parametres.nb_jours_initialisation_indicateurs
    mpf.plot(table.set_index(colonnes[6]).tail(nombre_de_bougies*6), type='candle')


def mise_en_page(table):
    """Met les éléments de la table dans un format correct"""
    table.columns = colonnes
    colonnes_au_format_numeriques = [colonnes[i] for i in list(range(1, 6)) + [7, 9, 10]]
    table[colonnes_au_format_numeriques] = table[colonnes_au_format_numeriques].apply(pd.to_numeric, axis=1)
    table['Open Time'] = pd.to_datetime(table['Open Time'] / 1000, unit='s') + timedelta(hours=2)  # Car décalage horaire de 2h mais les données sont bien en temps réel
    table['Close Time'] = pd.to_datetime(table['Close Time'] / 1000, unit='s') + timedelta(hours=2)


def extraction(date_debut):
    donnee_brut = client.get_historical_klines(symbole, timeframe, date_debut)  # Client.KLINE_INTERVAL_4HOUR permet de voir le format correct
    table = pd.DataFrame(donnee_brut)
    mise_en_page(table)
    return table
