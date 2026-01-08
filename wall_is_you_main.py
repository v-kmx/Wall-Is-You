#Projet wall_is_you SAE 1.0.1
#groupe: Pennetier msika Elie, Kitadi Vianney, Diouri Noam
from random import randint, random

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

def modifier_case(coordonnee, carte):
    """
    tourne une case de 90° : Haut devient Droite, Droite devient Bas, etc.
    """
    i, j = coordonnee
    h, d, b, g = carte[i][j][0]
    carte[i][j][0] = [g, h, d, b]
def deplacer_dragons(carte):
    """
    Déplace les dragons en respectant strictement le dessin des murs :
    sorties[0]=Haut, [1]=Droite, [2]=Bas, [3]=Gauche
    """
    longueur = len(carte)
    hauteur = len(carte[0])
    mouvements = []
    
    for i in range(longueur):
        for j in range(hauteur):
            niveau = carte[i][j][1]
            if niveau is None or niveau < 1:
                continue
            
            sorties_ici = carte[i][j][0]
            directions_valides = []

            # TENTATIVE HAUT : ligne i-1
            # Sortie HAUT (0) ici ET Entrée BAS (2) chez le voisin
            if i > 0 and sorties_ici[0] and carte[i-1][j][0][2] and carte[i-1][j][1] is None:
                directions_valides.append((i-1, j))
            
            # TENTATIVE DROITE : colonne j+1
            # Sortie DROITE (1) ici ET Entrée GAUCHE (3) chez le voisin
            if j < hauteur - 1 and sorties_ici[1] and carte[i][j+1][0][3] and carte[i][j+1][1] is None:
                directions_valides.append((i, j+1))
                
            # TENTATIVE BAS : ligne i+1
            # Sortie BAS (2) ici ET Entrée HAUT (0) chez le voisin
            if i < longueur - 1 and sorties_ici[2] and carte[i+1][j][0][0] and carte[i+1][j][1] is None:
                directions_valides.append((i+1, j))

            # TENTATIVE GAUCHE : colonne j-1
            # Sortie GAUCHE (3) ici ET Entrée DROITE (1) chez le voisin
            if j > 0 and sorties_ici[3] and carte[i][j-1][0][1] and carte[i][j-1][1] is None:
                directions_valides.append((i, j-1))

            if directions_valides:
                nx, ny = directions_valides[randint(0, len(directions_valides) - 1)]
                mouvements.append(((i, j), (nx, ny), niveau))

    for (old_i, old_j), (new_i, new_j), niveau in mouvements:
        if carte[new_i][new_j][1] is None:
            carte[old_i][old_j][1] = None
            carte[new_i][new_j][1] = niveau
def tour_jeu(carte,intention,aventurier):
    """
    fait avancer l'enventurier d'une case selon son intention
    et combattre si ce dernier termine son deplacement sur une case contenant
    un dragon
    renvoi un booléen définissant ou non la fin du jeu
    // update rendu2
    désormais, tour jeu gère maintenant le déplacement de l'aventurier et des dragons
    (fonctionne avec deplacer_dragons)
    """
    if len(intention)>1:
        aventurier[0]=intention.pop(1)
    position_x_aventurier,position_y_aventurier=aventurier[0]
    intention[0]=(position_x_aventurier,position_y_aventurier)
    
    objet_case = carte[position_x_aventurier][position_y_aventurier][1]
    if objet_case is not None:
        # Cas d'un Dragon (Combat)
        if objet_case >= 1:
            if objet_case <= aventurier[1]:
                if objet_case > 50:
                    aventurier[1] += objet_case
                else:
                    carte[position_x_aventurier][position_y_aventurier][1] = None
                    aventurier[1] += 1
                return False
            else:
                return True
        # Cas d'un Trésor (Récupération)
        elif objet_case < 0:
            aventurier[1] += abs(objet_case)
            carte[position_x_aventurier][position_y_aventurier][1] = None

    # Fin du tour de l'aventurier
    if len(intention) == 1:
        deplacer_dragons(carte)
        objet_final = carte[position_x_aventurier][position_y_aventurier][1]
        if objet_final is not None and objet_final >= 1:
            if objet_final <= aventurier[1]:
                 carte[position_x_aventurier][position_y_aventurier][1] = None
                 aventurier[1] += 1
            else:
                 return True

    return False

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

def test_objets(carte):
    """
    cette fonction test toutes les cases et renvoies les informations de celle
    qui contiennent un dragon et celles qui contiennent des trésors
    pour référence renvoi : (position i,position j, information sur la case contenant l'objet)
    """
    compte_dragon=[0]
    compte_tresor=[0]
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            if carte[i][j][1] and carte[i][j][1]>=1:
                compte_dragon[0]+=1
                compte_dragon.append((i,j,carte[i][j][1]))
            elif carte[i][j][1] and carte[i][j][1]<0:
                compte_tresor[0]+=1
                compte_tresor.append((i,j,carte[i][j][1]))
    return compte_dragon,compte_tresor

