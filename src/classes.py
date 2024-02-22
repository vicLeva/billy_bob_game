import pygame
from pygame.locals import *

MAIN_DIR = "../"
INCLUDE_DIR = MAIN_DIR + "include/"
IMG_DIR = INCLUDE_DIR + "img/"
FONT_DIR = INCLUDE_DIR + "font/"
LEVELS_DIR = INCLUDE_DIR + "levels/"
SOUNDS_DIR = INCLUDE_DIR + "sounds/"

nombre_sprite_longueur = 128
nombre_sprite_largeur = 72
taille_sprite = 15

class Niveau:
        """Classe permettant de créer un niveau"""
        def __init__(self, fichier):
                self.fichier = fichier
                self.structure = 0
        
        
        def generer(self):
                """Méthode permettant de générer le niveau en fonction du fichier.
                On crée une liste générale, contenant une liste par ligne à afficher""" 
                #On ouvre le fichier
                with open(self.fichier, "r") as fichier:
                        structure_niveau = []
                        #On parcourt les lignes du fichier
                        for ligne in fichier:
                                ligne_niveau = []
                                #On parcourt les sprites (lettres) contenus dans le fichier
                                for sprite in ligne:
                                        #On ignore les "\n" de fin de ligne
                                        if sprite != '\n':
                                                #On ajoute le sprite à la liste de la ligne
                                                ligne_niveau.append(sprite)
                                #On ajoute la ligne à la liste du niveau
                                structure_niveau.append(ligne_niveau)
                        #On sauvegarde cette structure
                        self.structure = structure_niveau
        
        
        def afficher(self, fenetre):
                """Méthode permettant d'afficher le niveau en fonction 
                de la liste de structure renvoyée par generer()"""
                #Chargement des images
                mur = pygame.image.load(IMG_DIR+"mur.png").convert()
                
                #On parcourt la liste du niveau
                num_ligne = 0
                for ligne in self.structure:
                        #On parcourt les listes de lignes
                        num_case = 0
                        for sprite in ligne:
                                #On calcule la position réelle en pixels
                                x = num_case * taille_sprite
                                y = num_ligne * taille_sprite
                                if sprite == 'm':                  #m = Mur
                                        fenetre.blit(mur, (x,y))
                                num_case += 1
                        num_ligne += 1
                        
                        
                        
                        
class Perso:
        """Classe permettant de créer un personnage"""
        def __init__(self, droite, gauche, niveau):
                #Sprites du personnage
                self.droite = pygame.image.load(droite).convert_alpha()
                self.gauche = pygame.image.load(gauche).convert_alpha()
                #Position du personnage en cases et en pixels
                self.case_x = 3#cases fichier
                self.case_y = 59
                self.x = 45#position en pixel
                self.y = 705
                #Direction par défaut
                self.direction = self.droite
                #Niveau dans lequel le personnage se trouve 
                self.niveau = niveau

        def deplacer(self, direction):
                """Methode permettant de déplacer le personnage"""
                
                #Déplacement vers la droite
                if direction == 'droite':
                        #Pour ne pas dépasser l'écran
                        if self.case_x < 128:
                                #On vérifie que la case de destination n'est pas un mur
                                if self.niveau.structure[self.case_y][self.case_x+6] != 'm':
                                        #Déplacement d'une case
                                        self.case_x += 1
                                        #Calcul de la position "réelle" en pixel
                                        self.x = self.case_x * taille_sprite
                        #Image dans la bonne direction
                        self.direction = self.droite
                
                #Déplacement vers la gauche
                if direction == 'gauche':
                        if self.case_x > 0:
                                if self.niveau.structure[self.case_y][self.case_x+3] != 'm':
                                        self.case_x -= 1
                                        self.x = self.case_x * taille_sprite
                        self.direction = self.gauche


##def affiche(liste):
##        for i in range(len(liste)):
##                for j in range(len(liste)):
##                        if liste[i][j] == "0":
##                                print("0",end="")
##                        elif liste[i][j] == "a":
##                                print("a", end="")
##                        else:
##                                print("m", end="")
##                print()
##        print()

                                
        
                                
                                
                                
                        

                
        
