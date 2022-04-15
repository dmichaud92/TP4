"""
Ce module contient la classe JoueurOrdinateurAmeliore.
À la base, ce joueur hérite de JoueurOrdinateur, et n'est donc qu'un ordinateur ayant
la même stratégie d'intelligence artificielle.

Vous devez redéfinir les méthodes strategie_selection_attaquant et strategie_selection_defenseur
pour rendre cette intelligence plus fûtée que l'intelligence originale.

Attention, une fois les méthodes décommentées, elles effaceront les méthodes du même nom
de JoueurOrdinateur.

Des idées de changement à apporter sont disponibles dans l'énoncé.
"""
from random import randint

from guerre_des_des_tp3.joueur_ordinateur import JoueurOrdinateur


class JoueurOrdinateurAmeliore(JoueurOrdinateur):
    def __init__(self, couleur, carte):
        """
        Constructeur de la classe JoueurOrdinateurAmeliore

        Args:
            couleur (str): La couleur du joueur. Cela lui sert de nom.
            carte (Carte): La totalité de la carte, pour vous aider à prendre
                des décisions plus globales
        """
        super().__init__(couleur)
        self.carte = carte

    # def strategie_selection_attaquant(self, cases_disponibles):
        # VOTRE CODE ICI

    # def strategie_selection_defenseur(self, cases_disponibles, case_attaquante):
        # VOTRE CODE ICI
