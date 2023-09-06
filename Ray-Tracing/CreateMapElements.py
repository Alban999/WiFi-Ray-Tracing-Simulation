"""

 FICHIER QUI S'OCCUPE DE CREER LES ELEMENTS PRESENT SUR LA MAP

"""

import Cellule as cel
import Wall as w
import Emetteur as em
from OperationsSpaciales import calculSymetrie
import math as m
import EditeurMap as edM

def creationCellules():
    """
    :return: renvoie la liste contenant toutes les cellules
    """
    listCellules = list()
    for i in range(nbreCellY):
        for j in range(nbreCellX):
            # Centré au centre de la cellule
            iReal = i / nbreCellY * mapSizeY + tailleCell / 2;
            jReal = j / nbreCellX * mapSizeX + tailleCell / 2;
            cell = cel.Cellule([jReal, iReal])
            listCellules.append(cell)
    return listCellules



def creationListeEmetteurImg(emetteur, wallListeBis):
    """
    :param emetteur: emetteur
    :param wallListeBis: la liste des murs par lesquels l'émetteur va être réfléchi
    :return: renvoie la liste de tous les émetteurs images
    """
    wallListeBis = wallListeBis[:]
    nbreMur = len(emetteur.getListeMurs())

    if(nbreMur!=0):
        wallListeBis.remove(emetteur.getListeMurs()[nbreMur-1])
    for wall in wallListeBis:
        newEmet = em.Emetteur(calculSymetrie(wall, emetteur.getPos()))
        for mur in emetteur.getListeMurs():
            newEmet.rajouteMurListe(mur)
        newEmet.rajouteMurListe(wall)
        if(nbreMur==0):
            listEmetImage.append(newEmet)  # A changer mettre juste émetteur la on le faitpour observer les pos
        else:
            if (ver(emetteur, emetteur.getListeMurs()[nbreMur - 1], wall)):
                listEmetImage.append(newEmet) #A changer mettre juste émetteur la on le faitpour observer les pos


def ver(emetteurImg, oldMur, newMur):
    """
    :param emetteurImg: emetteur image
    :param oldMur: ancien mur par lequel l'émetteur à été réfléchi
    :param newMur: nouveau mur par lequel l'émetteur va être réfléchi
    :return: renvoie si oui ou non cette emetteur image est pertinent. Si oui, il est créé. Si non, il est détruit.
    """
    if(oldMur.posDebut[1]==oldMur.posFin[1] and newMur.posDebut[1]==newMur.posFin[1]):
        dOld = emetteurImg.getPos()[1]-oldMur.posDebut[1]
        dN = newMur.posDebut[1]-oldMur.posDebut[1]
        if(dOld*dN>=0):
            return False
    if (oldMur.posDebut[0] == oldMur.posFin[0] and newMur.posDebut[0] == newMur.posFin[0]):
        dOld = emetteurImg.getPos()[0] - oldMur.posDebut[0]
        dN = newMur.posDebut[0] - oldMur.posDebut[0]
        if (dOld * dN>=0):
            return False

    return True

# Boolean disant si on se met en mode optimisation ou non
modeOptimisation = False
listOpti = list()

# Appel de l'éditeur de map pour créer la map
edM.editMapBis("MapEdit.xlsx")

# Ouverture du fichier map avec pour info la taille de la map et la discrétisation
map_fichier = open("map.txt", "r")

mapEmetCoord = map_fichier.read().strip().split("\n")
emetCoord = mapEmetCoord[0].split("/")
emetCoord.remove("")

mapCoord = mapEmetCoord[1].split(" ")
emetDepart = list()

for elem in emetCoord:
    # Création de ou des émetteurs de base
    elemAttribut = elem.split(" ")
    emetteur = em.Emetteur([float(elemAttribut[0]), float(elemAttribut[1])])
    emetteur.setPhase(float(elemAttribut[2])*m.pi/180)
    emetDepart.append(emetteur)


mapSizeX = float(mapCoord[0])
mapSizeY = float(mapCoord[1])

discretisation = float(mapCoord[2])

tailleCell = mapSizeX/discretisation

nbreCellX = int(discretisation)
nbreCellY = int(mapSizeY/tailleCell)

map_fichier.close()

# Définition du nombre de réflexion
NBRE_MAX_REFL = 3

# Création des listes qui contiennent tous les émetteurs créés
listEmetImage = list()
listEmetImageTot = list()

# Liste contenant toutes les donées
listeData = list()


# Ouverture du fichier walls.txt afin de créer une liste de mur
wall_fichier = open("walls.txt", "r")
wallCoord = wall_fichier.read().strip().split("\n")
wallListe = list()

wall_fichier.close()

if(wallCoord[0]!=''):
    for a in wallCoord:
        elements = a.split(" ")
        wall = w.Wall(elements[:4], float(elements[4]), float(elements[5]), float(elements[6]))
        wallListe.append(wall)

# Création de la liste de cellule
listeCellules = creationCellules()

# Création
if(modeOptimisation):
    # Partie optimisation
    # On créé tous les émetteurs images créés à partir de la liste totale des emetteurs
    listeTotEmetteurs = list()
    nbreDisc = 10
    tailleX = int(mapSizeX/nbreDisc)
    tailleY = int(mapSizeY/nbreDisc)
    for b in range(0, nbreDisc):
        for a in range(0, nbreDisc):
            emetDepart = [em.Emetteur([a*tailleX+0.5, b*tailleY+0.5])]
            listeTotEmetteurs.extend(emetDepart[:])
    for e in listeTotEmetteurs:
        listEmetImage = list()
        listEmetImageTot = list()
        listEmetImageTot.append(e)
        # On rajoute tous les émetteurs images créés à la liste totale
        if(NBRE_MAX_REFL > 0):
            creationListeEmetteurImg(e, wallListe)
            listEmetImageTot.extend(listEmetImage[:])


        for i in range(NBRE_MAX_REFL-1):
            listEmBis = listEmetImage[:]

            listEmetImage = list()

            for emet in listEmBis:
                creationListeEmetteurImg(emet, wallListe)
            listEmetImageTot.extend(listEmetImage[:])
        listOpti.append(listEmetImageTot[:])

else:
    # Mode Classique
    # On créé tous les émetteurs images créés à partir de la liste totale des emetteurs

    listEmetImageTot.extend(emetDepart)

    if (NBRE_MAX_REFL > 0):
        for a in emetDepart:
            creationListeEmetteurImg(a, wallListe)
        listEmetImageTot.extend(listEmetImage)

    for i in range(NBRE_MAX_REFL - 1):
        listEmBis = listEmetImage[:]

        listEmetImage = list()
        for emet in listEmBis:
            creationListeEmetteurImg(emet, wallListe)
        listEmetImageTot.extend(listEmetImage)

