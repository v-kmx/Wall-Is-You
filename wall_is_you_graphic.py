# Projet wall_is_you SAE 1.0.1
# groupe: Pennetier msika Elie, Kitadi Vianney, Diouri Noam

# IMPORTS
"""On importe ici les différents modules utiles ainsi que la partie logique du jeu wall_is_you_main"""
from random import randint
from time import sleep
import copy
from fltk import *
from wall_is_you_main import *

"""Définition de la taille de la marge comparée à la fenêtre, c.f. def dessiner_marge_droite"""
# Partie interface graphique WallIsYou
marge_droite = 1/3 

# IU (Inteface utilisateur) principale hors jeu
def dessiner_fond_noir_total():
    """Cette fonction fait en sorte que le fond de la fenêtre reste en noir"""
    rectangle(0, 0, 2000, 2000, couleur="black", remplissage="black")

def dessiner_marge_droite(x0, largeur, hauteur):
    """Problémtique joueur // indication des contrôles pour ce dernier"""
    rectangle(x0, 0, x0 + largeur, hauteur, couleur="black", remplissage="black")
    texte(x0 + 20, 20, "Contrôles :", "white", ancrage="nw", police="helvetica", taille=18)
    lignes = [
        "- Clic gauche :\nPivot de salle",
        "- Clic droit :\nAjout/Supression\nintention",
        "\n- Espace :\nTerminer le tour",
        "\n- T : Placer/Supprimer\nun trésor",
        "\n- R : Reset le donjon",
        "\n- S : Sauvegarder",
        "\n- E : Easter Egg",
        "\n- Echap : Retour Menu",
    ]
    y = 60
    for l in lignes:
        texte(x0 + 20, y, l, "white", "nw", "helvetica", 13)
        y += 50

# Copie initiale du jeu
"""Problématique sur les commandes, l'aventurier, la carte et les dragons 
//Copie de l'état initial du jeu avec la fonction deepcopy() de la librairie copy de Python
Contrairement un à simple copy, deepcopy permet de réaliser une copie indépendente des éléments
précédemment mentionnés au tout début du jeu afin que la touche R (commande de reest) puisse
fonctionner correctement et bel et bien ramener le jeu à son etat original"""
def copy_initial(carte, aventurier):
    copy_carte = copy.deepcopy(carte)
    copy_aventurier = copy.deepcopy(aventurier)
    return copy_carte, copy_aventurier

def charger_initial(backupcarte, backupaventurier, taille_case):
    efface_tout()
    dessiner_fond_noir_total() 
    nouvelle_carte = copy.deepcopy(backupcarte)
    nouvel_aventurier = list(copy.deepcopy(backupaventurier))
    dessiner_carte(nouvelle_carte, taille_case, nouvel_aventurier, [nouvel_aventurier[0]])
    return nouvelle_carte, nouvel_aventurier

