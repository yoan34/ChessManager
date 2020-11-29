'''
Classe qui représente la view du controlleur
'ControllerTournamentRegister'.
'''

from .view import View

from ...constante import SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, SMALL_DASH_TITLE, MEDIUM_DASH_TITLE


class ViewTournamentRegister(View):

    def tournament_focus_register(self, tournament):
        l1 = "{}The tournament has not started.\n\n".format(SMALL_SPACE)
        l2 = "{}{} Players register ({}/{}) {}\n".format(
            LARGE_SPACE, MEDIUM_DASH_TITLE, len(tournament.players), tournament.n_player, MEDIUM_DASH_TITLE)
        print(l1 + l2)

    def help(self):
        r = ''
        print("{} helper {}\n".format(SMALL_DASH_TITLE, SMALL_DASH_TITLE).center(65))
        l1 = "\n{}All commands possible:\n\n".format(SMALL_SPACE)

        l2 = "{}start\n".format(MEDIUM_SPACE)
        l3 = "{}note: only possible if all players are registered\n\n\n".format(LARGE_SPACE)

        l4 = "{}add id1 id2 id3\n".format(MEDIUM_SPACE)
        l5 = "{}exemple: add 1 45 22 3\n\n\n".format(LARGE_SPACE)

        l6 = "{}remove id1 id2 id3 id4... \n".format(MEDIUM_SPACE)
        l7 = "{}exemple: remove 1 22 3 4\n\n\n".format(LARGE_SPACE)

        l8 = "{}update <name1>=value1\n".format(MEDIUM_SPACE)
        l9 = "{}exemple: update country=france\n".format(LARGE_SPACE)
        l10 = "{}note: you can change name, place, country, description,\n".format(LARGE_SPACE)
        l11 = "{}n_turn, time\n".format(LARGE_SPACE)
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10 + l11
        print(r)

    def remove_player_registered_error(self, ids_in, ids_out):
        r = ''
        if ids_in:
            ids_in = ', '.join(map(str, ids_in))
            r += "\n{}Player unregistered ({}).".format(SMALL_SPACE, ids_in)
        if ids_out:
            ids_out = ', '.join(map(str, ids_out))
            r += "\n{}Player(s) not in this tournament ({}).".format(SMALL_SPACE, ids_out)
        return r

    def ids_not_place_error(self, ids, place):
        r = ''
        played_ids = ', '.join(map(str, ids[place:]))
        if place:
            r += "\n{}Tournament if full. Can take player(s) with id ({}).".format(
                SMALL_SPACE, played_ids) if played_ids else ''
        else:
            r += "\n{}Tournament is full.".format(SMALL_SPACE)
        return r
