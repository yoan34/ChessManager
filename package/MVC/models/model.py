'''
Classe hérité des models 'Tournament' et 'Player'.
On y trouve des méthodes pour formater les différentes
dates et points de joueur.
'''

import datetime


class Model:

    def _format_birth_to_datetime(self, array, attr):
        for p in array:
            value = datetime.date(*list(reversed(list(map(int, getattr(p, attr).split('/'))))))
            setattr(p, attr, value)

    def _format_datetime_to_birth(self, array, attr):
        for p in array:
            value = "{:02}/{:02}/{}".format(getattr(p, attr).day, getattr(p, attr).month, getattr(p, attr).year)
            setattr(p, attr, value)

    def _format_birth(self, date, sep):
        arr = list(map(int, date.split(sep)))
        return "{:02}/{:02}/{}".format(arr[0], arr[1], arr[2])

    def _format_points_to_number(self, players):
        for p in players:
            if p.status[0] != 'p':
                p.points = -1

    def _format_points_to_str(self, players):
        for p in players:
            if p.status[0] != 'p':
                p.points = ''
