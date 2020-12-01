'''
Classe qui représente la view du controlleur
'ControllerTournament'.
'''

from .view import View

from ...constante import (
    SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, SMALL_DASH_TITLE, MEDIUM_DASH_TITLE,
    MAX_CHAR_DESCRIPTION, MAX_CHAR_NAME, MAX_CHAR_PLACE, MAX_CHAR_IDS_PLAYERS
    )


class ViewTournament(View):

    HEADERS = ('id', 'name', 'place', 'country', 'date', 'turn', 'n player', 'time',
               'description', 'ids players', 'status')

    def read_all(self, tournaments):
        data = [ViewTournament.HEADERS]
        for t in tournaments:
            description = (t.description if len(t.description) <= MAX_CHAR_DESCRIPTION
                           else t.description[:MAX_CHAR_DESCRIPTION - 3] + '...')
            name = (t.name if len(t.name) <= MAX_CHAR_NAME else t.name[:MAX_CHAR_NAME - 3] + '...')
            place = (t.place if len(t.place) <= MAX_CHAR_PLACE else t.name[:MAX_CHAR_PLACE - 3] + '...')
            ids_players = ', '.join(map(str, t.players))
            ids_players = (ids_players if len(ids_players) <= MAX_CHAR_IDS_PLAYERS
                           else ids_players[:MAX_CHAR_IDS_PLAYERS - 3] + '...')
            n_player = "{}/{}".format(len(t.players), t.n_player)

            row = (str(t.id), name, place, t.country, t.date, str(t.n_turn), n_player,
                   t.time, description, ids_players, t.status)
            data.append(row)
        self.grid(data)

    def title(self):
        print("{} List of tournaments {}\n".format(MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE).center(100))

    def help(self):
        r = ''
        print("{} helper {}\n".format(SMALL_DASH_TITLE, SMALL_DASH_TITLE).center(65))
        l1 = "\n{}All commands possible (* -> optional):\n\n".format(SMALL_SPACE)

        l2 = "{}sort <name> reverse*\n".format(MEDIUM_SPACE)
        l3 = "{}exemple: sort date OR sort max_turn reverse\n".format(LARGE_SPACE)
        l4 = "{}note: <name> can be equal to 'id, name, place, country, date,\n".format(LARGE_SPACE)
        l5 = "{}max_turn, n_player, time, description, ids_player, status\n\n\n".format(LARGE_SPACE)

        l6 = "{}focus id\n".format(MEDIUM_SPACE)
        l7 = "{}note: this will take you to the page to change\n".format(LARGE_SPACE)
        l8 = "{}some tournament information \n\n\n".format(LARGE_SPACE)

        l9 = "{}delete id1 id2 id3 id4... \n".format(MEDIUM_SPACE)
        l10 = "{}exemple: delete 1, 2, 3, 4\n".format(LARGE_SPACE)
        l11 = "{}note: can't delete a tournament with status=play\n".format(LARGE_SPACE)
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10 + l11
        print(r)

    # Affiche les erreurs lié aux IDs des joueurs.
    def ids_error(self, wrong, played, good):
        r = ''
        wrong = list(set(wrong))
        played = list(set(played))
        good = list(set(good))
        r += self.id_exist(good) if good else ''
        r += self.id_no_exist_error(wrong) if wrong else ''
        r += self.id_on_play_error(played) if played else ''
        return r

    def id_exist(self, ids):
        ids = ', '.join(map(str, ids))
        return "\n{}Tournament(s) with id ({}) are delete.".format(SMALL_SPACE, ids)

    def id_no_exist_error(self, ids):
        wrong_ids = ', '.join(map(str, ids))
        return "\n{}Tournament(s) with id ({}) doesn't exist.".format(SMALL_SPACE, wrong_ids)

    def id_on_play_error(self, ids):
        played_ids = ', '.join(map(str, ids))
        return "\n{}Tournament(s) with id ({}) are in play.".format(SMALL_SPACE, played_ids)
