"""
python 3.11.7
pygame 2.5.2
"""

import time
from classes import *


pygame.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1920, 1080))
#fenetre = pygame.display.set_mode((1920, 1080), FULLSCREEN) sometimes bugs
# Titre
pygame.display.set_caption("Billy Bob Game")

# Police des textes
font = pygame.font.Font(FONT_DIR+"BradBunR.ttf", 28)
# couleur des textes
marron = (88, 41, 0)
# Textes
texte_mission = font.render(
    "Bonjour mon petit. J'aurais besoin que tu ailles chercher mon coffre, il se trouve à l'EST, je te récompenserai.",
    1, marron)  # lien avec texte_mission_pp
texte_objet = font.render(" Appuis sur 'Entrée' pour récuperer l'objet", 1, marron)  # lien avec texte_recup_objet
texte_reessaye_mission = font.render("Tu ne m'as pas ramené le coffre, incapable! Retournes y, nom d'une pipe!", 1,
                                     marron)  # lien avec mission_ratee
texte_mission_reussi = font.render(
    "Bravo mon petit! Tu fais la fierté de ton papi, maintenant, prends ce billet et rentre chez toi.", 1,
    marron)  # lien avec mission_reussi

coffre_inventaire = pygame.image.load(IMG_DIR+"coffre_inventaire.png").convert_alpha()
coffre = pygame.image.load(IMG_DIR+"coffre.png").convert_alpha()
papy = pygame.image.load(IMG_DIR+"pepe.png").convert_alpha()
pancarte = pygame.image.load(IMG_DIR+"passage_secret.png").convert_alpha()

#Sons
son_coffre = pygame.mixer.Sound(SOUNDS_DIR+"son_coffre.wav")
son_passage = pygame.mixer.Sound(SOUNDS_DIR+"son_passage.wav")
son_saut = pygame.mixer.Sound(SOUNDS_DIR+"son_saut.wav")
son_fin = pygame.mixer.Sound(SOUNDS_DIR+"son_reward.wav")

pygame.key.set_repeat(20, 10)

