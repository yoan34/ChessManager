'''
Classes qui permet de créer les matches.
On crée à l'aide du module random la couleur que
le joueur aura lors du match.
Différentes méthodes:
    -write(id): stock le gagnant.
    -read(): récupère le patch sous forme de liste.
    -serialize(): retourne sous forme de dictionnaire le match
    -deserialize(): retourne sous forme de classe le match.
'''

from random import choice
from ..exception import PlayerNotFound

from ...constante import SMALL_SPACE


class Match:

    def __init__(self, id1, id2, n, score_id1=0.0, score_id2=0.0, color_id1='', color_id2='', status='play', name=''):
        self.id1 = id1
        self.id2 = id2
        self.score_id1 = score_id1
        self.score_id2 = score_id2
        self.color_id1 = color_id1 if color_id1 else choice(('W', 'B'))
        self.color_id2 = color_id2 if color_id2 else 'B' if self.color_id1 == 'W' else 'W'
        self.n = n
        self.status = status
        self.name = 'Match ' + str(n+1) if not name else name

    def read(self):
        return ([self.id1, self.score_id1], [self.id2, self.score_id2])

    def write(self, id):

        if id == 0:
            self.score_id1 = self.score_id2 = 0.5
            self.status = 'equality'
        elif id == self.id2:
            self.score_id2, self.score_id1 = 1, 0
            self.status = 'winner'
        elif id == self.id1:
            self.score_id1, self.score_id2 = 1, 0
            self.status = 'winner'
        else:
            raise PlayerNotFound("{}ID player doesn't exist.".format(SMALL_SPACE))

    def serialize(self):
        data = {}
        for attr in self.__dict__:
            data[attr] = self.__dict__[attr]
        return data

    @classmethod
    def deserialize(self, matchs):
        # Ici on doit recréer également les tours et les matchs avec
        # les constructor Match et Turn
        return [Match(**match) for match in matchs]
