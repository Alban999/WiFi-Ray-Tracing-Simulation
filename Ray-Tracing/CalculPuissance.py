"""

 FICHIER S'OCCUPANT DE TOUS LES CALCULS AFIN DE DETERMINER LA PUISSANCE

"""

import cmath as cm
from OperationsSpaciales import *
from CreateMapElements import wallListe, listeCellules, nbreCellX, nbreCellY
import matplotlib.pyplot as p


def coefReflexPerp(resMur, aI, aT):
    """
    :param resMur: Résistance du mur
    :param aI: Angle d'incidence
    :param aT: Angle de transmission
    :return: Coefficient de reflexion perpendiculaire
    """
    z1 = m.sqrt(muO/epsO)
    z2 = resMur
    return (z2*m.cos(aI)-z1*m.cos(aT))/(z2*m.cos(aI)+z1*m.cos(aT))


def coefficientTransmitionCalcul(wall, point1, point2):
    """
    :param wall: mur par lequel le rayon passe
    :param point1: point 1 du segment intersectant le mur
    :param point2: point 2 du segment intersectant le mur
    :return: Renvoie le coefficient de transmission
    """
    aI = calculeAngleIncident(point1, point2, wall)
    aT = calculeAngleTransmit(aI, epsO,wall.eps)
    epsTilde = complex(wall.eps, -wall.sigma/puls)
    wall.setResistance(epsTilde)
    refCoef = coefReflexPerp(wall.resistance, aI, aT)
    beta = puls/c
    s = wall.width/m.cos(aT)
    # gamma = A + jB
    A = puls * m.sqrt(muO * wall.eps / 2) * (m.sqrt(1 + (wall.sigma / (puls * wall.eps)) ** 2) - 1) ** 0.5
    B = puls * m.sqrt(muO * wall.eps / 2) * (m.sqrt(1 + (wall.sigma / (puls * wall.eps)) ** 2) + 1) ** 0.5
    gamma = complex(A,B)
    return ((1-refCoef**2)*cm.exp(-gamma*s))/(1-refCoef**2*cm.exp(-2*gamma*s)*cm.exp(complex(0,2*beta*s*m.sin(aT)*m.sin(aI))))

def coefficientReflexionCalcul(wall, point1, point2):
    """
    :param wall: mur par lequel le rayon passe
    :param point1: point 1 du segment intersectant le mur
    :param point2: point 2 du segment intersectant le mur
    :return: Renvoie le coefficient de réflexion
    """
    # Calcul du coefficient de reflexion
    aI = calculeAngleIncident(point1, point2, wall)
    aT = calculeAngleTransmit(aI, epsO, wall.eps)
    epsTilde = complex(wall.eps, -wall.sigma / puls)
    wall.setResistance(epsTilde)
    refCoef = coefReflexPerp(wall.resistance, aI, aT)
    beta = puls/c
    s = wall.width / m.cos(aT)
    #gamma = A + jB
    A = puls * m.sqrt(muO * wall.eps / 2) * (m.sqrt(1 + (wall.sigma / (puls * wall.eps)) ** 2) - 1) ** 0.5
    B = puls * m.sqrt(muO * wall.eps / 2) * (m.sqrt(1 + (wall.sigma / (puls * wall.eps)) ** 2) + 1) ** 0.5
    gamma = complex(A, B)

    num = (1-refCoef**2)*refCoef*cm.exp(-2*gamma*s)*cm.exp(complex(0,2*beta*s*m.sin(aT)*m.sin(aI)))
    den = 1-refCoef**2*cm.exp(complex(0,2*beta*s*cm.sin(aT)*cm.sin(aI)))
    return refCoef+num/den


def calculChampE(coefT, dist):
    """
    :param coefT: coefficient total (multiplication des différents coefficients s'il y a eu réflexion ou transmission)
    :param dist: distance de l'émetteur au récepteur
    :return: renvoie le champ E multiplié par la hauteur de l'antenne
    """
    # Calcul de champ électrique
    he = -c / f / m.pi
    beta = puls / c
    if (dist == 0):
        dist = 0.15
    E = coefT * m.sqrt(60 * GTX * PTX) * cm.exp(complex(0, -beta * dist)) / dist
    return he*E

def puissanceZoneLocale(coefT, dist):
    """
    :param coefT: coefficient total (multiplication des différents coefficients s'il y a eu réflexion ou transmission)
    :param dist: distance de l'émetteur au récepteur
    :return: renvoie le module au carré du champ multiplié par différents facteur (approximation zone locale)
    """
    # Calcul de de la puissance par l'approximation des zones locals
    he = -c/f/m.pi
    beta = puls / c
    if(dist == 0):
        dist = 0.15
    E = coefT * m.sqrt(60 * GTX * PTX) * cm.exp(complex(0, -beta * dist)) / dist
    return 1/(8*Ra)*abs((he*E))**2

