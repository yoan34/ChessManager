Installation du programme:</br>
<b>git clone https://github.com/yoan34/ChessManager.git </b>

On va dans le répertoire du projet et crée un espace virtuel:</br>
<b> cd ChessManager && python -m venv env </b>

On active l'espace virtuel et installe les dépendances:</br>
<b> .\env\scripts\actvate && pip install -r requirements.txt </b>

Pour créer un rapport flake8-html on utile cette commande:</br>
<b>flake8 --format=html --htmldir=flake-report</b>

Pour lancer le programme:</br>
<b>python main.py</b>

Le programme consiste en plusieurs menus/pages pour intéragir
avec la base de donnée des joueurs, des tournois.

Il y a 4 menu:</br>
<b>1 - créer</b> d'un tournoi.</br>

<b>2 - supprimer/changer/trier</b> les tournois.</br>
changer un tournoi nous amène dans une nouvelle page ou </br>
l'on peut ajouter des joueurs pour lancer le tournoi.</br>Ensuite on peut entrer les résultats de matchs, passer</br> au tour suivant jusqu'à la fin du tournoi.</br>
<b>3 - créer/supprimer/changer/trier</b> les joueurs.</br>
<b>4 - Créer</b> des rapports de différents type et imprimable sur fichier.

On peut également créer des joueurs aléatoire avant le lancement du
programme avec <b>python random_player.py</b>



