"""

 DEFINITION DE L'OBJET WALL (LES MURS DE LA MAP)

"""

import math as m
import cmath as cm

class Wall():

    def __init__(self, position, width, epsR, sigma):
        """
        :param position: initialisation de la position du mur (contient ces deux extrémités : [pos1, pos2])
        :param width: la largeur du mur
        :param epsR: son epsilon relatif
        :param sigma: sa conductivité
        """
        self.posDebut = [float(position[0]), float(position[1])]
        self.posFin = [float(position[2]), float(position[3])]
        self.eps = 8.854*10**(-12)*epsR
        self.width = width
        self.sigma = sigma

    def setResistance(self, epsTilde):
        """
        :param epsTilde: epsilon tilde
        :return: ne renvoie rien. Initialise la résistance.
        """
        self.resistance = complex(cm.sqrt(4 * m.pi * 10 ** (-7) / epsTilde))
