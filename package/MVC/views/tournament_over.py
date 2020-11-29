'''
Classe qui représente la view du controlleur
'ControllerTournamentOver'.
'''

from .view import View

from ...constante import (
    SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, MEDIUM_DASH_TITLE, MAX_CHAR_NAME_NO_GRID
    )


class ViewTournamentOver(View):

    POSITION = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth')

    def tournament_focus_over(self, tournament, index):
        len_id = len(str(max([p for p in tournament.players])))
        l1 = "{}The tournament is finish.  \n\n".format(LARGE_SPACE)
        turn = tournament.turns[index]
        date_left = str(turn.start).center(30, '-')
        date_right = str(turn.end).center((28 + len_id - 1), '-')
        l2 = "{}+{} {} {}+\n".format(MEDIUM_SPACE, date_left, turn.name, date_right)
        l3 = '{}|{}|'.format(MEDIUM_SPACE, ' '*(66 + len_id - 1))
        print(l1 + l2 + l3)

    def result(self, tournament):
        r = ''
        l1 = "{}The tournament is finish.  \n\n".format(LARGE_SPACE)
        l2 = "{}{} Ranking {}\n".format(MEDIUM_SPACE, MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE)
        r += l1 + l2
        print(r)

        for i, item in enumerate(tournament.ranking):
            name = "{} {}".format(item[3], item[4])
            if len(name) > MAX_CHAR_NAME_NO_GRID:
                name = name[:MAX_CHAR_NAME_NO_GRID - 4] + '... '
            name = name.ljust(MAX_CHAR_NAME_NO_GRID)
            rank = ' ' * (4 - len(str(item[2]))) + str(item[2])
            point = ' ' * (3 - len(str(item[1]))) + str(item[1])
            position = ' ' * (8 - len(str(ViewTournamentOver.POSITION[i]))) + str(ViewTournamentOver.POSITION[i])
            print("{} {} {} with {} pts - rank: {}".format(SMALL_SPACE, position, name, point, rank))
        print(MEDIUM_SPACE + '-'*(len(l2)-10))
