import wall_is_you_graphic_automatique
import wall_is_you_graphic

def main():
    fichier_sauvegarde=open("save/caracteristique_dernier_donjon.txt","r")
    lignes=fichier_sauvegarde.readlines()
    if lignes[0]=="A":
        wall_is_you_graphic_automatique.main(-1,lignes[-1]=="T")
    else:
        wall_is_you_graphic.main(-1,lignes[-1]=="T")
    return "quitter"
        
