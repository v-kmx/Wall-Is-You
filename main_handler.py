from fltk import *
import menu
import wall_is_you_graphic

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
            wall_is_you_graphic.main()       # on lance le jeu
            efface_tout()                    # retour du jeu → effacer avant de revenir au menu

        elif choix == "charger_donjon":
            pass 

        elif choix == "quitter":
            ferme_fenetre()
            break


if __name__ == "__main__":
    main_handler()
