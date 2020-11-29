'''
Classe qui représente la view du controlleur
'ControllerTournamentPlay'.
'''

from .view import View

from ...constante import SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, SMALL_DASH_TITLE


class ViewTournamentPlay(View):

    def tournament_focus_play(self, tournament, index):
        len_id = len(str(max([p for p in tournament.players])))
        on_turn = len(tournament.turns)
        l1 = "{}The tournament is in turn {}.  \n\n".format(LARGE_SPACE, on_turn)
        turn = tournament.turns[index]
        date_left = str(turn.start).center(30, '-')
        date_right = str(turn.end).center((28 + len_id - 1), '-')
        l2 = "{}+{} {} {}+\n".format(MEDIUM_SPACE, date_left, turn.name, date_right)
        l3 = '{}|{}|'.format(MEDIUM_SPACE, ' '*(66 + len_id - 1))
        print(l1 + l2 + l3)

    def help(self):
        r = ''
        print("{} helper {}\n".format(SMALL_DASH_TITLE, SMALL_DASH_TITLE).center(65))
        l1 = "\n{}All commands possible:\n\n".format(SMALL_SPACE)
        l2 = "{}next\n".format(MEDIUM_SPACE)
        l3 = "{}note: only possible if all matchs of the current turn is finish. \n\n\n".format(LARGE_SPACE)

        l4 = "{}match id winner id  OR  m id w id \n".format(MEDIUM_SPACE)
        l5 = "{}exemple: match 7 winner 75  OR  m 7 w 75\n\n\n".format(LARGE_SPACE)

        l6 = "{}update <name1>=value1 <name2>=value2\n".format(MEDIUM_SPACE)
        l7 = "{}exemple: update country=france\n".format(LARGE_SPACE)
        l8 = "{}note: you can change place, country, description\n".format(LARGE_SPACE)
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8
        print(r)
