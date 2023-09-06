"""

 MENU GERANT LES DIFFERENTES FONCTIONNALITES

"""

# Importation des fichiers et bibliothèsques nécessaire
from matplotlib import colors
from CreateMapElements import listEmetImageTot, mapSizeX, mapSizeY, listOpti, modeOptimisation
from CalculPuissance import *

def optimisation(listeDatas, seuilleHaut, seuilleBas):
    """
    :param listeDatas: la liste contenant toutes les données de puissances pour chaque position d'émetteur possible
    :param seuilleHaut: le seuille au dessus du quel la puissance sature
    :param seuilleBas:le seuille en dessous du quel la puissance sature
    :return: renvoie la liste contenant les données de l'émetteur ayant la meilleur position
    """
    totaleMax = -10000000000000 # Totale de puissance de départ
    elementPos = -1
    elementPosMemory = 0
    for sousListeData in listeDatas:
        elementPos += 1
        totale = 0
        for sousSousListe in sousListeData:
            for elem in sousSousListe:
                if(elem>seuilleHaut):
                    totale+=seuilleHaut
                elif(elem<seuilleBas):
                    totale+=seuilleBas
                else:
                    totale+=elem
        if(totale==seuilleHaut*len(sousListeData)*len(sousSousListe)):
            # Cas où on a du réseau partout dans la map. On arrête la fonction et on renvoie la position
            print("Zone déjà parfaite")
            break
        if(totale>totaleMax):
            totaleMax = totale
            elementPosMemory = elementPos

    return elementPosMemory



# MAIN

# VARIABLES DE BASE

# Définition des bornes pour l'optimisation
seuilleOptHaut = -51
seuilleOptBas = -82

# Zone local oui ou non
zoneLocale = True

# Option débit binaire ou non
booleanDebitBin = False

# Zone de couverture
zoneDeCouverture = False

# Définition du débit minimum et maximum demandé
borneMinDébit1 = 54; borneMinDébit2 = 454; borneMin = -82

# Définition de la palette de couleur
name = 'jet'; namePaletteCouleur = "Puissance [dBm]"

# Définition de la borne de saturation / Puissance minimum et maximum
borneMinPuissance1 = -82; borneMinPuissance2 = -51

borneInf = -1000; borneSup = 1000

# Conversion en binaire si demandé
if(booleanDebitBin):
    borneMin = conversionDebitBinaire(borneMin)
    borneMin1 = borneMinDébit1
    borneMin2 = borneMinDébit2
    #Définition de la palette de couleur pour le débit binaire
    name = 'inferno'
    namePaletteCouleur = "Débit Binaire [Mb/s]"
else:
    borneMin1 = borneMinPuissance1
    borneMin2 = borneMinPuissance2

# Définition du graphe, de ces axes, ...
fig = p.figure()
fig.canvas.set_window_title('Projet ray-tracing')

p.xlabel('x [m]', fontsize=12)
p.ylabel('y [m]', fontsize=12)

# Calcul des données
avancement = 1
if(modeOptimisation):
    # Parcourir différents émetteurs possible pour trouver la meilleur position possible
    listDataTot = list()
    for listElem in listOpti:
        for cell in listeCellules:
            cell.resetPuissance(0)

        listeData = list()
        for emet in listElem:
            totalElem = len(listElem)*len(listOpti)
            puissanceTotal(emet, zoneLocale)
            print(str(avancement) + "/" + str(totalElem)) # Affiche le chargement du programme
            avancement += 1

        # Création de la liste contenant les donées
        listeData = makeListeGraph(listeCellules, booleanDebitBin, zoneLocale)
        listDataTot.append(listeData[:])
    posNum = optimisation(listDataTot, seuilleOptHaut, seuilleOptBas)
    listeData = listDataTot[posNum]

else:
    for emet in listEmetImageTot:
        puissanceTotal(emet, zoneLocale)
        print(str(avancement)+"/"+str(len(listEmetImageTot))) # Affiche le chargement du programme
        avancement+=1

    # Création de la liste contenant les donées
    listeData = makeListeGraph(listeCellules, booleanDebitBin, zoneLocale)

if(zoneDeCouverture):
    # Affichage de la zone de couverture
    nameFonction = "Zone de couverture"
    cmap = colors.ListedColormap(['gray', "orange", 'red'])
    bounds = [borneInf, borneMin1, borneMin2,borneSup]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    img = p.imshow(listeData, interpolation='none', origin='lower', cmap=cmap, norm=norm, extent=[0, mapSizeX, 0, mapSizeY])
    cbar = p.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[borneMin1, borneMin2])
    cbar.ax.set_ylabel(namePaletteCouleur, rotation=270, labelpad=25)
else:
    # Affichage de la map
    nameFonction = "Ray-Tracing"
    p.imshow(listeData,interpolation='none',cmap=p.get_cmap(name), origin='lower', vmin = borneMin, extent=[0, mapSizeX, 0, mapSizeY])

    cbar = p.colorbar()
    cbar.ax.set_ylabel(namePaletteCouleur, rotation=270, labelpad=25)


# Affichage des murs
for elem in wallListe:
    p.plot([elem.posDebut[0], elem.posFin[0]], [elem.posDebut[1], elem.posFin[1]], color='k', linewidth=3)

p.title(nameFonction, y=1.02)
p.show()


