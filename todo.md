#  Plan d'attaque de la conception du jeu
- [x] Définir un groupe de 3-4 personnes
- [x] Présentation de votre proposition de votre jeu à l'oral
- [x] Créer un projet github/gitlab et partager les droits à toute l'équipe et jusdeliens-pedago
- [x] Définir et répartir les tâches dans un kanban (trello) 
	- 1 responsable développement API : définir les fonctions pour chaque use case du joueur
	- 1 responsable test API : assert de toutes les fonctions de l'API
	- 1 responsable arbitre de l'arÃ¨ne : suivre le tutos.jusdeliens.com et implémenter les règles du jeu
	- 1 responsable README : description, use case, maquette
- [x] Définir tous les use cases des utilisateurs joueurs sur un readme
- [ ] Faire une maquette à insérer dans votre readme (figma, paint, powerpoint ...)
- [ ] Trouver/créer ressources libres de droit pour 
	- le fond de l'arène
	- le logo/preview dans le launcher 
- [x] Lire le champs des possibles de votre arbitre sur tutos.jusdeliens
- [x] Transmettre les nom de vos arbitres pour la création de vos arÃ¨nes
- [ ] Définir les responsabilités de chaque arbitre de votre groupe : initialisation resources, gestion score, gestion carte ...
- [ ] Choisir les fonctions de votre API en Python
- [ ] Réaliser les tests de l'API : créer des agents automatiquement et vérifier que toutes les actions marchent comme elles devraient

# Arborescence projet Github
- votrejeu
	- doc                   -> *ressources utilisées dans vos readme: maquette, diagrammes*
		- *.svg
		- *.png
		- *.jpg
	- res                   -> *ressources utilisées dans vos jeux: sprites, image arrière plan*
		- *.svg
		- *.png
		- *.jpg
	- src
		- api
			- j2l           -> *lib jusdeliens Ã  récupérer sur tutos.jusdeliens.com* 
			- votrejeu.py   -> *interface API de votre jeu côté client*
			- readme.md     -> *explique au joueur les actions possibles de l'api*
		- server
			- res           -> *dossier des ressources de votre jeu*
			- main.py       -> *logique backend implémentant les règles du jeu*
	- tests
		- api
			- test_votrejeu.py
		- server
			- test_main.py
	- readme.md             -> *inclus diagramme de conception du dossier doc*

# Dev de votre API en TDD
1. Définir l'interface de l'API du jeu pour respecter les US de l'utilisateur joueur
	- 1 méthode update() pour actualiser votre classe joueur et synchroniser son état et requêtes avec le server
	- 1 constructeur prennant en paramètre au minimum : playerId, arena, le serveur et son port, username et password
	 Méthodes et attributs en anglais, avec la même convention de nommage (en snake case ou camel case) 

2. Ecrire les tests de l'interface dans le fichier "test_*" correspondant à chaque fichier * de l'API. 

...

# Dev de votre server

1. A partir du tutoriel tutos.jusdeliens.com  "Créer vos propres règles du jeu"
- Téléchargez le dernier zip pytactx 
- Créer votre main.py dans votre dossier server recopiez le sample de l'arbitre pour comprendre les règles du jeu  

2. Nommer votre arbitre dans votre .env (NE PAS LE COMMIT):
```
@arenaname  
```
**arenaname** Ã  remplacer par le nom de l'arène
ex: @spythoon pour l'arène spythoon

3. Utiliser les mÃ©thodes **ruleArena** et **rulePlayer** en bac Ã  sable pour tester le bon fonctionnement des modifications du serveur
	- Redemarrer l'arène
	```python
	arbiter.ruleArena("reset", True)
	```
	- Modifier le infinite ammo de tous les joueurs par défaut (profile = 0)
	```python
	infiniteAmmoRule = arbiter.game["infiniteAmmo"]
	infiniteAmmoRule[0] = True #Modifie uniquement pour le 1er porfile (0)
	arbiter.ruleArena("infiniteAmmo", infiniteAmmoRule)
	arbiter.update()
	```
	- Créer des joueurs dans différentes équipes à différentes positions sur la carte
	```python
	agents = {
		"joueur1": {
			"team": 0,
			"x": 5,
			"y": 10
		},
		"joueur2": {
			"team": 1,
			"x": 15,
			"y": 10
		},
		"ball": {
			"playerId": "",
			"profile": 4,
			"x": 15,
			"y": 10
		}
	}
	for agentId, attributes in agents.items():
		for attributeKey, attributeValue in attributes.items():
			arbitre.rulePlayer(agentId, attributeKey, attributeValue)
	arbiter.update()
	```

4. Développer en CDD la logique de votre server dans votre main.py
```python
#0. Reset de l'arÃ¨ne
#1. Initialiser les règles du jeu : changer graphiques, et logiques, profiles des joueurs ...
#2. CrÃ©er les agents avec le bon profile et les bons Ã©tats
#3. Fermer l'arÃ¨ne pour interdire la venue de nouveaux agents non autorisÃ©s
#4. Dans votre boucle principale : tant que le jeu tourne
	#4.1. RÃ©cupÃ©rer les requÃªtes et infos des joueurs dans le range de l'arbitre
	#4.2. Si le range change (ex: nFire pour check si un agent Ã  tirÃ©), 
		# 4.3. mettre Ã  jour les rÃ¨gles du jeu (ex: appliquer acceleration sur agent, ou changer Ã©tat de la map)
	#4.5. Sauvegarder le nouveau range avant de reboucler
	#4.6. GÃ©rer condition de fin de jeu : fin du dÃ©lai rÃ©glementaire, morts des joueurs d'une Ã©quipe ...
```