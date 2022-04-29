"""
Ce module contient la classe CarteTeleversee. Celle-ci permet d'utiliser une carte de jeu
provenant d'un fichier texte. Ce fichier doit contenir des . là où il y aura une case, et des
espaces là où il y aura des trous. Évidemment, la carte doit être connectée (toutes les cases
sont accessibles).

Exemple valide:
.. ..
 ...
  .

Exemple invalide:
..
.  .
  ..

"""

from guerre_des_des_tp3.carte import Carte
from guerre_des_des_tp3.case import Case
from tkinter import messagebox


class CarteTeleversee(Carte):
    def __init__(self, nom_fichier):
        """
        Constructeur de la classe CarteTeleversee.

        Args:
            nom_fichier (str): Le nom du fichier contenant la carte sous forme de points.
        """
        cases = self.lire_fichier_carte(nom_fichier)
        hauteur = 0
        largeur = 0
        for coor in cases.keys():
            hauteur = max(hauteur, coor[0] + 1)
            largeur = max(largeur, coor[1] + 1)
        super().__init__(hauteur, largeur, cases)

    def lire_fichier_carte(self, nom_fichier):
        """
        Cette méthode lit le fichier et convertit son contenu en cases.

        Args:
            nom_fichier (str): Le nom du fichier à lire

        Returns:
            dict: Le dictionnaire de cases, dont les clés sont les coordonnées.
        """

        try:
            fichier = open(nom_fichier, "r")
        except :
            messagebox.showerror("Erreur", "Le fichier dont on a entré le nom n’existe pas.")
            return None


        fichier = open(nom_fichier, "r")
        texte = fichier.read()
        colonne = -1
        rangee = 0
        dico = {}

        try:
            for car in texte:
                print(car)
                if car != ".":
                    if car != " ":
                        if car != "\n":
                            raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le fichier contient des caratères invalides.")
            return None

        for car in texte:
            colonne = colonne + 1
            if car == '.':
                coor = (rangee, colonne)
                dico[coor] = Case(coor)
                self.definir_voisins(dico)
            if car == '\n':
                rangee = rangee + 1
                colonne = -1

        if not self.verifier_cases_connectees(dico):
            messagebox.showerror("Erreur", "Les cases du fichier ne sont pas toutes connectées.")
            return None

        return dico

# if __name__ == "__main__":
#     carte = CarteTeleversee('carte_invalide.txt')
#     carte.lire_fichier_carte()

