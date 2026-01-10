# Projet wall_is_you SAE 1.0.1
# groupe: Pennetier msika Elie, Kitadi Vianney, Diouri Noam

from fltk import *
from wiy_editor_main import *

TAILLE_CASE = 45

def dessiner_fond_noir_total():
    rectangle(0, 0, 2000, 2000, couleur="black", remplissage="black")

def dessiner_niveau(case, taille_case, niveau):
    r, c = case
    x_center = c * taille_case + taille_case // 2
    y_center = r * taille_case + taille_case // 2
    rectangle(x_center + 10, y_center - 18, x_center + 25, y_center, "black", "white")
    texte(x_center + 12, y_center - 17, str(abs(niveau)), "black", "nw", "helvetica", 9)

def dessiner_case(carte, taille_case, aventurier):
    ep = 4
    for r in range(len(carte)):
        for c in range(len(carte[0])):
            x_init, y_init = c * taille_case, r * taille_case
            sorties, obj = carte[r][c][0], carte[r][c][1]
            if not sorties[0]: rectangle(x_init, y_init, x_init + taille_case, y_init + ep, "white", "black")
            if not sorties[1]: rectangle(x_init + taille_case - ep, y_init, x_init + taille_case, y_init + taille_case, "white", "black")
            if not sorties[2]: rectangle(x_init, y_init + taille_case - ep, x_init + taille_case, y_init + taille_case, "white", "black")
            if not sorties[3]: rectangle(x_init, y_init, x_init + ep, y_init + taille_case, "white", "black")
            if obj is not None:
                if obj > 0:
                    image(x_init + taille_case // 2, y_init + taille_case // 2, "ressources/img/dragon.png", 32, 30)
                    dessiner_niveau((r, c), taille_case, obj)
                elif obj < 0:
                    image(x_init + taille_case // 2, y_init + taille_case // 2, "ressources/img/tresor.png", 32, 30)
            if aventurier[0] == (r, c):
                image(x_init + taille_case // 2, y_init + taille_case // 2, "ressources/img/hero.png", 26, 34)
                dessiner_niveau((r, c), taille_case, aventurier[1])

def dessiner_carte(carte, taille_case, aventurier):
    for r in range(len(carte)):
        for c in range(len(carte[0])):
            try:
                image(c * taille_case + taille_case // 2, r * taille_case + taille_case // 2, "ressources/img/dungeon-tileset.png", taille_case, taille_case)
            except:
                rectangle(c*taille_case, r*taille_case, (c+1)*taille_case, (r+1)*taille_case, "gray")
    dessiner_case(carte, taille_case, aventurier)
    rectangle(0, 0, len(carte[0]) * taille_case, len(carte) * taille_case, "white")

def dessiner_interface_editeur(x0, options, index, entites, ent_idx, niv, auto, w, h, mur_idx):
    y = 30
    texte(x0 + 20, y, "MODE EDITEUR", "red", "nw", "helvetica", 16); y += 60
    for i, opt in enumerate(options):
        c = "yellow" if i == index else "white"
        val = ""
        if opt == "Placer Mur":
            # Indique le nombre de sorties du mur qui SERA posé
            val = f": < {mur_idx if mur_idx < 4 else 4} sorties >" if mur_idx > 0 else ": < Vide >"
        elif opt == "Placer Entité": val = f": < {entites[ent_idx]} >"
        elif opt == "Niveau": val = f": < {niv} >"
        elif opt == "Dragon Auto": val = f": < {'OUI' if auto else 'NON'} >"
        elif opt == "Largeur": val = f": < {w} >"
        elif opt == "Hauteur": val = f": < {h} >"
        texte(x0 + 20, y, f"{opt}{val}", c, "nw", "helvetica", 12); y += 40
    texte(x0 + 20, y + 40, "Navigation: Fleches\nModifier: Gauche/Droite\nL: Action / R: Effacer\nS: Save / ESC: Menu", "white", "nw", "helvetica", 10)

def main_editeur():
    nb_w, nb_h = 8, 8 # nb_w = colonnes, nb_h = lignes
    carte = init_carte_vide(nb_w, nb_h)
    aventurier = [None, 1]
    options = ["Pivoter", "Placer Mur", "Placer Entité", "Niveau", "Dragon Auto", "Largeur", "Hauteur"]
    entites = ["Hero", "Dragon", "Trésor"]
    sel_idx, ent_idx, niv_sel, auto_dr, mur_preset_idx = 0, 0, 1, True, 1

    while True:
        efface_tout()
        dessiner_fond_noir_total()
        dessiner_carte(carte, TAILLE_CASE, aventurier)
        dessiner_interface_editeur(nb_w * TAILLE_CASE, options, sel_idx, entites, ent_idx, niv_sel, auto_dr, nb_w, nb_h, mur_preset_idx)
        mise_a_jour()

        ev = donne_ev()
        tev = type_ev(ev)
        
        if tev == "Quitte": break
        if tev == "Touche":
            t = touche(ev)
            if t == "Escape": return "menu"
            elif t == "Up": sel_idx = (sel_idx - 1) % len(options)
            elif t == "Down": sel_idx = (sel_idx + 1) % len(options)
            elif t in ["Left", "Right"]:
                mod = 1 if t == "Right" else -1
                if options[sel_idx] == "Placer Mur": mur_preset_idx = (mur_preset_idx + mod) % 5
                elif options[sel_idx] == "Placer Entité": ent_idx = (ent_idx + mod) % len(entites)
                elif options[sel_idx] == "Niveau": niv_sel = max(1, niv_sel + mod)
                elif options[sel_idx] == "Dragon Auto": auto_dr = not auto_dr
                elif options[sel_idx] == "Largeur":
                    nb_w = max(2, min(12, nb_w + mod))
                    carte = init_carte_vide(nb_w, nb_h)
                elif options[sel_idx] == "Hauteur":
                    nb_h = max(2, min(12, nb_h + mod))
                    carte = init_carte_vide(nb_w, nb_h)
            elif t == "s": 
                print('sauvegarde en cours...')
                sauvegarde(carte, [], aventurier, 0)
                print('sauvegarde terminée.')


        if tev == "ClicGauche":
            # x = colonne, y = ligne
            cx, cy = abscisse(ev) // TAILLE_CASE, ordonnee(ev) // TAILLE_CASE
            if 0 <= cx < nb_w and 0 <= cy < nb_h:
                mode = options[sel_idx]
                if mode == "Pivoter": modifier_case((cy, cx), carte)
                elif mode == "Placer Mur": appliquer_type_mur((cy, cx), carte, mur_preset_idx)
                elif mode == "Placer Entité":
                    ent = entites[ent_idx]
                    if ent == "Hero": aventurier[0], aventurier[1] = (cy, cx), niv_sel
                    elif ent == "Dragon":
                        dragons, _ = test_objets(carte)
                        carte[cy][cx][1] = (dragons[0] + 1) if auto_dr else niv_sel
                    elif ent == "Trésor": carte[cy][cx][1] = -niv_sel
        
        if tev == "ClicDroit":
            cx, cy = abscisse(ev) // TAILLE_CASE, ordonnee(ev) // TAILLE_CASE
            if 0 <= cx < nb_w and 0 <= cy < nb_h:
                if aventurier[0] == (cy, cx): aventurier[0] = None
                else: carte[cy][cx][1] = None
        attente(0.01)