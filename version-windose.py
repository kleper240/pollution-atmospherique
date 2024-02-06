

import pandas as pd
import matplotlib.pyplot as plt
from time import *


def var(annee= input("rentrez l'année: "), mois= input("rentrez le mois : "), jour = input("rentrez le jour: ")):
    # On utilise ces valeurs pour créer l'URL du fichier CSV à télécharger

    url = (f"https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/{annee}/FR_E2_{annee}-{mois}-{jour}.csv")
    
    # On utilise la fonction read_csv de pandas pour lire le fichier CSV à partir de l'URL
    lire = pd.read_csv(url, sep = ";")

    
    # On sélectionne les lignes du fichier qui correspondent au site "VITRY-SUR-SEINE"
    vitry = lire[lire["nom site"]== "VITRY-SUR-SEINE"]
    # On crée une liste unique des valeurs de la colonne "Date de début" pour les lignes sélectionnées
    dates= list(set(vitry["Date de début"]))
    dates.sort()
    # On crée une liste unique des valeurs de la colonne "Polluant" pour les lignes sélectionnées
    pollu= list(set(vitry["Polluant"])) 
    pollu.sort()
    
    # On crée un dictionnaire contenant les valeurs de la colonne "valeur" pour chaque polluant
    dico = {p: list(vitry[vitry.Polluant==p].valeur) for p in pollu}

    
    # On crée un DataFrame pandas à partir du dictionnaire en utilisant les dates comme index
    dataframes = pd.DataFrame(dico, index=dates)


    print(dataframes)
    print(dataframes.describe())
    print(dataframes.plot(kind='line'))

    # Définir les seuils réglementaires pour chaque polluant
    seuils = {'NOX as NO2': 30, 'NO': 40, 'NO2': 200, 'PM10': 10, 'PM2.5': 25, 'O3': 100, 'SO2':50}

    for keys, vals in seuils.items():
        for key, val in dico.items():
            if keys == key:
                for i in range(24):
                    if vals < val[i]:
                        print(f"Alerte de dépassement de seuil réglementaire pour le polluant {keys} avec une valeur de {val[i]} le {dates[i]}")
                        sleep(1)
                        dates_id = dates.index(dates[i])
                        plt.scatter(dates_id, val[i], color = "red")
                        plt.xlabel('les dates et les heures de la journée ')
                        plt.ylabel("les valeurs ")
    plt.show()


# On appelle la fonction pour lancer le processus
var()