def puissanceTotal(emetteur, zoneLocale):
    """
    :param emetteur: variable contenant l'émetteur
    :param zoneLocale: boolean qui nous dit si on utilise la formule en zone locale ou non
    :return: pas de return. Stock la puissance calculée dans l'attribut puissance de la cellule
    """
    for cell in listeCellules:
        coefT = 1
        [x, y] = cell.getPos()
        coefT *=ReflTransFonct(emetteur, x, y)
        dist = distCalcul(emetteur.getPos(), [x,y])
        if(zoneLocale):
            puis = puissanceZoneLocale(coefT, dist)
            cell.setPuissance(puis)
        else:
            champE = calculChampE(coefT, dist)*cm.exp(complex(0,emetteur.phase))
            cell.setChampE(champE)


def conversionDebitBinaire(puissance):
    """
    :param puissance: puissance
    :return: renvoie la conversion en débit binaire de la puissance en Mb/s
    """
    return 379/31*puissance+32752/31


def ReflTransFonct(emetteur, x, y):
    """
    :param emetteur: emetteur
    :param x: position en x de la cellule
    :param y: position en y de la cellule
    :return: renvoie le coefficient global
    """
    global showRayon #Boolean indiquant si on veut afficher les rayons ou non
    interBis = 0
    interBisBis = 0
    interMemory = list()
    interMemoryBis = list()
    xlist = list()
    ylist = list()
    coefTBisBis = 1
    nR = len(emetteur.getListeMurs())
    mur = 1
    oldMur = 1
    [x2, y2] = emetteur.getPos()[:]
    [x1, y1] = [x, y][:]
    listMurs = emetteur.getListeMurs()

    while(nR>0):
        if(len(listMurs)!=1):
            oldMur = listMurs[nR - 2]
        mur = listMurs[nR - 1]
        inter = intersectionCalcul(mur.posDebut, mur.posFin, [x1, y1], [x2, y2])
        if (inter != 0):
            [xi, yi] = inter[:]

            coefTBisBis *= coefficientReflexionCalcul(mur, [x1, y1], [xi, yi])

            #Afficher les rayons
            if([x, y] == [8.5, 5.5] and len(emetteur.getListeMurs())==2 and showRayon):
                xlist.extend([x1, xi])
                ylist.extend([y1, yi])

            for wall in wallListe:
                if(interBis!=0):
                    interMemory = interBis[:]
                interBis = intersectionCalcul(wall.posDebut, wall.posFin, [x1, y1], [xi, yi])
                if (wall != mur and wall!= oldMur and interBis != 0 and interBis!=interMemory):
                    coefTBisBis *= coefficientTransmitionCalcul(wall, [x1, y1], interBis)
            [x1, y1] = inter[:]
            [x2, y2] = calculSymetrie(mur, [x2, y2])[:]

        else:
            coefTBisBis = 0
            break
        nR-=1

    if(nR==0):
        for wall in wallListe:
            if(interBisBis!=0):
                interMemoryBis = interBisBis[:]
            interBisBis = intersectionCalcul(wall.posDebut, wall.posFin, [x1, y1], [x2, y2])
            if (wall != mur and interBisBis != 0 and interBisBis!=interMemoryBis):
                coefTBisBis *= coefficientTransmitionCalcul(wall, [x1, y1], interBisBis)

    # Afficher les rayons
    if(coefTBisBis!=0 and [x, y] == [8.5, 5.5] and len(emetteur.getListeMurs())==2 and showRayon):
        xlist.extend([x1, x2])
        ylist.extend([y1, y2])
        p.plot(xlist, ylist, color='k', linewidth=1)
        showRayon = False

    return coefTBisBis

def makeListeGraph(listeCellules, boolDebitBin, zoneLocale):
    """
    :param listeCellules: une liste contenant toutes les cellules
    :param boolDebitBin: boolean indiquant si on calcule le débit binaire ou la puissance en dBm
    :param zoneLocale: boolean indiquant si on utilise la formule de la puissance en zone locale ou non
    :return: renvoie la liste qui contient tous les données pour afficher la map
    """
    bigListe = list()
    for j in range(nbreCellY):
        smallListe = list()
        for i in range(nbreCellX):
            cell = listeCellules[i + j*nbreCellX]
            if(not zoneLocale):
                puis = 1 / (8 * Ra) * abs(cell.champE) ** 2
                cell.setPuissance(puis)
            power = 10 * m.log10(cell.puissance * 1000)
            if(boolDebitBin):
                smallListe.append(conversionDebitBinaire(power))
            else:
                smallListe.append(power)
        bigListe.append(smallListe)
    return bigListe

# Définition des constantes
muO = 4*m.pi*10**(-7); epsO = 8.854*10**(-12)

showRayon = False # Affichage du rayon réflechi oui ou non

Ra = 73; GTX = m.sqrt(muO/epsO)/(m.pi*Ra); PTX = 0.1; f = 5*10**(9); c = 299792458

puls = 2 * m.pi * f
