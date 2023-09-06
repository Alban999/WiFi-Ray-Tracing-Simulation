"""

 DEFINITION DE L'OBJET EMETTEUR

"""

from Object import Object as obj

class Emetteur(obj):

    def __init__(self, position):
        """
        :param position: initialisation de la position
        """
        obj.__init__(self, position)
        self.listeDeMur = list()
        self.phase = 0

    def rajouteMurListe(self, mur):
        """
        :param mur: un mur par lequel l'émetteur a été réfléchi
        :return: pas de return. Met à jour la liste des murs par lequel l'émetteur a été réfléchi
        """
        self.listeDeMur.append(mur)

    def getListeMurs(self):
        """
        :return: renvoie la liste des murs par lequel l'émetteur a été réfléchi
        """
        return self.listeDeMur

    def setPhase(self, phase):
        """
        :param phase: la phase de l'émetteur
        :return: pas de return
        """
        self.phase = phase


