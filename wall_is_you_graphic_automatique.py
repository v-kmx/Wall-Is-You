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
        "- Clic droit :\n Placer/Supprimer\nun trésor",
        "\n- Espace :\nTerminer le tour",
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


    print(carte)
    for r in range(lignes):
        for c in range(colonnes):
            x_init = c * taille_case
            y_init = r * taille_case
            print(r,c,lignes,colonnes)
            case = carte[r][c]
            sorties = case[0]
            dragon = case[1]

            # Dessin des Murs
            if not sorties[0]:
                rectangle(x_init, y_init, x_init + epaisseur, y_init + taille_case, remplissage="white", couleur="black")
            if not sorties[1]:
                 rectangle(x_init, y_init, x_init + taille_case, y_init + epaisseur, remplissage="white", couleur="black")
            if not sorties[2]:
                rectangle(x_init, y_init + taille_case - epaisseur, x_init + taille_case, y_init + taille_case, remplissage="white", couleur="black")
            if not sorties[3]:
                rectangle(x_init + taille_case - epaisseur, y_init, x_init + taille_case, y_init + taille_case, remplissage="white", couleur="black")
                

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
def modification_dessin(carte, taille_case, aventurier, intention, nb_w, nb_h, mode_tour_unique, case_visite):
    if not clic_dans_zone_de_jeu(taille_case, nb_w, nb_h): return intention
    coord = (ordonnee_souris() // taille_case, abscisse_souris() // taille_case)
    if mode_tour_unique and coord in case_visite:
        return intention,case_visite
    modifier_case(coord, carte)
    case_visite.add(coord)
    chemin=pathfind(carte, aventurier)
    if chemin:
        intention=chemin
    else:
        intention=[aventurier[0]]
    dessiner_fond_noir_total() 
    dessiner_carte(carte, taille_case, aventurier, intention)
    return intention, case_visite
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

def ajouter_tresor(carte, coordonnee_clic):
    i,j=coordonnee_clic
    if carte[i][j][1] == -1:
        carte[i][j][1] = None
    else:
        dragon,tresor=test_objets(carte)
        if len(tresor)>1:
            for i_tresor_pose in range(1,len(tresor)):
                i_tresor,j_tresor,niveau_tresor=tresor[i_tresor_pose]
                carte[i_tresor][j_tresor][-1]=None
        if carte[i][j][1]==None:
            carte[i][j][-1]=-1
    return carte

def position_tresor(carte):
    dragon, tresors = test_objets(carte)
    if len(tresors) > 1:
        i, j, dragon = tresors[1]
        return (i, j)
    return None


def dragon_plus_fort(M, aventurier):
    """
    Retourne la coordonnée du dragon le plus fort accessible depuis 'depart' (aventurier),
    en utilisant BFS.
    """
    maxniveau = -1
    coord = None
    chemins=[[aventurier[0]]]
    cases={aventurier[0]}

    while chemins:
        new_chemins=[]
        for chemin in chemins:
            x, y=chemin[-1]
            a=dispo(M, (x, y))
            for i, j in a:
                if (i, j) in cases:
                    continue
                if not sorties(x, y, i, j, M):
                    continue 
                if M[i][j][1] is not None and M[i][j][1]>0:
                    if M[i][j][1]>maxniveau:
                        maxniveau=M[i][j][1]
                        coord=(i, j)
                cases.add((i, j))
                new_chemins.append(chemin + [(i, j)])
        chemins=new_chemins
    return coord

def dispo(M, coord):
    dispo=[]
    a, b = coord
    if a-1>=0:
        dispo.append((a-1, b))
    if a+1<len(M):
        dispo.append((a+1, b))
    if b-1>=0:
        dispo.append((a, b-1))
    if b+1<len(M):
        dispo.append((a, b+1))
    return dispo

#fait le test corresp à la sortie
def sorties(x, y, i, j, M):
    if not( i>=0 and j>=0 and i<len(M) and j<len(M[i])):
        return False
    
    elif i==x and j==y-1:
        return M[x][y][0][0] and M[i][j][0][3]
    
    elif i==x and j==y+1:
        return M[x][y][0][3] and M[i][j][0][0]
    
    elif i==x-1 and j==y:
        return M[x][y][0][1] and M[i][j][0][2]
    
    elif i==x+1 and j==y:
        return M[x][y][0][2] and M[i][j][0][1]
    
    return False
    """
    if i==x and j==y-1:
        return M[x][y][0][3]==True and M[x][y][0][3]==M[i][j][0][1]
    elif i==x and j== y+1:
        return M[x][y][0][1]==True and M[x][y][0][1]==M[i][j][0][3]
    elif i==x-1 and j==y:
        return M[x][y][0][0]==True and M[x][y][0][0]==M[i][j][0][2]
    elif i==x+1 and j==y:
        return M[x][y][0][2]==True and M[x][y][0][2]==M[i][j][0][0]
    else:
        return False
    #"""
    
    
def pathfind(M, aventurier):
    coord_tresor=position_tresor(M)
    if coord_tresor:
        chemin=rec_pathfind(M, aventurier, coord_tresor)
        if chemin:
            return chemin

    coord_dragon=dragon_plus_fort(M, aventurier)
    if coord_dragon:
        chemin=rec_pathfind(M, aventurier, coord_dragon)
        return chemin

    return False
    
def rec_pathfind(M, aventurier, coord):
    chemins=[[aventurier[0]]]
    cases={aventurier[0]}
    while chemins:
        new_chemins=[]
        for chemin in chemins:
            x, y=chemin[-1]
            a=dispo(M, chemin[-1])
            for i, j in a:
                if (i, j) in cases:
                    continue
                if not sorties(x, y, i, j, M):
                    continue
                if M[i][j][1] is not None and M[i][j][1]>0 and(i,j)!=coord:
                    continue
                pas=chemin+[(i, j)]
                if (i, j)==coord:
                    return chemin + [(i, j)]
                
                cases.add((i, j))
                new_chemins.append(pas)
        chemins=new_chemins
        
    return False

# Fonction principale
"""Il s'agit de la fonction principale du jeu qui va initialiwser la carte, gérer la boucle
evenementielle et l'affichage."""
def main(chargement_carte=0, mode_tour_unique=False):
    game_over = False

    if not chargement_carte:
        hauteur_tableau = 8
        longueur_tableau = 8
        carte = init_carte(longueur_tableau, hauteur_tableau)
        aventurier = init_aventurier()
        init_dragon(carte)
        intentions = [aventurier[0]]
    else:
        carte, intentions, aventurier, tresor = chargement(chargement_carte)
        hauteur_tableau = len(carte)
        longueur_tableau = len(carte[0])
        
    taille_case= taille_optimale(largeur_fenetre()//2,hauteur_fenetre(),longueur_tableau,hauteur_tableau)
    largeur_jeu = longueur_tableau * taille_case
    hauteur_jeu = hauteur_tableau * taille_case
    largeur_totale = int(largeur_jeu * (1 + marge_droite))
    hauteur_totale = hauteur_jeu 

    efface_tout()
    dessiner_fond_noir_total()

    dessiner_carte(carte, taille_case, aventurier, intentions)
    dessiner_marge_droite(largeur_fenetre()//2, largeur_totale - (largeur_fenetre()//2), hauteur_totale)
    mise_a_jour() 

    copy_carte, copy_aventurier = copy_initial(carte, aventurier)
    case_modifie=set()

    while not game_over:
        efface_tout()
        dessiner_fond_noir_total()
        
        dessiner_carte(carte, taille_case, aventurier, intentions)
        dessiner_marge_droite(largeur_fenetre()//2, largeur_totale - (largeur_fenetre()//2), hauteur_totale)
        
        mise_a_jour()

        evenement = attend_ev()
        type_e = type_ev(evenement)
        if (type_ev(evenement) == "Quitte"):
            game_over = True
        elif type_ev(evenement) == "ClicGauche":
            intentions, case_modifie = modification_dessin(carte, taille_case, aventurier, intentions, longueur_tableau, hauteur_tableau, mode_tour_unique, case_modifie)
        elif type_ev(evenement) =="ClicDroit":
            if clic_dans_zone_de_jeu(taille_case, longueur_tableau, hauteur_tableau):
                    x=ordonnee_souris()//taille_case
                    y=abscisse_souris()//taille_case
                    carte=ajouter_tresor(carte, (x, y))
                    chemin = pathfind(carte, aventurier)
                    if not chemin:
                        intentions=[]
                    else:
                        intentions=verif_intention_global(aventurier, carte, chemin)
        elif type_e == "Touche":
            nom_touche = touche(evenement)
             

            if nom_touche == "space":
                while len(intentions) > 1 and not game_over:
                    game_over = tour_jeu(carte, intentions, aventurier)
                    efface_tout()
                    dessiner_fond_noir_total()
                    dessiner_carte(carte, taille_case, aventurier, intentions)
                    nouveau_chemin = pathfind(carte, aventurier)
                    if nouveau_chemin:
                        intentions=nouveau_chemin
                    else:
                        intentions=[aventurier[0]]
                    dessiner_marge_droite(largeur_jeu, largeur_totale - largeur_jeu, hauteur_totale)
                    mise_a_jour()
                    sleep(0.2)
            # keybind pour reset
            elif nom_touche == "r" or nom_touche == "R":
                carte, aventurier = charger_initial(copy_carte, copy_aventurier, taille_case)
                intentions = [aventurier[0]]
            # keybind pour sauvegarde
            elif nom_touche == "s" or nom_touche == "S":
                sauvegarde(carte, intentions, aventurier,tresor)
            # keybind pour... payer vos impots, générer de la choucroute, gérer vos finances
            # (nan c'est faux c'est juste l'easter egg)
            elif nom_touche == "e" or nom_touche == "E":
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


