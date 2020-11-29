'''
Classes qui permet de créer les tournaments.
    -serialize(): retourne sous forme de dictionnaire le tournament.
    -deserialize(): retourne sous forme de classe le tournament.
'''

from datetime import datetime

from .turn import Turn


class Tournament:

    def __init__(self, name, place, country, time, date='', n_player=8, n_turn=4, description='',
                 turns=[], players=[], ranking=[], status='register', id=-1):
        self.name = name
        self.place = place
        self.country = country
        self.time = time
        self.n_player = n_player
        self.n_turn = n_turn
        self.description = description
        if date:
            self.date = date
        else:
            self.date = "{}/{}/{}".format(
                datetime.today().day, datetime.today().month, datetime.today().year)
        self.players = players
        self.turns = [Turn(**turn) for turn in turns]
        self.status = status
        self.ranking = ranking
        self.id = id

    def serialize(self):
        data = {}
        for attr in self.__dict__:
            if isinstance(self.__dict__[attr], list):
                data[attr] = [item.serialize() if isinstance(item, Turn) else item for item in self.__dict__[attr]]
            else:
                data[attr] = self.__dict__[attr]

        return data

    @classmethod
    def deserialize(self, tournament):
        return Tournament(**tournament)
