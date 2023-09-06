"""

 DEFINITION D'UN OBJET PRESENT SUR LA MAP

"""

class Object:

    def __init__(self, position):
        """
        :param position: initialisation de la position
        """
        self.position = position

    def setPos(self, pos):
        """
        :param pos: la position de l'objet
        :return: pas de return
        """
        self.position = pos;

    def getPos(self):
        """
        :return: renvoie la position de l'objet
        """
        return self.position;


