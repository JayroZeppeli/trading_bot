import matplotlib.pyplot as plt

from donnees.strategies.indicateurs import ema


def calcul_macd(table, longueur_rapide, longueur_lente, longueur_signal):
    table = ema.calcul_ema(table, longueur_rapide, "Fast")
    table = ema.calcul_ema(table, longueur_lente, "Slow")
    table["MACD"] = table["Fast"] - table["Slow"]
    table = ema.calcul_ema(table, longueur_signal, "Signal", "MACD")
    return table


def observer_macd(debut):
    from demarrage.parametres import nb_de_bougie_par_jour
    from donnees.extracteur_de_donnees import extraction
    table_indicateurs = ["MACD", "Signal"]
    table = extraction(debut)
    table = calcul_macd(table, 12, 26, 9)
    table = table.iloc[(14*nb_de_bougie_par_jour):]
    for indicateur in table_indicateurs:
        plt.plot(table["Close Time"], table[indicateur])
    plt.show()
