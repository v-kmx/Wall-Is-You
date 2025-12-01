#Projet wall_is_you SAE 1.0.1
#groupe: Pennetier msika Elie, Kitadi Vianney, Diouri Noam
from random import randint
from random import random

def init_case(coordonnee,carte):
    """
    initialise une case qui peut contenir 1,2,3 ou 4 sortie
    cette case peut contenir un dragon ou non
    (initiallement la valeur du dragon est définie sur None)
    pour reference:
    case=[gauche,haut,bas,droite]
    """
    i,j=coordonnee
    sorties=[bool(randint(0,1)),bool(randint(0,1)),bool(randint(0,1)),bool(randint(0,1))]
    while not(True in sorties):
        sorties=[bool(randint(0,1)),bool(randint(0,1)),bool(randint(0,1)),bool(randint(0,1))]
    carte[i].append([sorties,None])

def init_dragon(carte):
    """
    creer aleatoirement des dragons sur chaque case
    (avec une probabilité de 4%)
    si un dragon n'est pas présent sur une case, la case à pour 2ème valeur None
    ainsi une case donne:
    [[liste_sorties],None ou Niveau_dragon]
    
    """
    longueur_carte,hauteur_carte=len(carte),len(carte[0])
    niveau_dragons=1
    probabilite_apparition=0.04
    for i in range(longueur_carte):
        for j in range(hauteur_carte):
            if random()<=probabilite_apparition and carte[i][j][1]==None:
                carte[i][j][1]=niveau_dragons
                niveau_dragons+=1

def init_aventurier(coordonnee=(0,0)):
    #posiblement obsolete, je vous laisse me le dire
    """
    initialise les donnée de l'aventurier
    (si aucune case n'est définis, l'aventurier apparaitra sur la case(0,0))
    et renvoie une liste contenant les coordonnee et le niveau de base de
    l'aventurier
    """
    return [coordonnee,1]  

def verifier_validite_intention(carte, liste_intention):
    """
    Vérifie la validité de la dernière case entrée dans la liste intention.
    Renvoie un booléen.
    """
    i = len(liste_intention) - 1
    Coord_suggeree = liste_intention[i]
    Coord_precedente = liste_intention[i - 1]

    a, b = Coord_suggeree
    c, d = Coord_precedente
    # Check si cases sont identiques
    if (a, b) == (c, d):
        return False

    # Check abscisse: doivent être adjacents horizontalement
    if abs(a - c) > 1:
        return False

    # Check ordonnée: doivent être adjacents verticalement
    if abs(b - d) > 1:
        return False

    # Comparaison sorties
    # Adjacent verticalement
    if a == c:
        # vers le haut
        if b > d and carte[a][b][0][3] and carte[c][d][0][1]:
            return True
        # vers le bas
        if b < d and carte[a][b][0][1] and carte[c][d][0][3]:
            return True

    # Adjacent horizontalement
    if b == d:
        # vers la gauche
        if a > c and carte[a][b][0][0] and carte[c][d][0][2]:
            return True
        # vers la droite
        if a < c and carte[a][b][0][2] and carte[c][d][0][0]:
            return True

    return False

def ajouter_intention(coordonnee_clic,carte,liste_intention):
    """
    verifie si c'est possible et ajoute une intention à l'aventurier
    (dans la beta, celle ci sera définis manuellement)
    """
    if coordonnee_clic in liste_intention:
        supprimer_intention(coordonnee_clic,liste_intention)
        return
    liste_intention.append(coordonnee_clic)
    if not verifier_validite_intention(carte,liste_intention):
        liste_intention.pop()
    return
        
def supprimer_intention(coordonnee_clic,liste_intention):
    """
    supprime la dernière intention si le joueur clique sur une case
    marquée par l'intention
    """
    if not(len(liste_intention)==1) and coordonnee_clic in liste_intention:
        liste_intention.pop()

def verif_intention_global(aventurier,carte,liste_intention):
    """
    vérifie chaque case où est définis l'intention en partant du héro
    si elle trouve une intention invalide elle renvoie une nouvelle liste intention
    composé uniquement des cases valides
    cette fonction est utiles si les cases change alors qu'une intention
    est déjà définie
    """
    
    nouvelle_liste_intention=[aventurier[0]]
    if len(liste_intention)==1:
        return liste_intention
    for i in range(1,len(liste_intention)):
        if not(verifier_validite_intention(carte,liste_intention[:i+1])) or len(liste_intention)==1:
            return nouvelle_liste_intention
        nouvelle_liste_intention.append(liste_intention[i])
    return nouvelle_liste_intention

