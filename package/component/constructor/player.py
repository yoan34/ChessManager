'''
Classes qui permet de créer les joueurs.
    -serialize(): retourne sous forme de dictionnaire le joueur.
    -deserialize(): retourne sous forme de classe le joueur.
'''


class Player:

    def __init__(self, lastname, firstname, sex, birth, rank, points='',
                 status='available', opponent=-1, ids_tournaments=[], id=-1):
        self.lastname = lastname
        self.firstname = firstname
        self.sex = sex
        self.birth = birth
        self.rank = rank
        self.points = points
        self.status = status
        self.opponent = opponent
        self.ids_tournaments = ids_tournaments
        self.id = id

    def serialize(self):
        data = {}
        for attr in list(self.__dict__.keys())[:-1]:
            data[attr] = self.__dict__[attr]
        return data

    @classmethod
    def deserialize(self, player):
        return Player(**player)