# IU (Interface Utilisateur) Dans le jeu
"""Permet d'afficher le niveau d'une entitée (Aventurier ou Dragon) sur une case donnée"""
def dessiner_niveau(case, taille_case, niveau):
    r, c = case
    x_center = c * taille_case + taille_case // 2
    y_center = r * taille_case + taille_case // 2
    x_dec = int(taille_case * 0.375 // 2)
    y_dec = int(taille_case * 0.625 // 2)
    rectangle(x_center + x_dec, y_center - y_dec, x_center + x_dec * 2, y_center, "black", "white")
    texte(x_center + x_dec + 1, y_center - y_dec + 1.5, str(niveau), "black", "nw", "helvetica", 8)
"""Cette fonction va dans un premier temps parcourir la grille afin de dessiner le contenu de
chaque case sur le grillage"""
def dessiner_case(carte, taille_case, aventurier):
    lignes = len(carte)
    colonnes = len(carte[0]) if lignes > 0 else 0
    epaisseur = int(taille_case * 0.1)

    for r in range(lignes):
        for c in range(colonnes):
            x_init = c * taille_case
            y_init = r * taille_case
            case = carte[r][c]
            sorties = case[0]
            dragon = case[1]

            # Dessin des Murs
            if not sorties[0]:
                rectangle(x_init, y_init, x_init + taille_case, y_init + epaisseur, remplissage="white", couleur="black")
            if not sorties[1]:
                rectangle(x_init + taille_case - epaisseur, y_init, x_init + taille_case, y_init + taille_case, remplissage="white", couleur="black")
            if not sorties[2]:
                rectangle(x_init, y_init + taille_case - epaisseur, x_init + taille_case, y_init + taille_case, remplissage="white", couleur="black")
            if not sorties[3]:
                rectangle(x_init, y_init, x_init + epaisseur, y_init + taille_case, remplissage="white", couleur="black")

           # Dessin des Dragon
            if dragon is not None:
                if dragon>0:
                    x_centre = x_init + taille_case // 2
                    y_centre = y_init + taille_case // 2
                    image(x_centre, y_centre, "ressources/img/dragon.png", 32, 30)
                    dessiner_niveau((r, c), taille_case, dragon)
                
                # Dessin du trésor
                if dragon<0:
                    x_centre = x_init + taille_case // 2
                    y_centre = y_init + taille_case // 2
                    image(x_centre, y_centre, "ressources/img/tresor.png", 32, 30)

            # Dessin de l'Aventurier
            if (r, c) == aventurier[0]:
                lvl = aventurier[1]
                x_centre = x_init + taille_case // 2
                y_centre = y_init + taille_case // 2
                image(x_centre, y_centre, "ressources/img/hero.png", 26, 34)
                dessiner_niveau((r, c), taille_case, lvl)
"""affiche l'ensemble de l'intention présent dans la liste_intention"""
def dessiner_intention(carte, taille_case, intention):
    if len(intention) <= 1: return
    r_prev, c_prev = intention[0]
    x_prev = c_prev * taille_case + taille_case // 2
    y_prev = r_prev * taille_case + taille_case // 2
    for idx in range(1, len(intention)):
        r, c = intention[idx]
        x = c * taille_case + taille_case // 2
        y = r * taille_case + taille_case // 2
        ligne(x_prev, y_prev, x, y, "red", 2)
        x_prev, y_prev = x, y
"""Dessine une carte sous forme de grille en fonction d'une taille de case donnée."""
def dessiner_carte(carte, taille_case, aventurier, intention):
    lignes = len(carte)
    colonnes = len(carte[0]) if lignes > 0 else 0

    # Texture de fond des cases
    for r in range(lignes):
        for c in range(colonnes):
            x_init = c * taille_case
            y_init = r * taille_case
            image(x_init + taille_case // 2, y_init + taille_case // 2, "ressources/img/dungeon-tileset.png", int(taille_case), int(taille_case))

    dessiner_case(carte, taille_case, aventurier)
    dessiner_intention(carte, taille_case, intention)
    
    # Bordure
    largeur_totale_jeu = colonnes * taille_case
    hauteur_totale_jeu = lignes * taille_case
    
    # On retire 1 pixel à la largeur et hauteur pour que le trait soit DEDANS
    rectangle(0, 0, largeur_totale_jeu - 1, hauteur_totale_jeu - 1, couleur="white")

# Detection souris & Intention
"""Vérifie si le clic de souris a eu lieu à l'intérieur de la grille de jeu.
Renvoie True si oui, False sinon."""
def clic_dans_zone_de_jeu(taille_case, nb_cases_largeur, nb_cases_hauteur):
    x = abscisse_souris()
    y = ordonnee_souris()
    return (0 <= x < nb_cases_largeur*taille_case) and (0 <= y < nb_cases_hauteur*taille_case)
"""Gère l'action du clic gauche : Rotation des murs d'une salle et met à jour l'affichage
après chaque modification."""
def modification_dessin(carte, taille_case, aventurier, intention, nb_w, nb_h):
    if not clic_dans_zone_de_jeu(taille_case, nb_w, nb_h): return intention
    coord = (ordonnee_souris() // taille_case, abscisse_souris() // taille_case)
    modifier_case(coord, carte)
    if len(intention) > 1:
        intention = verif_intention_global(aventurier, carte, intention)
    efface_tout()
    dessiner_fond_noir_total() 
    dessiner_carte(carte, taille_case, aventurier, intention)
    return intention
"""Gère l'action du clic droit : Ajout/supression d'une étape au déplacement (intention).
    Met à jour l'affichage après modification"""
def modifier_intention(carte, taille_case, aventurier, intention, nb_w, nb_h):
    if not clic_dans_zone_de_jeu(taille_case, nb_w, nb_h): return intention
    coord = (ordonnee_souris() // taille_case, abscisse_souris() // taille_case)
    ajouter_intention(coord, carte, intention)
    efface_tout()
    dessiner_fond_noir_total()
    dessiner_carte(carte, taille_case, aventurier, intention)
    return intention

# Game Over/ Victoire
"""Affiche un écran de GAME OVER quand la partie se termine abruptement ou que le joueur perd"""
def affiche_game_over(largeur_totale, hauteur_totale):
    efface_tout()
    dessiner_fond_noir_total()
    l_win = largeur_fenetre()
    h_win = hauteur_fenetre()
    texte(l_win / 2, h_win / 2, "Game Over", "red", "center", "helvetica", 38)
    mise_a_jour()
"""Affiche un écran de Victoire lorsque le joueur a abattu tous les dragons"""
def afficher_victoire(largeur_totale, hauteur_totale):
    efface_tout()
    dessiner_fond_noir_total()
    l_win = largeur_fenetre()
    h_win = hauteur_fenetre()
    texte(l_win / 2, h_win / 2, "You win!", "green", "center", "helvetica", 38)
    mise_a_jour()

# Ah! Voici l'Easter Egg!!! (Ne le dites à personne)
"""Ceci est une partie bonus avec un Easter Egg étant le Konami Code. Lorsque le joueur
entre ce dernier, l'aventurier recevra un bonus"""
def verif_ee(carte, aventurier, taille_case, intentions):
    dessiner_carte(carte, taille_case, (aventurier[0], 0), intentions)
    dernier_evenement = []
    code = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right"]
    for _ in range(len(code)):
        ev = attend_ev()
        dernier_evenement.append(touche(ev))
    if dernier_evenement == code:
        carte, aventurier = ee(carte, aventurier)
        dessiner_carte(carte, taille_case, (aventurier[0], 150), intentions)
    else:
        dessiner_carte(carte, taille_case, (aventurier[0], -1), intentions)
    sleep(1)
    return carte, aventurier

def ajouter_tresor(carte,coordonnee_clic):
    i,j=coordonnee_clic
    dragon,tresor=test_objets(carte)
    if len(tresor)>1:
        for i_tresor_pose in range(1,len(tresor)):
            i_tresor,j_tresor,niveau_tresor=tresor[i_tresor_pose]
            carte[i_tresor][j_tresor][-1]=None
    if carte[i][j][1]==None:
        carte[i][j][-1]=-1
    return carte
    

# Fonction principale
"""Il s'agit de la fonction principale du jeu qui va initialiwser la carte, gérer la boucle
evenementielle et l'affichage."""
def main(chargement_carte=0):
    game_over = False
    taille_case = 40 

    if not chargement_carte:
        hauteur_tableau = 8
        longueur_tableau = 8
        carte = init_carte(longueur_tableau, hauteur_tableau)
        aventurier = init_aventurier()
        init_dragon(carte)
        intentions = [aventurier[0]]
    else:
        carte, intentions, aventurier = chargement()
        hauteur_tableau = len(carte)
        longueur_tableau = hauteur_tableau

    largeur_jeu = longueur_tableau * taille_case
    hauteur_jeu = hauteur_tableau * taille_case
    largeur_totale = int(largeur_jeu * (1 + marge_droite))
    hauteur_totale = hauteur_jeu 

    efface_tout()
    dessiner_fond_noir_total()

    dessiner_carte(carte, taille_case, aventurier, intentions)
    dessiner_marge_droite(largeur_jeu, largeur_totale - largeur_jeu, hauteur_totale)
    mise_a_jour() 

    copy_carte, copy_aventurier = copy_initial(carte, aventurier)

    while not game_over:
        efface_tout()
        dessiner_fond_noir_total()
        
        dessiner_carte(carte, taille_case, aventurier, intentions)
        dessiner_marge_droite(largeur_jeu, largeur_totale - largeur_jeu, hauteur_totale)
        
        mise_a_jour()

        evenement = attend_ev()
        type_e = type_ev(evenement)
        if (type_ev(evenement) == "Quitte"):
            game_over = True
        elif type_ev(evenement) == "ClicGauche":
            intentions = modification_dessin(carte, taille_case, aventurier, intentions, longueur_tableau, hauteur_tableau)
        elif type_ev(evenement) == "ClicDroit":
            if clic_dans_zone_de_jeu(taille_case, longueur_tableau, hauteur_tableau):
                intentions = modifier_intention(carte, taille_case, aventurier, intentions, longueur_tableau, hauteur_tableau)
        elif type_e == "Touche":
            nom_touche = touche(evenement)
            
            if nom_touche == "t":
                if clic_dans_zone_de_jeu(taille_case, longueur_tableau, hauteur_tableau):
                    x_c = ordonnee_souris() // taille_case
                    y_c = abscisse_souris() // taille_case
                    carte = ajouter_tresor(carte, (x_c, y_c))
            
            elif nom_touche == "space":
                while len(intentions) > 1 and not game_over:
                    game_over = tour_jeu(carte, intentions, aventurier)
                    efface_tout()
                    dessiner_fond_noir_total()
                    dessiner_carte(carte, taille_case, aventurier, intentions)
                    dessiner_marge_droite(largeur_jeu, largeur_totale - largeur_jeu, hauteur_totale)
                    mise_a_jour()
                    sleep(0.2)
            # keybind pour reset
            elif nom_touche == "r":
                carte, aventurier = charger_initial(copy_carte, copy_aventurier, taille_case)
                intentions = [aventurier[0]]
            # keybind pour sauvegarde
            elif nom_touche == "s":
                sauvegarde(carte, intentions, aventurier)
            # keybind pour... payer vos impots, générer de la choucroute, gérer vos finances
            # (nan c'est faux c'est juste l'easter egg)
            elif nom_touche == "e":
                carte, aventurier = verif_ee(carte, aventurier, taille_case, intentions)
            # keybinding pour retourner vers le menu principal
            elif nom_touche == "Escape":
                return "quitter"

        if a_gagner(carte):
            afficher_victoire(largeur_totale, hauteur_totale)
            attente(5)
            return "quitter"

    affiche_game_over(largeur_totale, hauteur_totale)
    attente(3)
    return "quitter"


# main()  # /!\ DEBUGGAGE // Lance le jeu graphique 
