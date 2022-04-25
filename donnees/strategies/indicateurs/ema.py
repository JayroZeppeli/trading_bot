def calcul_ema(table, longueur, nom, nom_colonne="Close"):
    table[nom] = table[nom_colonne].ewm(span=longueur).mean()
    return table
