from fltk import *
import os
import wall_is_you_graphic
import wall_is_you_graphic_automatique

hauteur_fenetre=520
largeur_fenetre=520
taille_texte=20

def affiche_bouton_niveau(nom,x1,y1,x2,y2,couleur,taille_texte,couleur_texte):
    rectangle(x1,y1,x2,y2,couleur,couleur)
    texte((x1+x2)/2,(y1+y2)/2,nom,couleur_texte,"center","Helvetica",taille_texte)


def affiche_option(nom,x1,y1,x2,y2,couleur,taille_texte,couleur_texte):
    rectangle(x1,y1,x1+30,y1+30,couleur,"black")
    texte((x1+x2)//2,(y1+y2)//2,nom,couleur_texte,"center","Helvetica",taille_texte)


def recuperer_liste_niveau():
    niveaux_precree=None
    niveau_custom=None
    for _,_,niveaux in os.walk("level"):
        niveaux_precree=niveaux
    for _,_,niveau in os.walk("custom"):
        niveau_custom=niveau
    return niveaux_precree,niveau_custom


def affiche_bases():
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, "black", "black")
    ligne(largeur_fenetre//2, 0, largeur_fenetre//2, hauteur_fenetre,"grey")
    ligne(0, hauteur_fenetre//taille_texte*2, largeur_fenetre, hauteur_fenetre//taille_texte*2, "grey")
    ligne(largeur_fenetre//2,hauteur_fenetre//2,largeur_fenetre,hauteur_fenetre//2,"grey")
    texte(largeur_fenetre//4, hauteur_fenetre//taille_texte, "Niveaux", "white", "center", "Helvetica", taille_texte)
    texte(largeur_fenetre*3//4, hauteur_fenetre//taille_texte, "Autre", "white", "center", "Helvetica", taille_texte)
    texte(largeur_fenetre*3//4, hauteur_fenetre//2+taille_texte*2,"Option", "white", "center", "Helvetica", taille_texte)
    texte(largeur_fenetre*3//4, hauteur_fenetre//2+taille_texte*3.5,"Il se peut que certaine selection\n bloque certaine options", "red", "center", "Helvetica", taille_texte//2)
    affiche_bouton_niveau("Demarrer",10,hauteur_fenetre-60,largeur_fenetre//2-10,hauteur_fenetre-10,"green",taille_texte,"black")


def affiche_bouton(niveaux_precree,niveau_custom):
    hauteur_bouton=hauteur_fenetre//taille_texte*2.5
    ecart=hauteur_bouton
    for niveau in niveaux_precree:
        affiche_bouton_niveau(niveau,10,hauteur_bouton,largeur_fenetre//2-10,hauteur_bouton+50,"white",taille_texte,"black")
        hauteur_bouton+=ecart
    hauteur_bouton=hauteur_fenetre//taille_texte*2.5
    for niveau in niveau_custom:
        affiche_bouton_niveau(niveau,largeur_fenetre//2+10,hauteur_bouton,largeur_fenetre-10,hauteur_bouton+50,"white",taille_texte,"black")
        hauteur_bouton+=ecart
    affiche_bouton_niveau("libre",largeur_fenetre//2+10,hauteur_bouton,largeur_fenetre-10,hauteur_bouton+50,"white",taille_texte,"black")


def affiche_options():
    hauteur_option=hauteur_fenetre//2+taille_texte*4.5
    ecart=hauteur_option
    affiche_option("intention manuelle",largeur_fenetre//2+10,hauteur_option,largeur_fenetre-10,hauteur_option+50,"white",taille_texte-5,"white")
    affiche_option("tour unique",largeur_fenetre//2+10,hauteur_option+50,largeur_fenetre-10,hauteur_option+100,"white",taille_texte-5,"white")
 
 
def init_menu(niveaux_precree,niveau_custom):
    affiche_bases()
    affiche_bouton(niveaux_precree,niveau_custom)
    affiche_options()
    mise_a_jour()
    
    
def affiche_option_selectionner(num_option):
    hauteur_option=hauteur_fenetre//2+taille_texte*4.5
    rectangle(largeur_fenetre//2+10,hauteur_option+50*num_option,largeur_fenetre//2+40,hauteur_option+30+50*num_option,"white","white")
    
    
def recuperer_valeur(evenement,liste_niveau_precree,liste_niveau_custom):
    x_clic=abscisse(evenement)
    y_clic=ordonnee(evenement)
    hauteur_bouton=hauteur_fenetre//taille_texte*2.5
    for i in range(len(liste_niveau_precree)):
        if x_clic>0 and x_clic<largeur_fenetre//2 and y_clic>hauteur_bouton+hauteur_bouton*i and y_clic<hauteur_bouton+50+hauteur_bouton*i:
            return liste_niveau_precree[i]
    for i in range(len(liste_niveau_custom)):
        if x_clic>largeur_fenetre//2 and x_clic<largeur_fenetre and y_clic>hauteur_bouton+hauteur_bouton*i and y_clic<hauteur_bouton+50+hauteur_bouton*i:
            return liste_niveau_custom[i]
    hauteur_option=hauteur_fenetre//2+taille_texte*4.5
    hauteur_bouton=hauteur_fenetre//taille_texte*2.5
    if x_clic>largeur_fenetre//2+10 and x_clic<largeur_fenetre//2+40 and y_clic>hauteur_option and y_clic<hauteur_option+50:
        return "Option0"
    elif x_clic>largeur_fenetre//2+10 and x_clic<largeur_fenetre//2+40 and y_clic>hauteur_option+50 and y_clic<hauteur_option+100:
        return "Option1"
    elif x_clic>largeur_fenetre//2 and x_clic<largeur_fenetre and y_clic>hauteur_bouton and y_clic<hauteur_option+50:
        return "libre0"
    elif x_clic>0 and x_clic<largeur_fenetre//2 and y_clic>hauteur_fenetre-60 and y_clic<hauteur_fenetre-10:
        return "Demarrer"


def recuperer_indice(liste,element):
    for i in range(len(liste)):
        if liste[i]==element:
            return i
    return None


def actualisation_menu_selectionner(selection_niveau,liste_option,liste_niveau_precree,liste_niveau_custom,selection_precedente,option_precedente):
    if selection_niveau!=selection_precedente:
        affiche_bouton(liste_niveau_precree,liste_niveau_custom)
    if liste_option!=option_precedente:
        affiche_options()
    if selection_niveau!=None:
        hauteur_bouton=hauteur_fenetre//taille_texte*2.5
        if selection_niveau[0] in ["n","t"]:
            indice_decalage=recuperer_indice(liste_niveau_precree,selection_niveau)
            affiche_bouton_niveau(selection_niveau,10,hauteur_bouton+hauteur_bouton*indice_decalage,largeur_fenetre//2-10,hauteur_bouton+hauteur_bouton*indice_decalage+50,"red",taille_texte,"black")
        elif selection_niveau[0]=="l":
            affiche_bouton_niveau(selection_niveau,largeur_fenetre//2+10,hauteur_bouton*2,largeur_fenetre-10,hauteur_bouton*2+50,"red",taille_texte,"black")
        elif selection_niveau[0]=="c":
            indice_decalage=recuperer_indice(liste_niveau_custom,selection_niveau)
            affiche_bouton_niveau(selection_niveau,largeur_fenetre//2+10,hauteur_bouton,largeur_fenetre-10,hauteur_bouton+50,"red",taille_texte,"black")
    for i in range(len(liste_option)):
        if liste_option[i]:
            affiche_option_selectionner(i)
    mise_a_jour()


def sauvegarde_caracteristique(selection_niveau,options):
    fichier_sauvegarde=open("save/caracteristique_dernier_donjon.txt","w")
    if options[0]:
        fichier_sauvegarde.write("A\n")
    else:
        fichier_sauvegarde.write("M\n")
    fichier_sauvegarde.write(selection_niveau[-1]+"\n")
    if options[1]:
        fichier_sauvegarde.write("T\n")
    else:
        fichier_sauvegarde.write("F\n")
    print("sauvegarde terminé")

    
def main(debug=False):
    if debug:
        cree_fenetre(largeur_fenetre,hauteur_fenetre)
        
    #initialisation des variables nécessaire
    selection_niveau=None
    option=[False,False]
    est_finis=False
    selection_precedente=None
    option_precedente=[False,False]
    #l'indice 0 correspond a l'intention manuelle, l'indice 1 correspond au mode tour unique    
    niveaux_precree,niveau_custom=recuperer_liste_niveau()
    
    #initialisation du menu
    init_menu(niveaux_precree,niveau_custom)
    
    #boucle d'interaction
    while not(est_finis):
        evenement=attend_ev()
        if type_ev(evenement)=="Quitte":
            print("Je veux quitter")
            return "quitter"
        elif type_ev(evenement)=="ClicGauche":
            valeur_clic=recuperer_valeur(evenement,niveaux_precree,niveau_custom)
            if valeur_clic!=None:
                if valeur_clic[0] in ["t","n","c"]:
                    selection_precedente=selection_niveau
                    selection_niveau=valeur_clic
                elif valeur_clic[0]=="l":
                    selection_precedente=selection_niveau
                    selection_niveau=valeur_clic
                    option_precedente=option[:]
                    option[0]=True
                elif valeur_clic[0]=="O" and (selection_niveau==None or selection_niveau[0]!="l"):
                    option_precedente=option[:]
                    option[int(valeur_clic[-1])]=not(option[int(valeur_clic[-1])])
                elif valeur_clic[0]=="D":
                    est_finis=True
        actualisation_menu_selectionner(selection_niveau,option,niveaux_precree,niveau_custom,selection_precedente,option_precedente)
    efface_tout()
    print("chargement niveau: ",selection_niveau,"\navec les options suivantes : \n	Intention manuelle:",option[0],"\n	mode tour unique :",option[1])
    sauvegarde_caracteristique(selection_niveau,option)
    if option[0]:
        if option[1]:
            wall_is_you_graphic.main(int(selection_niveau[-1]),True)
        else:
            wall_is_you_graphic.main(int(selection_niveau[-1]))
    else:
        if option[1]:
            wall_is_you_graphic_automatique.main(int(selection_niveau[-1]),True)
        else:
            wall_is_you_graphic_automatique.main(int(selection_niveau[-1]))

#main(True)
