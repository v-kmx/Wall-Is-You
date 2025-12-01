# Wall-Is-You
A "Dungeon &amp; Dragons" rogue-like game project entirely made in Python w/ FLTK  

SAE 1.01: Implémentation d'un besoin client | Rendu N°1
Projet : Wall Is You
Groupe 8 : KITADI MUNDUNGA Vianney, PENNETIER-MSIKA Elie, DIOURI-ADEQUIN Noam

/!\ Le fichier à executer pour lancer le jeu est main_handler.py /!\\


Ce projet a pour objectif de nous faire réaliser une structure de jeu avec des menues des sauvegardes.

Nous avons décidé de séparer le programme en deux sous-programmes, une partie qui se charge des menues et l'autre qui se charge du jeu.
Chacun de ses sous-programmes est également divisé en deux sous-programmes.
La partie menu est séparée entre un programme qui gère le visuel (appelé menu) et un autre qui s'occupe de lancer chaque programme quand c'est nécessaire (c'est grâce à ce dernier que l'on peut utiliser une seule fenêtre à travers toutes les boucles de jeux), celui est ci est appelé main_handler.
Du côté du jeu, la séparation est plutôt simple, nous avons une partie graphique, appelé wall_is_you_graphic, qui gère l’aspect visuel ainsi que les interactions utilisateur, de l'autre, le code wall_is_you_main qui possède les principales fonctions permettant de faire tourner le jeu correctement.

Les différentes tâches pour la conception du jeux on été réparties pour que chacun d'entre nous puisse avoir une part de travail plus ou moins égale. Elie eut pour mission d'assurer le fonctionnement de la partie logique du jeu (le moteur), Noam lui eut pour mission d'implémenter l'affichage graphique de base FLTK et Vianney eut pour mission d'implémenter un Menu Principal, les textures du jeu, les commandes et la liaison des différents programmes (Moteur Logique, Moteur Graphique et Menu)

/!\ Le fichier à executer pour lancer le jeu est main_handler.py /!\

Les 3 principales structures de données que nous avons utilisé sont:
-Une carte, correspondant à une matrice (liste de listes) qui, à chaque coordonnée, associe une liste de ses sorties (représenté par True si ouvert ou False si fermé) et le contenu de sa case (dragon, objet (dans une version plus développée)).

-L’intention, une liste de positions valides par lesquelles l'aventurier/ère va se déplacer (les positions étant représentées par des tuples i,j).

-L'aventurier, une liste composé de sa position actuelle (qui n'est alors pas stockée sur la carte) et de son niveau.

L'utilisateur n'a que 2 options pour jouer, soit il charge un niveau qui a déjà été enregistré, soit il lance une nouvelle partie, les parties sont créées de manière aléatoire et auront besoin d'être retravaillé pour les rendre réalisables lorsque l'intention sera automatique.

Les cases ont donc 1,2,3 ou 4 sortie aléatoirement placée dans tout le tableau, elles ont aussi environ 4% de chance de contenir un dragon, les niveaux des dragons étant choisis de manière incrémenté (s'il y a un unique dragon dans le donjon, sont niveau sera 1, s'il y en a 2 il y en aura 1 de niveau 1 et 1 de niveau 2).
Les booléen représentant les portes des cases corresponde à un sens, l'indice 0 correspond à la gauche, 1, le haut, 2 le bas et 3 la droite.

