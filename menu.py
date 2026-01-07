from fltk import *
from wall_is_you_graphic import *

hauteur_fenetre = 520
largeur_fenetre = 520
ecart_btn = hauteur_fenetre // 8
# Afin de désactiver le menu après avoir choisi une option//lancé une partie et le réactiver quand on revient au menu principal
# Cette variable ne sera qu'utile après avoir tout mis en place
afficher_menu = True
# Choix du joueur au sein du menu
choix_menu = 0
selection = []
def init_menu_principal():
    """
    cette fonction se charge d'afficher les différent éléments du menu
    """
    efface_tout()
    # Couleur de fond
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, couleur="black", remplissage="black")
    attente(1)
    # Splash art du jeu
    image(largeur_fenetre//2, hauteur_fenetre//8, "ressources/img/splashart.png", largeur_fenetre//2, hauteur_fenetre//6, ancrage="center", tag="titre")
    attente(1)
    # Implémentation des boutons
    # Nouvelle Partie
    rectangle(largeur_fenetre//4, hauteur_fenetre//3, 3*largeur_fenetre//4, hauteur_fenetre//3 + 50, couleur="white", remplissage="white", tag="btn_nouvelle_partie")
    texte(largeur_fenetre//2, hauteur_fenetre//3 + 25, "Nouvelle Partie", couleur="black", ancrage="center", taille=20, police="Helvetica", tag="txt_nouvelle_partie")
    # Charger Donjon
    rectangle(largeur_fenetre//4, hauteur_fenetre//3 + ecart_btn, 3*largeur_fenetre//4, hauteur_fenetre//3 + ecart_btn + 50, couleur="white", remplissage="white", tag="btn_charger_donjon")
    texte(largeur_fenetre//2, hauteur_fenetre//3 + ecart_btn + 25, "Charger Donjon", couleur="black", ancrage="center", taille=20, police="Helvetica", tag="txt_charger_donjon")
    # Creer Donjon
    rectangle(largeur_fenetre//4, hauteur_fenetre//3 + 2*ecart_btn , 3*largeur_fenetre//4, hauteur_fenetre//3 + 2*ecart_btn + 50, couleur="white", remplissage="white", tag="btn_creer_donjon")
    texte(largeur_fenetre//2,hauteur_fenetre//3 + 2*ecart_btn + 25, "Créer Donjon", couleur="black", ancrage="center", taille=20, police="Helvetica", tag="txt_creer_donjon")
    # Quitter
    rectangle(largeur_fenetre//4, hauteur_fenetre//3 + 3*ecart_btn, 3*largeur_fenetre//4, hauteur_fenetre//3 + 3*ecart_btn + 50, couleur="white", remplissage="white", tag="btn_quitter")
    texte(largeur_fenetre//2, hauteur_fenetre//3 + 3*ecart_btn + 25, "Quitter", couleur="black", ancrage="center", taille=20, police="Helvetica", tag="txt_quitter")
    # Credits
    texte(largeur_fenetre//2, hauteur_fenetre*0.9, "Créé par DIOURI-ADEQUIN Noam,\nPENNETIER-MSIKA Elie et\nKITADI MUNDUNGA Vianney", couleur="white", ancrage="center", taille=10, police="Helvetica", tag="credits")
    # attend_ev()
    # Selection des options du menu
    while True:
        mise_a_jour()
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            return "quitter"
        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            # Nouvelle Partie
            if largeur_fenetre//4 <= x <= 3*largeur_fenetre//4 and hauteur_fenetre//3 <= y <= hauteur_fenetre//3 + 50:
                global afficher_menu
                afficher_menu = False
                print("Lancement d'une nouvelle partie...")
                efface_tout()
                rectangle(0, 0, largeur_fenetre, hauteur_fenetre, couleur="black", remplissage="black")
                return "nouvelle_partie"
                # Insertion -> nouvelle partie
            # Charger Donjon
            elif largeur_fenetre//4 <= x <= 3*largeur_fenetre//4 and hauteur_fenetre//3 + ecart_btn <= y <= hauteur_fenetre//3 + ecart_btn + 50:
                afficher_menu = False
                print("Chargement de la partie...")
                efface_tout()
                return "charger_donjon"
                # Insertion -> système de chargement
            # Creer Donjon
            elif largeur_fenetre//4 <= x <= 3*largeur_fenetre//4 and hauteur_fenetre//3 + 2*ecart_btn <= y <= hauteur_fenetre//3 + 2*ecart_btn + 50:
                print("creation d'un nouveau donjon...")
                return "creer"
            # Quitter
            elif largeur_fenetre//4 <= x <= 3*largeur_fenetre//4 and hauteur_fenetre//3 + 3*ecart_btn <= y <= hauteur_fenetre//3 + 3*ecart_btn + 50:
                return "quitter"
        
def main_menu():
    cree_fenetre(largeur_fenetre, largeur_fenetre)
    init_menu_principal()

"""
if __name__ == "__main__":
    # Création de la fenêtre du menu principal
    cree_fenetre(largeur_fenetre, largeur_fenetre)
    init_menu_principal()

    # DEBUGGAGE // Pour tester le menu en standalone
"""
# main_menu()
