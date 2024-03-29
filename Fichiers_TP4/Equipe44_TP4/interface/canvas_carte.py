"""
Ce module contient la classe CanvasCarte, qui permet de dessiner l'ensemble de la carte
et de gérer les clics.
"""

from tkinter import Canvas, ALL

# Cette constante donne la hauteur totale de la carte, en pixels.
DIMENSION_BASE = 300


class CanvasCarte(Canvas):
    def __init__(self, parent, carte):
        """
        Constructeur de la classe CanvasCarte. Attribue les dimensions en pixels
        en fonction des dimensions de la carte, dessine la carte dans l'interface
        et associe le clic de souris à la méthode selectionner_case.

        Args:
            parent (Tk): Le widget TKinter dans lequel le canvas s'intègre.
            carte (Carte): La carte de la guerre des dés à afficher.
        """
        self.carte = carte
        ratio = self.carte.hauteur / self.carte.largeur
        self.hauteur_canvas = DIMENSION_BASE
        self.largeur_canvas = int(DIMENSION_BASE // ratio)
        super().__init__(parent, width=self.largeur_canvas + 1, height=self.hauteur_canvas + 1,
                         borderwidth=0, highlightthickness=0)

        self.suite_clic = None
        self.hauteur_case = self.hauteur_canvas // self.carte.hauteur
        self.largeur_case = self.largeur_canvas // self.carte.largeur
        self.bind("<Button-1>", self.selectionner_case)
        self.bind("<Motion>", self.changer_taille_police)
        self.font_sizes = {}
        self.dessiner_canvas()

    def changer_taille_police(self, event):
        """
        Cette méthode trouve sur quelle case la souris se trouve avec sa position pixel par pixel et est activée à
        chaque fois que la souris se déplace. Ensuite elle appelle la méthode récursive self.fct_recursive afin de
        changer la taille de la police de chaque case de la carte dans le dictionnaire self.font_sizes.

        Args:
            event: La positon event.x et event.y de la souris en pixel par pixel sur le canvas.

        Returns:
            None: Seulement si la case ne fait pas partie de la liste des cases existantes. Exemple: la case est un
            trou dans la carte. La position existe une fois convertit avec la méthode self.pixel_vers_coordonnees, mais
            la case n'est pas dans la liste car c'est un trou. Ça empêche d'afficher un message d'erreur dans la fenêtre
            console dans Pycharm.

        """
        x, y = event.y, event.x
        coor = self.pixel_vers_coordonnees(x, y)
        self.font_sizes = {}

        try:
            case_sous_la_souris = self.carte.cases[coor]
        except:
            return None

        case_sous_la_souris = self.carte.cases[coor]
        self.fct_recursive(case_sous_la_souris, 30)
        self.dessiner_canvas()

    def fct_recursive(self, case, font_size):
        """
        Cette méthode récursive va regarder un case et lui attribuer un taille de police ainsi qu'à ses voisins
        récursivement.

        Args:
            case: La case qui va être ajouté au dictionnaire self.font_sizes et que la police va etre changée
            font_size: La taille de la police que la case va avoir dans le dictionnaire self.font_sizes

        """
        if font_size < 15:
            self.font_sizes[case.coordonnees] = 15
        else:
            self.font_sizes[case.coordonnees] = font_size
        for voisin in case.voisins:
            if voisin.coordonnees not in self.font_sizes or self.font_sizes[voisin.coordonnees] < font_size:
                self.fct_recursive(voisin, font_size - 5)
            if self.font_sizes[voisin.coordonnees] == font_size:
                self.fct_recursive(voisin, font_size - 5)

    def pixel_vers_coordonnees(self, x, y):
        """
        Cette méthode convertit la position d'un clic en coordonnées de la carte.

        Args:
            x: La position du clic, en x (de haut en bas)
            y: La position du clic, en y (de gauche à droite)

        Returns:
            tuple: Les coordonnées de la case cliquée.
        """
        return x // self.hauteur_case, y // self.largeur_case

    def coordonnees_vers_pixels(self, x, y):
        """
        Cette méthode des coordonnées de la carte en position en pixels

        Args:
            x: La coordonnée en x
            y: La coordonnée en y

        Returns:
            tuple: La position en pixels.
        """
        return x * self.hauteur_case, y * self.largeur_case

    def selectionner_case(self, event):
        """
        Cette méthode prend en argument un clic de souris sur le canvas, et actionne
        la fonction définie comme devant faire suite au clic (self.suite_clic), dont
        l'argument est en coordonnées plutôt qu'en pixels.

        Args:
            event (tkinter.Event): L'événement correspondant au clic

        """
        x, y = event.y, event.x  # nos coordonnées sont transposées par rapport aux pixels
        if self.suite_clic is not None:
            self.suite_clic(self.pixel_vers_coordonnees(x, y))

    def dessiner_canvas(self):
        """
        Cette méthode dessine la carte.
        """
        self.delete(ALL)
        for (x, y), case in self.carte.cases.items():
            if len(self.font_sizes) > 0:
                font_size = self.font_sizes[(x, y)]
            else:
                font_size = 15
            if case.mode == 'attaque':
                outline, width = 'gray', 4
            elif case.mode == 'defense':
                outline, width = 'lightgray', 4
            elif case.mode == 'disponible':
                outline, width = 'black', 3
            else:
                outline, width = 'black', 1

            haut, gauche = self.coordonnees_vers_pixels(x, y)
            bas, droite = self.coordonnees_vers_pixels(x + 1, y + 1)
            self.create_rectangle(gauche, haut, droite, bas, fill=case.appartenance.couleur,
                                  outline=outline, width=width)
            self.create_text((gauche + droite) // 2, (haut + bas) // 2, fill='black',
                             font="Times {} bold".format(font_size), text=len(case.des))

    def permettre_clics(self, suite_clic):
        """
        Cette méthode associe une fonction à exécuter à ce qui doit arriver suite
        à un clic.
        """
        self.suite_clic = suite_clic
