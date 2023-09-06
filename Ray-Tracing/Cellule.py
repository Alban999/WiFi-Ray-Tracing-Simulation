"""

 DEFINITION DE L'OBJET CELLULE

"""

from Object import Object as obj

class Cellule(obj):

    def __init__(self, position):
        """
        :param position: initialise la position
        """
        obj.__init__(self, position)
        self.puissance = 0
        self.champE = 0

    def setTailleCell(self, tailleCell):
        """
        :param tailleCell: la taille de la cellule
        :return: pas de return
        """
        self.tailleCell = tailleCell

    def setPuissance(self, puissance):
        """
        :param puissance: puissance qui s'additionne à la puissance totale de la cellule
        :return: pas de return
        """
        self.puissance += puissance

    def setChampE(self, champE):
        """
        :param champE: champ E qui s'additionne au champ E totale de la cellule
        :return: pas de return
        """
        self.champE += champE

    def resetPuissance(self, puissance):
        """
        :param puissance: remet la puissance de la cellule à la valeur puissance
        :return: pas de return
        """
        self.puissance = puissance

