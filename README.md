# Projet :: ovarena

Dans l'optique du Projet Open Innovation à l'ESPI Rennes,
Création d'une arène de compétition inter-écoles.

L'objectif est que les participants puissent apprendre la programmation par un moyen ludique.

Les sessions de challenges peuvent se présenter sous plusieurs formats : 
- 2H
- 4H
- 8H

Des interfaces permettent aux apprenants les moins avancés d'avoir des briques logiques pré-construites, afin de passer de la théorie à la pratique rapidement en utilisant son robot.

Pour les sessions les plus longues, nous n'offirons pas ces possibilités aux aprenants.

# minova
Description courte du projet
...

## Règles du jeu 
##### Maquette


##### Déroulé d'une partie:
	- Les joueurs arrivent à un emplacement aléatoire, défini sur les bords de la grille.
	- Chaque joueur possède un temps de préparation, afin d'apprendre à son robot à naviguer dans un labyrinthe sombre, exigüe, et rempli de de mésaventures
    - Lors de la 'compétition', chaque joueur aura TROIS essais pour trouver la sortie le plus rapidement possible. Ils apparaitront toujours aux mêmes emplacements.
    - L'objectif de chacun est d'entrainer un algorithme capable de se souvenir des chemins déjà empruntés par son robot, et de déterminer si un chemin est plus rapide à prendre qu'un autre pour gagner un maximum de points.


##### conditions de victoire :
	- ...

## Use cases

Un joueur peut : 
 - voir ce que son robot voit
 - avancer son robot
 - pivoter son robot
 - avoir accès à une boussole, lui permettant de connaitre son orientation dans le labyrinthe
 - perdre des points en cas de colision avec un mur
 - perdre des points à chaque mouvement sur une case 'lente'
 - gagner des points pour chaque seconde **en déplacement** où il n'y a pas eu de colisions
 - gagner une grande quantité de points en trouvant la **__Batterie__**
 - continuer d'explorer jusqu'à ce que le temps soit écoulé, ou que son score atteint 0

L'arbitre peut :
 	- voir toute la map
	- changer les scores des joueurs pour appliquer les règles
 	- tuer un joueur si son score est de 0
  	- faire gagner des avantages à des joueurs pour leurs découvertes dans le labyrinthe

 
## Pré-requis
- pour utiliser le projet:
Python >= 3.10


- pour utiliser le manager de jeu: (permet de changer les règles)
un fichier .env, avec les valeurs suivantes:

```txt
ARBITRE_NAME=nom_de_larbitre_arene_pour_gerer_les_regles_et_le_jeu
ARENA_NAME=nom_de_larene_ou_tu_souhaite_te_connecter
ARENA_PLAYER_PASS=aPassword_sinon_ca_ne_fonctionnera_pas
```


##  Installation 
Step by step : commandes à executer, paquets à installer ...

```shell
python -m venv venv
```
#### Windows :

```shell
./venv/Scripts/pip install -r requirements.txt
```
#### Linux :

```shell
./venv/lib/pip install -r requirements.txt
```

## How to run (prendre le contrôle d'OVA physique)

#### Windows :

```shell
./venv/Scripts/python ./src/api/ova-demo.py
```
#### Linux :

```shell
./venv/lib/python ./src/api/ova-demo.py
```

##  Auteur(s)
Rendre à César ce qui appartient à César !
N'oublier pas de citer toutes les personnes qui ont contribué directement (vous) ou indirectement (les auteurs des dépendances de votre projet, des ressources récupérées ou générées ...)

Mistayan : Stephen Proust @EPSI I1
ThimoteeG : Thimotee Garot @EPSI I1
ThimoteeL : Thimotee Lerailler @EPSI I1

JusDeLiens : Julien Arne @jusdeliens.com : fondateur

##  License
MIT 

...
S'appuyer sur https://choosealicense.com/ ou la doc de github
Attention à vérifier la compatibilité de votre licence avec celles des modules utilisés


## Liens utiles :

Voir l'aèrne : 
https://play.jusdeliens.com/tactx/

Voir l'avancement du projet :
https://jusdeliens.com/epsirennesopeninno2324

découvrir jusdeliens :
https://jusdeliens.com/bienvenue/

comment se connecter à OVA ?
https://tutos.jusdeliens.com/index.php/2023/01/17/onboarding/

comprendre comment utiliser l'interface graphique en ligne (pytactx, arène virtuelle):
https://tutos.jusdeliens.com/index.php/2020/01/14/pytactx-prise-en-main/

comprendre comment arbitrer une partie : 
https://tutos.jusdeliens.com/index.php/2023/04/27/pytactx-creez-vos-propres-regles-du-jeu/

jouer à la manette (non disponnible dans ce projet) :
https://tutos.jusdeliens.com/index.php/2020/05/10/piloter-votre-agent-pytactx-avec-une-manette-en-html/

Autres jeux développés par les apprenants de JusDeLiens : 
https://github.com/azemazer/bomberguys