# BOUCLE PRINCIPALE
continuer = 1
while continuer:
    # Chargement et affichage de l'écran d'accueil
    accueil = pygame.image.load(IMG_DIR+"accueil.png").convert()
    fenetre.blit(accueil, (0, 0))

    # Rafraichissement
    pygame.display.flip()

    # inventaire du personnage, qui ne possède rien au lancement du jeu.
    inventaire = []
    texte_mission_pp = False
    texte_recup_objet = False
    mission_reussi = False
    mission_lancee = False
    mission_ratee = False

    # On remet ces variables à 1 à chaque tour de boucle
    continuer_jeu = 1
    continuer_accueil = 1
    continuer_menu = 1
    continuer_fin = 1

    # Compteur pour faire disparaitre le premier texte, celui du lancement de la mission.
    affichage_texte_mission = 1200

    # BOUCLE D'ACCUEIL
    while continuer_accueil:

        # Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            # Si l'utilisateur quitte, on met les variables
            # de boucle à 0 pour n'en parcourir aucune et fermer
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Fin du jeu")
                quit()

            elif event.type == KEYDOWN:
                # Lancement du menu
                if event.key == K_RETURN:
                    continuer_accueil = 0  # On quitte l'accueil

    # Chargement et affichage de l'écran de menu
    menu = pygame.image.load(IMG_DIR+"menu.png").convert()
    fenetre.blit(menu, (0, 0))
    pygame.display.flip()

    # BOUCLE DE MENU
    while continuer_menu:
        choix = 0
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            # Si l'utilisateur quitte, on met les variables
            # de boucle à 0 pour n'en parcourir aucune et fermer
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Fin du jeu")
                quit()

            # Variable de choix du niveau
            choix = 0

            if event.type == KEYDOWN and event.key == K_RETURN:
                    choix = LEVELS_DIR+"n1"
                    continuer_menu = 0  # On quitte le menu

    # on vérifie que le joueur a bien fait un choix de niveau
    # pour ne pas charger s'il quitte
    if choix != 0:
        # Chargement du fond
        if choix == LEVELS_DIR+"n1":
            fond = pygame.image.load(IMG_DIR+"background.jpg").convert()
        Quel_niveau = 1

        # Génération d'un niveau à partir d'un fichier
        niveau = Niveau(choix)
        niveau.generer()
        # affiche(niveau.structure)
        niveau.afficher(fenetre)

        # Création du perso
        perso = Perso(IMG_DIR+"cowboy.png", IMG_DIR+"cowboyg.png", niveau)

    pygame.mixer.music.load(SOUNDS_DIR+"son_musique_fond.wav")
    pygame.mixer.music.play(loops = -1)
    pygame.mixer.music.set_volume(0.2)

    # BOUCLE DE JEU
    while continuer_jeu:

        for event in pygame.event.get():

            # Si l'utilisateur quitte, on met la variable qui continue le jeu
            # ET la variable générale à 0 pour fermer la fenêtre
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Fin du jeu")
                quit()

            elif event.type == KEYDOWN:
                # Touches de déplacement du perso
                if event.key == K_RIGHT:
                    perso.deplacer('droite')
                elif event.key == K_LEFT:
                    perso.deplacer('gauche')
                elif event.key == K_SPACE:
                    son_saut.play()
                    etape_saut = 0
                    while etape_saut < 15:  # Montee du saut
                        i = 0
                        for event in pygame.event.get():
                            if event.type == KEYDOWN and event.key == K_RIGHT:
                                i = 1
                                perso.direction = perso.droite
                            elif event.type == KEYDOWN and event.key == K_LEFT:
                                i = -1
                                perso.direction = perso.gauche

                        perso.case_x += i
                        perso.case_y -= 1
                        perso.x = perso.case_x * taille_sprite
                        perso.y = perso.case_y * taille_sprite
                        perso.y = perso.y - 180
                        etape_saut += 1
                        pygame.time.delay(20)
                        # reaffichage de tous les elements du decor
                        fenetre.blit(fond, (0, 0))
                        niveau.afficher(fenetre)
                        fenetre.blit(perso.direction, (perso.x, perso.y))
                        if Quel_niveau != 2:
                            fenetre.blit(papy, (150, 740))
                        if Quel_niveau != 1:
                            fenetre.blit(pancarte, (80, 670))
                            if "c" not in inventaire:
                                fenetre.blit(coffre, (1665, 500))
                        if 'c' in inventaire and not mission_reussi:
                            fenetre.blit(coffre_inventaire, (25, 25))
                        pygame.display.flip()

                    while etape_saut >= 1:  # Descente du saut
                        i = 0
                        for event in pygame.event.get():
                            if event.type == KEYDOWN and event.key == K_RIGHT:
                                i = 1
                                perso.direction = perso.droite
                            elif event.type == KEYDOWN and event.key == K_LEFT:
                                i = -1
                                perso.direction = perso.gauche

                        if perso.case_y > 0 and niveau.structure[perso.case_y + 1][perso.case_x + 2] == 'm':
                            break
                        perso.case_x += i
                        perso.case_y += 1
                        perso.x = perso.case_x * taille_sprite
                        perso.y = perso.case_y * taille_sprite
                        perso.y = perso.y - 180
                        pygame.time.delay(10)
                        etape_saut -= 1
                        # reaffichage de tous les elements du decor
                        fenetre.blit(fond, (0, 0))
                        niveau.afficher(fenetre)
                        fenetre.blit(perso.direction, (perso.x, perso.y))
                        if Quel_niveau != 2:
                            fenetre.blit(papy, (150, 740))
                        if Quel_niveau != 1:
                            fenetre.blit(pancarte, (80, 670))
                            if "c" not in inventaire:
                                fenetre.blit(coffre, (1665, 500))
                        if 'c' in inventaire and not mission_reussi:
                            fenetre.blit(coffre_inventaire, (25, 25))
                        pygame.display.flip()

            # chute des plateformes
            # saut de l'ange
            while perso.case_y < 59 and (not (niveau.structure[perso.case_y + 1][
                                                      perso.case_x + 2] == 'm' or not (
                        perso.direction == perso.droite))) and Quel_niveau == 2 and 68 < perso.case_x < 120:
                i = 0
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_RIGHT:
                        i = 1
                        perso.direction = perso.droite
                    elif event.type == KEYDOWN and event.key == K_LEFT:
                        i = -1
                        perso.direction = perso.gauche
                perso.case_x += i
                perso.case_y += 1
                perso.x = perso.case_x * taille_sprite
                perso.y = perso.case_y * taille_sprite
                perso.y = perso.y - 180
                pygame.time.delay(10)
                # reaffichage de tous les elements du decor
                fenetre.blit(fond, (0, 0))
                niveau.afficher(fenetre)
                fenetre.blit(perso.direction, (perso.x, perso.y))
                fenetre.blit(pancarte, (80, 670))
                if "c" not in inventaire:
                    fenetre.blit(coffre, (1665, 500))
                if "c" in inventaire and not mission_reussi:
                    fenetre.blit(coffre_inventaire, (25, 25))
                if texte_recup_objet:
                    fenetre.blit(texte_objet, (1500, 650))
                pygame.display.flip()

            while perso.case_y < 59 and (niveau.structure[perso.case_y + 1][
                                                 perso.case_x + 2] != "m" and perso.direction == perso.droite):
                perso.case_y += 1
                perso.x = perso.case_x * taille_sprite
                perso.y = perso.case_y * taille_sprite
                perso.y = perso.y - 180
                pygame.time.delay(10)
                # reaffichage de tous les elements du decor
                fenetre.blit(fond, (0, 0))
                niveau.afficher(fenetre)
                fenetre.blit(perso.direction, (perso.x, perso.y))
                if Quel_niveau != 2:
                    fenetre.blit(papy, (150, 740))
                if Quel_niveau != 1:
                    fenetre.blit(pancarte, (80, 670))
                    if "c" not in inventaire:
                        fenetre.blit(coffre, (1665, 500))
                if "c" in inventaire and not mission_reussi:
                    fenetre.blit(coffre_inventaire, (25, 25))
                pygame.display.flip()

            while perso.case_y < 59 and (niveau.structure[perso.case_y + 1][
                                                 perso.case_x + 7] != "m" and perso.direction == perso.gauche):
                perso.case_y += 1
                perso.x = perso.case_x * taille_sprite
                perso.y = perso.case_y * taille_sprite
                perso.y = perso.y - 180
                pygame.time.delay(10)
                # reaffichage de tous les elements du decor
                fenetre.blit(fond, (0, 0))
                niveau.afficher(fenetre)
                fenetre.blit(perso.direction, (perso.x, perso.y))
                if Quel_niveau != 2:
                    fenetre.blit(papy, (150, 740))
                if Quel_niveau != 1:
                    fenetre.blit(pancarte, (80, 670))
                    if "c" not in inventaire:
                        fenetre.blit(coffre, (1665, 500))
                if "c" in inventaire and not mission_reussi:
                    fenetre.blit(coffre_inventaire, (25, 25))
                pygame.display.flip()

            while perso.case_y < 59 and (niveau.structure[perso.case_y + 1][
                                                 perso.case_x + 2] != "m" and perso.direction == perso.droite) and Quel_niveau == 2 and perso.case_x < 68:
                i = 0
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_RIGHT:
                        i = 1
                        perso.direction = perso.droite
                    elif event.type == KEYDOWN and event.key == K_LEFT:
                        i = -1
                        perso.direction = perso.gauche
                perso.case_x += i
                perso.case_y += 1
                perso.x = perso.case_x * taille_sprite
                perso.y = perso.case_y * taille_sprite
                perso.y = perso.y - 180
                pygame.time.delay(10)
                # reaffichage de tous les elements du decor
                fenetre.blit(fond, (0, 0))
                niveau.afficher(fenetre)
                fenetre.blit(perso.direction, (perso.x, perso.y))
                if Quel_niveau != 2:
                    fenetre.blit(papy, (150, 740))
                if Quel_niveau != 1:
                    fenetre.blit(pancarte, (80, 670))
                    if "c" not in inventaire:
                        fenetre.blit(coffre, (1665, 500))
                if "c" in inventaire and not mission_reussi:
                    fenetre.blit(coffre_inventaire, (25, 25))
                if texte_recup_objet:
                    fenetre.blit(texte_objet, (1500, 650))
                pygame.display.flip()

        if perso.x > 1870 and Quel_niveau != 2:  # Changement de map
            perso.x = 30
            perso.case_x = 2
            niveau = []
            niveau = Niveau(LEVELS_DIR+"n2")
            niveau.generer()
            niveau.afficher(fenetre)
            Quel_niveau = 2
        if perso.x < 10 and Quel_niveau != 1:
            son_passage.play()
            perso.x = 1800
            perso.case_x = 120
            niveau = []
            niveau = Niveau(LEVELS_DIR+"n1")
            niveau.generer()
            niveau.afficher(fenetre)
            Quel_niveau = 1

        # affichage des textes et inventaire
        texte_mission_pp = False
        texte_recup_objet = False
        mission_reussi = False
        mission_lancee = False
        mission_ratee = False

        if (
                        20 < perso.x < 250) and Quel_niveau == 1 and "c" not in inventaire and not mission_lancee and affichage_texte_mission != 0:
            texte_mission_pp = True
            mission_lancee = True

        if affichage_texte_mission > 0:
            affichage_texte_mission -= 1

        if (
                        20 < perso.x < 250) and Quel_niveau == 1 and "c" not in inventaire and not mission_lancee and affichage_texte_mission == 0:
            mission_ratee = True

        if (1425 < perso.x < 1800 and perso.case_y <= 43) and Quel_niveau == 2:
            texte_recup_objet = True
            if event.type == KEYDOWN and event.key == K_RETURN and texte_recup_objet:
                son_coffre.play()
                inventaire.append("c")  # ajout du coffre

        if (150 < perso.x < 300) and "c" in inventaire and Quel_niveau == 1:
            mission_reussi = True

        # Affichages de tous les elements à chaque tour de boucle
        fenetre.blit(fond, (0, 0))
        niveau.generer()
        niveau.afficher(fenetre)

        if Quel_niveau != 2:
            fenetre.blit(papy, (150, 740))
        if Quel_niveau != 1:
            fenetre.blit(pancarte, (80, 670))
            if "c" not in inventaire:
                fenetre.blit(coffre, (1665, 500))
        if "c" in inventaire and not mission_reussi:
            fenetre.blit(coffre_inventaire, (25, 25))

        if texte_recup_objet:
            fenetre.blit(texte_objet, (1450, 700))
        if texte_mission_pp:
            fenetre.blit(texte_mission, (100, 100))
        if mission_ratee:
            fenetre.blit(texte_reessaye_mission, (100, 100))
        if mission_reussi:
            fenetre.blit(texte_mission_reussi, (100, 100))

        fenetre.blit(perso.direction, (perso.x, perso.y))  # perso.direction = l'image dans la bonne direction
        pygame.display.flip()

        if mission_reussi:
            pygame.mixer.music.stop()
            son_fin.play()
            time.sleep(3)
            continuer_jeu = 0

    ecran_fin = pygame.image.load(IMG_DIR+"ecran_fin.png").convert()
    fenetre.blit(ecran_fin, (0, 0))
    pygame.display.flip()

    while continuer_fin:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Fin du jeu")
                quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and 120 < event.pos[0] < 730:
                if 670 < event.pos[1] < 1038:
                    continuer_fin = 0
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and 1218 < event.pos[0] < 1774:
                if 658 < event.pos[1] < 1030:
                    print("Fin du jeu")
                    quit()
