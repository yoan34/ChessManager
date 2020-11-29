'''
Ce fichier permet de créer des joueurs aléatiores pour simuler une partie
du programme. On peut changer le nombre de joueurs crée en changeant la
constante 'RANDOM_PLAYER' dans le fichier 'constante.py'.
'''

from package.random.player import get_random_player
from package.MVC.models.player import ModelPlayer

from package.constante import RANDOM_PLAYER

model = ModelPlayer()

for i in range(RANDOM_PLAYER):
    player = get_random_player()
    model.create(player)
