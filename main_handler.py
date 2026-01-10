from fltk import *
import menu
import menu_selection
import chargement_dernier_niveau
import wiy_editor_graphic 

def main_handler():
    # Crée la fenêtre une seule fois
    cree_fenetre(520, 520)

    while True:
        choix = menu.init_menu_principal()   # récupère le choix du menu
        print(choix)
    
        if choix == "nouvelle_partie":
            choix = ""
            print(choix)
            efface_tout()                    # on nettoie le menu
            menu_selection.main()       # on lance le jeu

        elif choix == "charger_donjon":
            chargement_dernier_niveau.main()
            
        elif choix == "editeur":
            print("lancement du mode éditeur") #on lance le mode editeur
            wiy_editor_graphic.main_editeur()

        elif choix == "quitter":
            ferme_fenetre()
            break
        efface_tout()                    # retour du jeu → effacer avant de revenir au menu

if __name__ == "__main__":
    main_handler()