def modifier_case(coordonnee,carte):
    """
    tourne une case de 90° (modifie le tuple de booléén pour que cela corresponde)
    """
    i,j=coordonnee
    gauche,haut,bas,droite=carte[i][j][0]
    carte[i][j][0]=[droite,gauche,haut,bas]
    
def tour_jeu(carte,intention,aventurier):
    """
    fait avancer l'enventurier d'une case selon son intention
    et combattre si ce dernier termine son deplacement sur une case contenant
    un dragon
    renvoi un booléen définissant ou non la fin du jeu
    """
    if len(intention)>1:
        aventurier[0]=intention.pop(1)
    position_x_aventurier,position_y_aventurier=aventurier[0]
    intention[0]=(position_x_aventurier,position_y_aventurier)
    if carte[position_x_aventurier][position_y_aventurier][1]!=None:
        if carte[position_x_aventurier][position_y_aventurier][1]<=aventurier[1]:
            if carte[position_x_aventurier][position_y_aventurier][1]>50:
                aventurier[1]+=carte[position_x_aventurier][position_y_aventurier][1]
            else:
                carte[position_x_aventurier][position_y_aventurier][1]=None
                aventurier[1]+=1
            return False
        else:
            return True

def init_carte(longueur_carte,hauteur_carte):
    """
    renvoi une carte remplit de cases contenant, ou non, des dragons
    avec des sorties aleatoirement placé
    reference:
    carte[i][j] (coordonne x,y de la case) = [[liste des sorties], (ce que contient la case)
    """
    carte=[]
    for i in range(longueur_carte):
        carte.append([])
        for j in range(hauteur_carte):
            init_case((i,j),carte)
    return carte

def test_dragon(carte):
    """
    cette fonction test toutes les cases et renvoies les informations de celle
    qui contiennent un dragon
    pour référence renvoi : (position i,position j, information sur la case contenant le dragon)
    """
    compte_dragon=[0]
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            if carte[i][j][1]:
                compte_dragon[0]+=1
                compte_dragon.append((i,j,carte[i][j][1]))
    return compte_dragon
                
def sauvegarde(carte,intention,aventurier):
    """
    sauvegarde l'état de la carte actuelle dans un fichier text
    appelé "sauvegarde_derniere_partie.txt
    l'état comprend:
    la position et niveau du héro
    les informations des cases (position,dragon,sorties)
    la taille de la carte
    l'intention
    """
    saut_categorie="\n"
    fichier_sauvegarde=open("sauvegarde_dernier_donjon","w")
    for i_information in range(len(aventurier)):
        if i_information==0:
            fichier_sauvegarde.write(str(aventurier[i_information][0])+","+str(aventurier[i_information][1])+"\n")
        else:
            fichier_sauvegarde.write(str(aventurier[i_information])+"\n")
    fichier_sauvegarde.write(saut_categorie)
    for coordonne in intention:
        fichier_sauvegarde.write(str(coordonne[0])+","+str(coordonne[1])+"\n")
    fichier_sauvegarde.write(saut_categorie)
    fichier_sauvegarde.write(str(len(carte))+","+str(len(carte[0]))+"\n")
    for i in range(len(carte)):
        for j in range(len(carte[0])):
            fichier_sauvegarde.write(str(i)+","+str(j)+" ")
            for sortie in carte[i][j][0]:
                if sortie:
                    fichier_sauvegarde.write("T")
                else:
                    fichier_sauvegarde.write("F")
            if carte[i][j][1]==None:
                fichier_sauvegarde.write(",N\n")
            else:
                fichier_sauvegarde.write(","+str(carte[i][j][1])+"\n")
    fichier_sauvegarde.write("\n")

def recuperer_int(chaine):
    """
    renvoie le premier chiffre qu'il trouve et l'indice ou il s'est arreter
    (un chiffre est considerer comme une suite de numero et il renvoi
    la premiere suite de numéro qu'il croise)
    """
    chiffre=""
    indice_caractere=0
    while indice_caractere<len(chaine) and chaine[indice_caractere].isdigit():
        chiffre+=chaine[indice_caractere]
        indice_caractere+=1
    if indice_caractere==len(chaine)-1:
        return int(chiffre),indice_caractere
    return int(chiffre),indice_caractere+1

