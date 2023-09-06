"""

OPERATIONS DANS L'ESPACE / GEOMETRIE

"""

import math as m


def distCalcul(point1, point2):
    """
    :param point1: point 1
    :param point2: point 2
    :return: renvoie la distance entre ces deux points
    """
    return m.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

def calculSymetrie(mur, posEmetteur):
    """
    :param mur: mur par lequel l'émtteur va être symétrisé
    :param posEmetteur: la position de l'émetteur
    :return: renvoie la position de l'émetteur image
    """
    positionEmetImage = [0, 0]
    if (mur.posDebut[0] == mur.posFin[0]):
        # Mur v
        positionEmetImage[0] = mur.posDebut[0] + (mur.posDebut[0] - posEmetteur[0])
        positionEmetImage[1] = posEmetteur[1]
    else:
        # Mur h
        positionEmetImage[0] = posEmetteur[0]
        positionEmetImage[1] = mur.posDebut[1] + (mur.posDebut[1] - posEmetteur[1])

    return positionEmetImage


def intersectionCalcul(murPosDebut, murPosFin, cellPos, posEmet):
    """
    :param murPosDebut: position de la première extrémité du mur
    :param murPosFin: position de la deuxième extrémité du mur
    :param cellPos: position de la cellule
    :param posEmet: position de l'émetteur
    :return: renvoie l'intersection s'il y en a une sinon renvoie 0
    """
    x = 0; y = 0
    sortie = 1 # inter (1) ou pas (0)
    res1 = paramDroites(murPosDebut, murPosFin)
    res2 = paramDroites(cellPos, posEmet)
    if(res1[0]):
        if(res2[0]):
            sortie = 0
        x = res1[2]
        y = res2[1]*x + res2[2]
    elif(res2[0]):
        x = res2[2]
        y = res1[1] * x + res1[2]
    elif(res2[1]==res1[1]):
        sortie = 0
    else:
        x = (res2[2]-res1[2])/(res1[1]-res2[1])
        y = res1[1]*x + res1[2]

    if(sortie):
        if (not (interSurSegment(cellPos, posEmet, [x,y]) and interSurSegment(murPosDebut, murPosFin, [x,y]))):
            # Inter pas sur le segment
            sortie = 0
    if(sortie):
        return [x, y]

    return sortie

def interSurSegment(p1Bis, p2Bis, pInter):
    """
    :param p1Bis:  point 1
    :param p2Bis: point 2
    :param pInter: point d'intersection entre ces 2 points
    :return: renvoie si oui ou non l'intersection est sur le mur en question, c-à-d sur le segment [p1Bis, p2Bis]
    """
    p1 = p1Bis[:]
    p2 = p2Bis[:]
    sortie = 1
    if(p1[0] == p2[0]):
        if(p2[1]<p1[1]):
            stock = p1[1]
            p1[1] = p2[1]
            p2[1] = stock
        if(pInter[1]<p1[1] or pInter[1]>p2[1]):
            sortie = 0
    else:
        if(p2[0]<p1[0]):
            stock = p1[0]
            p1[0] = p2[0]
            p2[0] = stock
        if (pInter[0] < p1[0] or pInter[0] > p2[0]):
            sortie = 0

    return sortie



def paramDroites(p1, p2):
    """
    :param p1: point 1
    :param p2: point 2
    :return: renvoie res = true si la droite est verticale sinon False et la pente et l'oordonnée à l'origine de la droite
    """
    res = False
    a = 0; b = 0

    if (p1[0]==p2[0]):
        res = True
        b = p1[0]
    else:
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - a * p1[0]
    return [res, a, b]



def angleEntreDeuxPoints(point1, point2):
    """
    :param point1: point 1
    :param point2: point 2
    :return: renvoie l'angle le segment [point1, point2] et la normal
    """
    if(point2[0] == point1[0]):
        angle = m.pi/2
    else:
        angle = m.atan((point2[1]-point1[1])/(point2[0]-point1[0]))

    if(angle<0):
        angle+=m.pi
    return angle

def calculeAngleTransmit(angleI, epsI, epsT):
    """
    :param angleI: angle d'incidence
    :param epsI: epsilon du milieu incident
    :param epsT: epsilon du milieu de transmission
    :return: renvoie l'angle de transmission
    """
    return m.asin(m.sqrt(epsI/epsT)*m.sin(angleI))

def calculeAngleIncident(pos1, pos2, mur):
    """
    :param pos1: position 1
    :param pos2: position 2
    :param mur: mur qui est intersecté avec le segment [pos1, pos2]
    :return: renvoie l'angle incident avec le mur
    """
    angleEntrePos = angleEntreDeuxPoints(pos1, pos2)
    angleMur = angleEntreDeuxPoints(mur.posDebut, mur.posFin) + m.pi / 2
    if (angleMur > m.pi):
        angleMur -= m.pi

    angleI = m.fabs(angleMur - angleEntrePos)

    if (angleI > m.pi / 2):
        angleI -= m.pi

    return m.fabs(angleI)