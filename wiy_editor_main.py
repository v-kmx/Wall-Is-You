# Projet wall_is_you SAE 1.0.1
from random import randint, random

def taille_optimale(taille_x_max, taille_y_max, nb_colonnes, nb_lignes):
    """
    Renvoie la taille maximale d'une case pour que la grille loge 
    dans la zone de travail spécifiée.
    """
    taille = 1
    # On vérifie si on peut encore agrandir sans dépasser X ou Y
    while (taille + 1) * nb_colonnes < taille_x_max and (taille + 1) * nb_lignes < taille_y_max:
        taille += 1
    return taille

def init_case_vide(coordonnee, carte):
    i, j = coordonnee
    # Toutes les sorties à True = aucun mur selon ta logique de dessin
    sorties = [True, True, True, True] 
    carte[i].append([sorties, None])

def init_carte_vide(nb_colonnes, nb_lignes):
    carte = []
    for i in range(nb_lignes):
        carte.append([])
        for j in range(nb_colonnes):
            init_case_vide((i, j), carte)
    return carte

def modifier_case(coordonnee, carte):
    i, j = coordonnee
    h, d, b, g = carte[i][j][0]
    carte[i][j][0] = [g, h, d, b]

def appliquer_type_mur(coordonnee, carte, type_choisi):
    i, j = coordonnee
    presets = [
        [True, True, True, True],
        [True, False, False, False], 
        [True, True, False, False], 
        [True, True, True, False],
        [False, False, False, False]
    ]
    carte[i][j][0] = list(presets[type_choisi])

def test_objets(carte):
    compte_dragon = [0]
    compte_tresor = [0]
    for r in range(len(carte)):
        for c in range(len(carte[r])):
            val = carte[r][c][1]
            if val is not None:
                if val >= 1:
                    compte_dragon[0] += 1
                    compte_dragon.append((r, c, val))
                elif val < 0:
                    compte_tresor[0] += 1
                    compte_tresor.append((r, c, val))
    return compte_dragon, compte_tresor

def encode_case(carte):
    """
    encode les informations des cases de la carte et les renvois
    (l'encodage correspond au symbole boite)
    (ne prend pas en compte les dragons le hero ou les objets)
    """
    traduction_box2={(True,False,False,False):u'\u2561',(False,True,False,False):u'\u2568',(False,False,True,False):u'\u2565',(False,False,False,True):u'\u255E',(True,False,False,True):u'\u2550',(False,True,True,False):u'\u2551',(False,False,True,True):u'\u2554',(True,False,True,False):u'\u2557',(False,True,False,True):u'\u255A',(True,True,False,False):u'\u255D',(False,True,True,True):u'\u2560',(True,True,True,False):u'\u2563',(True,False,True,True):u'\u2566',(True,True,False,True):u'\u2569',(True,True,True,True):u'\u256C'}
    carte_encode=list()
    for i in range(len(carte)):
        carte_encode.append(list())
        for j in range(len(carte[0])):
            carte_encode[i].append(traduction_box2[tuple(carte[i][j][0])])
    return carte_encode

def sauvegarde(carte, intention=None, aventurier=None, nb_tresor=0):
    if intention is None:
        intention = []
    if aventurier is None:
        aventurier = [(0,0),1]

    fichier_sauvegarde=open("custom/custom_niveau","w", encoding="utf-8")
    carte_encode=encode_case(carte)

    for ligne in carte_encode:
        for case in ligne:
            fichier_sauvegarde.write(case)
        fichier_sauvegarde.write("\n")

    fichier_sauvegarde.write("\n")
    fichier_sauvegarde.write("A "+str(aventurier[0][0])+" "+str(aventurier[0][1])+" "+str(aventurier[1])+'\n')
    fichier_sauvegarde.write("\n")

    for position in intention:
        fichier_sauvegarde.write("I "+str(position[0])+" "+str(position[1])+"\n")

    fichier_sauvegarde.write("\n")
    dragons,tresors=test_objets(carte)

    for dragon in dragons:
        if type(dragon)==int:
            continue
        fichier_sauvegarde.write("D "+str(dragon[0])+" "+str(dragon[1])+" "+str(dragon[2])+"\n")

    fichier_sauvegarde.write("\n")

    for tresor in tresors:
        if type(tresor)==int:
            continue
        fichier_sauvegarde.write("T "+str(tresor[0])+" "+str(tresor[1])+" "+str(tresor[2])+'\n')

    fichier_sauvegarde.write(str(nb_tresor))
    fichier_sauvegarde.close()