def encode_case(carte):
    """
    encode les informations des cases de la carte et les renvois
    """
    traduction_box2={(True,False,False,False):u'\u2561',(False,True,False,False):u'\u2568',(False,False,True,False):u'\u2565',(False,False,False,True):u'\u255E',(True,False,False,True):u'\u2550',(False,True,True,False):u'\u2551',(False,False,True,True):u'\u2554',(True,False,True,False):u'\u2557',(False,True,False,True):u'\u255A',(True,True,False,False):u'\u255D',(False,True,True,True):u'\u2560',(True,True,True,False):u'\u2563',(True,False,True,True):u'\u2566',(True,True,False,True):u'\u2569',(True,True,True,True):u'\u256C'}
    carte_encode=list()
    for i in range(len(carte)):
        carte_encode.append(list())
        for j in range(len(carte[0])):
            carte_encode[i].append(traduction_box2[tuple(carte[i][j][0])])
    return carte_encode

def sauvegarde(carte,intention,aventurier):
    """
    sauvegarde l'état de la carte actuelle dans un fichier text
    """
    fichier_sauvegarde=open("save/sauvegarde_dernier_donjon","w")
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
    fichier_sauvegarde.write("\n")

def decode_cases(case_encode):
    """
    decodes les informations des cases de la carte et les renvois
    """
    traduction_box2={u'\u2561':(True,False,False,False),u'\u2568':(False,True,False,False),u'\u2565':(False,False,True,False),u'\u255E':(False,False,False,True),u'\u2550':(True,False,False,True),u'\u2551':(False,True,True,False),u'\u2554':(False,False,True,True),u'\u2557':(True,False,True,False),u'\u255A':(False,True,False,True),u'\u255D':(True,True,False,False),u'\u2560':(False,True,True,True),u'\u2563':(True,True,True,False),u'\u2566':(True,False,True,True),u'\u2569':(True,True,False,True),u'\u256C':(True,True,True,True)}
    return traduction_box2[case_encode]

def recuperer_int(chaine):
    """
    renvoie le premier chiffre qu'il trouve et l'indice ou il s'est arreter
    """
    chiffre=""
    indice_caractere=0
    for i in range(len(chaine)):
        if chaine[indice_caractere].isdigit():
            while indice_caractere<len(chaine) and chaine[indice_caractere].isdigit():
                chiffre+=chaine[indice_caractere]
                indice_caractere+=1
            if indice_caractere==len(chaine)-1:
                return int(chiffre),indice_caractere
            return int(chiffre),indice_caractere+1
        else:
            indice_caractere+=1
    return None,None

def recuperer_chiffre(chaine):
    """
    recupere les valeurs contenue dans une chaine
    """
    indice_traite=0
    resultat=list()
    indice=0
    while indice_traite<len(chaine)-1:
        resultat.append(None)
        indice_temp=0
        resultat[indice],indice_temp=recuperer_int(chaine[indice_traite:])
        indice+=1
        indice_traite+=indice_temp
    return resultat

def chargement(niveau):
    """
    cette fonction permet de lire les informations contenue sur un fichier
    """
    if niveau<0:
        fichier_chargement=open("save/sauvegarde_dernier_donjon","r")
    else:
        fichier_chargement=open("niveau_donjon"+str(niveau),"r")
    fichier_chargement=fichier_chargement.readlines() 
    carte=list()
    for colonne in range(len(fichier_chargement[0])-1):
        carte.append([])
    
    indice_ligne=0
    aventurier=[(0,0),1]
    intention=list()
    
    while fichier_chargement[indice_ligne]!="\n":
        for case in fichier_chargement[indice_ligne]:
            if not(case=="\n"):
                carte[indice_ligne].append([decode_cases(case),None])
        indice_ligne+=1
    
    indice_ligne+=1
    informations_aventurier=recuperer_chiffre(fichier_chargement[indice_ligne])
    aventurier[0]=(informations_aventurier[0],informations_aventurier[1])
    aventurier[1]=informations_aventurier[2]
    indice_ligne+=2
    
    while fichier_chargement[indice_ligne][0]=="I":
        intention.append(tuple(recuperer_chiffre(fichier_chargement[indice_ligne])))
        indice_ligne+=1
    indice_ligne+=1

    while indice_ligne < len(fichier_chargement) and fichier_chargement[indice_ligne][0] in ["D","T"]:
        information_objet=recuperer_chiffre(fichier_chargement[indice_ligne])
        carte[information_objet[0]][information_objet[1]][1]=information_objet[2]
        indice_ligne+=1
    return carte,intention,aventurier

def a_gagner(carte):
    """
    fonction vérifiant si le nombre de dragon est = à 0
    """
    liste_information_dragon,tresors=test_objets(carte)
    return liste_information_dragon[0]==0
        
def ee(carte,aventurier):
    """
    Easter Egg
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

def taille_optimale(taille_x_max,taille_y_max,taille_x_tableau,taile_y_tableau):
    """
    renvoie la taille maximale pour afficher les cases entièrement dans l'écran
    """
    taille=1
    while taille*taille_x_tableau<taille_x_max and taille*taile_y_tableau<taille_y_max:
        taille+=1
    return taille
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
