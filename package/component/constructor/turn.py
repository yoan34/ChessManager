'''
Classes qui permet de créer les tours.
    -serialize(): retourne sous forme de dictionnaire le tour.
    -deserialize(): retourne sous forme de classe le tour.
'''

from datetime import datetime
from .match import Match


class Turn:

    def __init__(self, n, name='', start='', end='', matchs=[], status='play'):
        self.n = n
        self.name = 'Turn ' + str(n+1) if not name else name
        self.matchs = [Match(**match) for match in matchs]
        if not start:
            date = datetime.today()
            self.start = "{:02}/{:02}/{} at {:02}:{:02}".format(
                date.day, date.month, date.year, date.hour, date.minute)
        else:
            self.start = start
        self.end = end
        self.status = status

    def serialize(self):
        data = {}
        for attr in self.__dict__:
            if isinstance(self.__dict__[attr], list):
                data[attr] = [item.serialize() if isinstance(item, Match) else item for item in self.__dict__[attr]]
            else:
                data[attr] = self.__dict__[attr]

        return data

    @classmethod
    def deserialize(self, turns):
        return [Turn(**turn) for turn in turns]