def recuperer_tuple(chaine):
    """
    recupere les valeurs d'un tuple
    (a condition que le tuple soit rempli de deux valeur numérique)
    "x,y"
    """
    indice_traite=0
    resultat=[None,None]
    for i in range(2):
        resultat[i],indice_traite=recuperer_int(chaine[indice_traite:])
    return tuple(resultat)

def chargement():
    """
    cette fonction permet de lire les informations contenue sur un fichier
    et de les renvoyer sous une forme valide pour etre utilisé ailleurs
    (pour l'instant uniquement du dernier donjon, à l'avenir aussi des
    niveaux prédéfinis)
    """
    fichier_chargement=open("sauvegarde_dernier_donjon","r")
    fichier_chargement=fichier_chargement.readlines()
    
    #Lecture des données du joueur (toujours les 2 premières lignes)
    joueur=[(0,0),1]
    indice_ligne=0
    joueur[0]=recuperer_tuple(fichier_chargement[0])
    joueur[1]=int(fichier_chargement[1])
    indice_ligne+=3
    
    #Lecture des données de l'intention (uniquement des tuples)
    intention=[]
    while fichier_chargement[indice_ligne]!="\n":
        intention.append(recuperer_tuple(fichier_chargement[indice_ligne]))
        indice_ligne+=1
    indice_ligne+=1
    
    #Lectures des informations des case
    #étape un création d'une carte de base
    taille_carte=recuperer_tuple(fichier_chargement[indice_ligne])
    carte=init_carte(taille_carte[0],taille_carte[1])
    indice_ligne+=1
    
    #étape 2 modification de celle ci par les données sauvegardés
    while fichier_chargement[indice_ligne]!="\n":
        ligne=fichier_chargement[indice_ligne]
        indice_traite_sur_ligne=0
        indice_fin_tuple=0
        while ligne[indice_fin_tuple]!=" ":
            indice_fin_tuple+=1
        i_case,j_case=recuperer_tuple(ligne[:indice_fin_tuple])
        indice_traite_sur_ligne+=len(str(i_case))+len(str(j_case))+2
        sortie=[]
        for i in range(4):
            sortie.append(ligne[indice_traite_sur_ligne+i]=="T")
        indice_traite_sur_ligne+=5
        dragon=None
        if "N" not in ligne:
            niveau_dragon,indice_a_oublier=recuperer_int(ligne[indice_traite_sur_ligne:])
            dragon=int(niveau_dragon)
        carte[i_case][j_case]=[sortie,dragon]
        indice_ligne+=1
    return carte,intention,joueur           

def a_gagner(carte):
    """
    fonction vérifiant si le nombre de dragon est = à 0
    renvoi un booléen
    """
    liste_information_dragon=test_dragon(carte)
    return liste_information_dragon[0]==0
        
def ee(carte,aventurier):
    """
    fonction la PLUS importante
    elle gère toutes les positions
    et vos finances
    et vous fait de la choucroute
    non...elle gère les Easter Egg
    """
    evenement=randint(0,2)
    x,y=aventurier[0]
    if evenement==0:
        for i in range(len(carte)):
            for j in range(len(carte[0])):
                carte[i][j][1]=1
        carte[x][y][1]=None
        if x!=len(carte)//2 or y!=len(carte[0])//2:
            carte[len(carte)//2][len(carte[0])//2][1]=len(carte)*len(carte[0])-2
        else:
            carte[0][0][1]=len(carte)*len(carte[0])-2
        aventurier[1]=2
    elif evenement==1:
        aventurier[1]=99
        for i in range(len(carte)):
            for j in range(len(carte[0])):
                carte[i][j][0]=[True,True,True,True]
    else:
        possibilite=[[True,False,False,False],[False,True,False,False],[False,False,True,False],[False,False,False,True]]
        for i in range(len(carte)):
            for j in range(len(carte[0])):
                position_porte=randint(0,3)
                carte[i][j][0]=possibilite[position_porte]
    return carte,aventurier
                
"""
def main():
    
    #lance la creation de carte et l'ensemble des systèmes
    #utilisé dans le jeux, utilisé pour les tests
    
    game_over=False
    hauteur_tableau=9
    longueur_tableau=9
    carte=init_carte(longueur_tableau,hauteur_tableau)
    aventurier=[(0,0),1]
    init_dragon(carte)
    #l'intention est une liste de coordonnée que l'aventurier va prochainement parcourir
    intentions=[aventurier[0]] #l'intention possède TOUJOURS les coordonnée de l'aventurier en sa première valeur (d'indice 0)
    ajouter_intention((1,0),carte,intentions)
    sauvegarde(carte,intentions,aventurier)

main()
"""