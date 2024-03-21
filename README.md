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
- [ ] Maximum 5 robot dans l'arène réelle
- [ ] Maximum 1 robots par 10x5 sur une arène virtuelle
- [ ] Quand un joueur entre en colision avec un mur, le joueur perd 0,5 points
- [ ] Quand un joueur avance sur une case autre que du sol (#floor), le joueur perd 0,2 point
- [ ] Toutes les 1 secondes sur une case autre que le sol, le joueur perd 0,1 point
- [ ] Si un joueur avance depuis plus de 3 secondes sans incidents, gagne 0,1 point par seconde.
- [ ] Si un joueur trouve la **__Batterie__**, il gagne **30 points**.
- [ ] Un match dure __3 minutes 20 secondes__.

##### Maquette


##### Déroulé d'une partie:
	- Les joueurs arrivent à un emplacement aléatoire, défini sur les bords de la grille.
	- Chaque joueur possède un temps de préparation, afin d'apprendre à son robot à naviguer dans un labyrinthe sombre, exigüe, et rempli de de mésaventures
    - Lors de la 'compétition', chaque joueur aura TROIS essais pour trouver la **__Batterie__** et accumuler le maximum de points
    - L'objectif de chacun est d'entrainer un algorithme capable de se souvenir des chemins déjà empruntés par son robot, et de déterminer si un chemin est plus rapide à prendre qu'un autre pour trouver la batterie avant tout le monde, et accumuler un maximum de points.


## conditions de victoire :
   Le maximum de points théorique est de : 89.1
   Sur 3 matchs distincts (total 10 minutes de compétition), l'objectif est d'accumuler un maximum de points 
Il est possible d'être éliminé (les points ne sont pas perdus), si un joueur est touché 3 fois par Minova

## Use cases

Un joueur peut :
 - [ ] Utiliser OVA avec IRobot dans un labyrinthe réel, ou l'agent virtuel avec pytactx
 - [ ] voir ce que son robot voit
 - [ ] mémoriser la carte de la manière de son choix
 - [ ] avancer son robot
 - [ ] pivoter son robot
 - [ ] avoir accès à une boussole, lui permettant de connaitre son orientation dans le labyrinthe
 - [ ] perdre des points en cas de colision avec un mur
 - [ ] perdre des points à chaque mouvement sur une case 'lente'
 - [ ] gagner des points pour chaque seconde **en déplacement** où il n'y a pas eu de colisions (actif au bout de 3 seconde)
 - [ ] gagner une grande quantité de points en trouvant la **__Batterie__**
 - [ ] continuer d'explorer jusqu'à ce que le temps soit écoulé, ou qu'il soit éliminé 


L'arbitre peut :
- [x] définir les règles du jeu
- [ ] faire apparaître les joueurs à des emplacements défini par lui-même.
- [ ] changer la map entre chaque partie ?
- [x] voir toute la map
- [ ] ajouter ce que le joueur voit du labyrinthe à sa map personnelle
- [ ] changer les scores des joueurs pour appliquer les règles
- [x] tuer un joueur
- [ ] faire gagner des points et avantages à des joueurs pour leurs découvertes dans le labyrinthe
- [ ] infliger des pénalités aux joueurs, si ils tapent un mur ou se déplacent sur une case 'lente'



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
Les produits de jusdeliens sont sous license CC BY-NC-ND 3.0

Le code produit est sous license Open Source (MIT)



## Liens utiles :

Voir l'aèrne : 
https://play.jusdeliens.com/tactx/

Récupérer la dernière version de pytactx, pour développer vos propres jeux :
https://replit.com/@jusdeliens/pytactxv2

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