from donnees.strategies import strategie_rsi_sma_ema, combinaison_ancienne, strategie_macd_psar_ema

raspberry = False

# non personnalisable

strategies_existantes = [strategie_rsi_sma_ema, combinaison_ancienne, strategie_macd_psar_ema]

symboles_existants = ['ETH', 'BTC']

timeframe_existants = ['4h', '30m']

fractionnement_des_heures = {'4h': [4*i for i in range(6)], '30m': [0.5*i for i in range(48)]}

premiere_bougie_de_la_journee = {'4h': 0, '30m': 0}

unite_time_frame_en_h = 0.5

nb_jours_initialisation_indicateurs = 15

nb_de_bougie_par_jour = 24 / unite_time_frame_en_h

marge_erreur_horloger_en_heure = 0.1

precision_apres_virgule_du_coin = 3

temps_avant_initialisation_nouvelle_bougie_binance_data = 0.5

distance_entre_stop_et_limit_pour_stop_loss = 1

effet_de_levier = 10

# personnalisable

strategie_a_appliquer = strategies_existantes[2]

symbole_a_utiliser = symboles_existants[0]

time_frame_a_utiliser = timeframe_existants[1]

taille_des_positions_en_dollars = 100  # en comptant la marge (qu'on suppose à *10 dans le laboratoire)

# time frame des 4h est le seul programmé pour l'instant
