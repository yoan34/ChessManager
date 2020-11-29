'''
Classe qui représente la view du controlleur
'ControllerReport'.
'''

from .view import View

from ...constante import (
    SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, SMALL_DASH_TITLE, MEDIUM_DASH_TITLE
    )


class ViewReport(View):

    def title(self):
        print("{} Report {}\n".format(MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE).center(50))

    def report(self):
        print("{}In this page you can retrieve".format(MEDIUM_SPACE))
        print("{}informations about:".format(MEDIUM_SPACE))
        print("{}-Tournaments".format(LARGE_SPACE))
        print("{}-Players".format(LARGE_SPACE))
        print("{}and put them in a file.\n".format(MEDIUM_SPACE))
        print("{}See the help page to learn more.\n".format(MEDIUM_SPACE))

    def turn(self, turn):
        print("{}{} - {}".format(MEDIUM_SPACE, turn.name, turn.status))
        print("{}start at: {}".format(LARGE_SPACE, turn.start))
        print("{}end at: {}\n".format(LARGE_SPACE, turn.end))

    def help(self):
        print("{} helper {}\n".format(SMALL_DASH_TITLE, SMALL_DASH_TITLE).center(65))
        r = ''
        l1 = "\n{}All commands possible (* -> optional):\n\n".format(SMALL_SPACE)

        l2 = "{}The argument 'file' create and add the report in a the file\n".format(SMALL_SPACE)
        l3 = "{}in the appropriate folder.\n\n".format(SMALL_SPACE)

        l4 = "{}players <name> reverse* file*\n".format(MEDIUM_SPACE)
        l5 = "{}exemple: players rank  OR  players birth reverse file\n".format(LARGE_SPACE)
        l6 = "{}note: The <name> sort the players.\n".format(LARGE_SPACE)
        l7 = "{}<name> can be equal to 'id, firstname, lastname, sex,\n".format(LARGE_SPACE)
        l8 = "{}birth, rank, points, status and finished'\n\n\n".format(LARGE_SPACE)

        l9 = "{}players <id> file*\n".format(MEDIUM_SPACE)
        l10 = "{}exemple: players 4 OR players 12 file\n".format(LARGE_SPACE)
        l11 = "{}note: <id> represente an id of tournament to list the players.\n\n\n".format(LARGE_SPACE)

        l12 = "{}tournaments <name> reverse* file*\n".format(MEDIUM_SPACE)
        l13 = "{}exemple: tournaments date file\n".format(LARGE_SPACE)
        l14 = "{}<name> can be equal to 'id, name, place, country, date,\n".format(LARGE_SPACE)
        l15 = "{}max_turn, n_player, time, description, ids_player and status\n\n\n".format(LARGE_SPACE)

        l16 = "{}turns <id> file*\n".format(MEDIUM_SPACE)
        l17 = "{}exemple: turns 7 file\n".format(LARGE_SPACE)
        l18 = "{}note: show all turns in tournaments id=7 and print it in a file.\n\n\n".format(LARGE_SPACE)

        l19 = "{}matches <id> file*\n".format(MEDIUM_SPACE)
        l20 = "{}exemple: matches 22 \n".format(LARGE_SPACE)
        l21 = "{}note: show all matches in tournaments id=22.\n\n\n".format(LARGE_SPACE)

        r += (l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10 + l11 + l12 +
              l13 + l14 + l15 + l16 + l17 + l18 + l19 + l20 + l21)
        print(r)