Pour la sauvegarde, n'arrivant pas à trouver les caractères spéciaux permettant de le rendre concis et simple, nous sommes parti pour que chaque ligne corresponde à des informations précises, les deux premières lignes contiennent uniquement la position et le niveau du personnage, après un certain nombre de ligne stocke l'intention (une ligne par position contenue dans l'intention) et enfin toutes les cases plus 1 ont leurs informations stockés +1 car il faut également prendre en compte la taille de la carte (stocker en première ligne avant les informations des cases), les informations des cases sont, leurs coordonnées, leurs sorties, leurs contenus (objet, monstre).


Durant ce projet nous avons rencontré de nombreux problèmes, dont les plus mémorables sont énumérer ici:

-L'intention et sa représentation, certainement la partie de code qui a le plus été refait, au minimum 4 à 5 versions ont été codé, principalement car nous n'arrivions pas à correctement implémenter la fonction "vérif_intention" et qu'elle provoquait de nombreuses erreurs. La représentation de celle-ci a été aussi un enfer, car comme les positions de fltk sont à l'envers il fallait constamment échanger les valeurs x et y (si vous lisez le code de la fonction "dessiner_intention" vous verrez que les positions x et y sont échanger. Une autre difficulté de cette fonction c'était de trouver la formule permettant de calculer le point au milieu des cases, les tests de cette formule pouvant encore être retrouvé dans le code de cette fonction.

- (Noam) L’utilisation de constantes numériques mal documentées lors de la création de l’interface graphique. Ce projet étant le premier projet de programmation d’un des membres de notre groupe, Noam, il a commis l’erreur de prioriser l’utilisation de constantes de longueurs au lieu d’utiliser une variable. L’interface graphique s’est réalisée dans les premiers stades de développement et à donc été cause de problème à l’avancement du projet. C’est une erreur qu’il ne refera pas. 

-La rotation des cases, cette fois-ci le blâme est sur moi (elie), j'ai vraiment galéré à faire fonctionner la fonction "tourner_case" de Wall_is_you_main car je n'arrivais pas à me faire l'image de comment je devais faire tourner, la personne qui m'a aidé à résoudre ce problème est mon père (qui est technicien du vide, j'ai honte qu'il ait mieux compris mon code que moi-même).

-Le chargement, le problème du chargement était de traduire des lignes de chaîne de caractère en donnée utilisable par le programme, comme plusieurs données sont presque collées les unes aux autres je ne pouvais pas juste faire une boucle et tout récupérer, qui plus est j'avais un bug qui m’empêchait d'utiliser des coordonnées à deux chiffres (une fonction que j'utilise pour décrypter des chiffres s’arrêtaient à une virgule et ne renvoyait rien faisant crasher le programme) la solution: changer un [:3] en une longueur variable, j’ai passé 3 heures à résoudre ce problème.

- (Vianney) L'implémentation des textures des salles afin que ces dernières puissent se positionner au niveau de chaque case, ne pas prendre trop d'espace, ne pas sortir du cadre de la salle. La résolution se fit par le changement des valeurs de position mais également des valeurs permettant de changer la taille d'une image (fonction image() FLTK).

- (Vianney) Difficulté à relier les programmes entre eux. Il s'agissait d'une problématique majeure étant donné que nous ne voulions point tout condenser en un seul programme. Nous avons donc réalisé des programmes annexes à main_handler.py qui s'occupe de tout embarquer et qui, à travers l'utilisation de returns "ordre" dans les programmes annexes, permet d'effectuer les actions voulues et relier tous les programmes entre eux par l'intermédiaire d'un seul programme ce qui vise à rendre les programmes plus lisibles, plus compréhensibles, pour s'aider lorsque le projet avancera (futures tâches, afin de s'y retrouver) mais également d'un point de vue des performances machines.


----------------------------
Toutes les ressources graphiques extérieures (images) sont contenues dans le répertoire ressources -> img
----------------------------
Sources
- Sprite Dragon Libre de droits : https://michael-jay-rov.itch.io/american-dragon
- Texture des fonds de salle: https://www.freepik.com -> Modifiés sur Microsoft Paint
- Documentation FLTK : https://fltk-b9f35a.frama.io/index.html
- Splash art (logo) Wall is You fait par Vianney sur PIXLR
- Utilisation des librairies standard de Python : https://docs.python.org/3/library/
- Sprite de l'aventurier : https://craftpix.net/freebies/free-swordsman-1-3-level-pixel-top-down-sprite-character-pack/?srsltid=AfmBOoq5e39PqaSoCdFOVx1DoshpYnHRQNUkiZ15pPnnpYKIa5V6elek

Merci d'avoir lu ce rapport,

PS : Si je peux vous donner un petit conseil, vous remarquerez certainement la fonction "verif_ee" dans Wall_is_you_graphic", je vous invite à taper sur e, puis le Konami Code (Sans B + A + START soit Entrée // avant d'aller vérifier ce que la fonction "ee" contenu dans Wall_is_you_main fais)

Par PENNETIER-MSIKA Elie, DIOURI-ADEQUIN Noam et KITADI MUNDUNGA Vianney
