def inscrit_variations_positives_et_negatives(table):
    delta = table["Close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    return up, down


def calcul_ema_variations(up, down, longueur_rsi):
    ema_up = up.ewm(com=longueur_rsi, adjust=False).mean()  # peut être modifier variable com
    ema_down = down.ewm(com=longueur_rsi, adjust=False).mean()
    return ema_up, ema_down


def calcul_rsi_et_sma_du_rsi(table, longueur_rsi, longueur_sma, noms):
    up, down = inscrit_variations_positives_et_negatives(table)
    ema_up, ema_down = calcul_ema_variations(up, down, longueur_rsi)
    rs = ema_up / ema_down
    table[noms[0]] = 100 - (100 / (1 + rs))
    table[noms[1]] = table[noms[0]].rolling(window=longueur_sma).mean()
    return table
