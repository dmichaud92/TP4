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

    def filtrer_nb_des(self, cases, valeurs_acceptees):
        """
        Cette méthode retourne les cases dont le nombre de dés (Case.nombre_de_des)
        fait partie des valeurs de nombres de dés acceptés.

        Args:
            cases (dict): Les cases du jeu
            valeurs_acceptees (list): La liste des nombres de dés à conserver

        Returns:
            dict: Les cases du jeu dont le nombre de dés fait partie des valeurs acceptées

        """
        cases_filtrees = {}
        for coor, case in cases.items():
            if case.nombre_de_des() in valeurs_acceptees:
                cases_filtrees[coor] = case
        return cases_filtrees

    def trouver_nb_des_optimal(self, cases, minimum=False):
        """
        Cette méthode trouve la case ayant le maximum OU le minimum de dés.
        Si l'option minimum n'est pas cochée, on trouve la case ayant le plus grand nombre de dés.
        Si l'option minimum est cochée, on trouve la case ayant le plus petit nombre de dés.
        Vous pouvez utiliser des sous-méthodes si cela vous facilite le travail.

        Dans le cas d'une égalité (e.g. plusieurs cases ont le maximum de dés), vous pouvez
        sélectionner n'importe laquelle de ces cases (au hasard, toujours la dernière visitée par
        votre algorithme, ...).

        Args:
            cases (dict): Les cases parmi lesquelles chercher
            minimum (bool, optionnel): Si True, trouver le minimum, si False, trouver le maximum.
                Défaut: False

        Returns:
            Case: la case sélectionnée
        """
        opti_nb_des = None
        case_max = None
        for case in cases.values():
            if minimum:
                condition = opti_nb_des is None or case.nombre_de_des() < opti_nb_des
            else:
                condition = opti_nb_des is None or case.nombre_de_des() > opti_nb_des
            if condition:
                case_max = case
                opti_nb_des = case.nombre_de_des()

        return case_max

    def strategie_selection_attaquant(self, cases_disponibles):
        """
        Cette méthode implémente l'intelligence artificielle (IA) permettant de sélectionner
        un attaquant.

        Args:
            cases_disponibles (dict): Les cases disponibles pour attaque

        Returns:
            Case: La case sélectionnée par l'IA. None si elle arrête son tour.
        """

        # L'IA sélectionne l'attaquant ayant le plus de dés
        return self.trouver_nb_des_optimal(cases_disponibles)

    def strategie_selection_defenseur(self, cases_disponibles, case_attaquante):
        """
        Cette méthode implémente l'intelligence artificielle (IA) permettant de sélectionner
        un défenseur.

        Args:
            cases_disponibles (dict): Les cases disponibles pour attaque
            case_attaquante (Case): La case qui attaque

        Returns:
            Case: La case sélectionnée par l'IA. None si elle retourne à la phase de
            sélection de l'attaquant.
        """

        # Si des voisins ont 1 ou 2 dés de moins, l'IA attaque le plus fort d'entre eux
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles,
                                [case_attaquante.nombre_de_des() - 1, case_attaquante.nombre_de_des() - 2])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, si un voisin a autant de dés que l'IA, elle l'attaque
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles, [case_attaquante.nombre_de_des()])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, si un voisin a au moins 3 dés de moins que l'IA, elle attaque le plus fort d'entre eux
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles,
                                [case_attaquante.nombre_de_des() - i for i in
                                 range(3, case_attaquante.nombre_de_des())])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, l'IA attaque le voisin le plus faible parmi ceux qui sont plus forts qu'elle
        if randint(1, 2) == 1:
            return self.trouver_nb_des_optimal(cases_disponibles, minimum=True)
        else:
            return None
