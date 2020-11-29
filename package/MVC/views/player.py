'''
Classe qui représente la view du controlleur
'ControllerPlayer'.
'''

from .view import View

from ...constante import (
    SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, SMALL_DASH_TITLE, MEDIUM_DASH_TITLE,
    MAX_CHAR_NAME_NO_GRID, MAX_CHAR_IDS_TOURNAMENTS
    )


class ViewPlayer(View):

    HEADERS = ('id', 'lastname', 'firstname', 'sex', 'birth', 'rank', 'tournament finished', 'status', 'points')

    def read_all(self, players):
        data = [ViewPlayer.HEADERS]
        for p in players:
            t_finished = ', '.join(map(str, p.ids_tournaments))
            t_finished = (t_finished if len(t_finished) <= MAX_CHAR_IDS_TOURNAMENTS
                          else t_finished[:MAX_CHAR_IDS_TOURNAMENTS - 3] + '...')
            row = (str(p.id), p.lastname, p.firstname, p.sex, p.birth, str(p.rank), t_finished,
                   p.status, str(p.points))
            data.append(row)
        self.grid(data)

    def title(self):
        print("{} List of players {}\n".format(MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE).center(100))

    def help(self):
        print("{} helper {}\n".format(SMALL_DASH_TITLE, SMALL_DASH_TITLE).center(65))
        r = ''
        l1 = "\n{}All commands possible (* -> optional):\n\n".format(SMALL_SPACE)

        l2 = "{}sort <name> reverse*\n".format(MEDIUM_SPACE)
        l3 = "{}exemple: sort rank OR sort lastname reverse\n".format(LARGE_SPACE)
        l4 = "{}note: <name> can be equal to 'id, firstname, lastname, sex,\n".format(LARGE_SPACE)
        l5 = "{}birth, rank, points, status and finished'\n\n\n".format(LARGE_SPACE)

        l6 = "{}update id <name1>=value1 <name2>=value2\n".format(MEDIUM_SPACE)
        l7 = "{}exemple: update 12 lastname=albert rank=756\n".format(LARGE_SPACE)
        l8 = "{}note: you can change lastname, firstname, sex,\n".format(LARGE_SPACE)
        l9 = "{}birth, rank, and status=available\n\n\n".format(LARGE_SPACE)

        l10 = "{}delete id1 id2 id3 id4...\n".format(MEDIUM_SPACE)
        l11 = "{}exemple: delete 45, 12, 1, 3\n".format(LARGE_SPACE)
        l12 = "{}note: can't delete a player with 'status=on play'\n\n\n".format(LARGE_SPACE)

        l13 = "{}create lastname, firstname, sex, birth, rank\n".format(MEDIUM_SPACE)
        l14 = "{}exemple: joe, marius, m, 17/12/1992, 1453\n".format(LARGE_SPACE)
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10 + l11 + l12 + l13 + l14
        print(r)

    def in_register_mode(self, player, len_id):
        name = '{} {}'.format(player.lastname, player.firstname)
        if len(name) > MAX_CHAR_NAME_NO_GRID + 4:
            name = name[:MAX_CHAR_NAME_NO_GRID] + '... '
        name = name.ljust(MAX_CHAR_NAME_NO_GRID + 4)
        rank = ' ' * (4 - len(str(player.rank))) + str(player.rank)
        point = player.points if player.points else '0'
        point = ' ' * (3 - len(str(player.points))) + str(player.points)
        _id = ' ' * (len_id - len(str(player.id))) + str(player.id)
        print('{}| ({})  {}-->   sex: {}   birth: {}   rank: {}   points: {} |'.format(
            SMALL_SPACE, _id, name, player.sex, player.birth, rank, point))

    def matches_current_turn(self, tournament, players, index, end=False, report=False):
        len_id = len(str(max([p.id for p in players])))
        for n, match in enumerate(tournament.turns[index].matchs):
            current = False if end else (len(tournament.turns) == index + 1)
            self.show_match(match, players, current, len_id)
            print('{}|{}|'.format(MEDIUM_SPACE, ' '*(66 + len_id - 1))) if not report else None
        print(MEDIUM_SPACE + '+' + (66 + len_id - 1)*'-' + '+') if not report else print()

    def show_match(self, match, players, current, len_id):
        r = ''
        p1 = list(filter(lambda p: int(p.id) == match.id1, players))
        p1 = p1[0] if p1 else ' Player has been deleted...'
        p2 = list(filter(lambda p: int(p.id) == match.id2, players))
        p2 = p2[0] if p2 else ' Player has been deleted...'

        len_ljust = 64 + len_id - 1
        if match.status[0] == 'w':
            id_win = match.id1 if match.score_id1 > match.score_id2 else match.id2
            if isinstance(p1, str):
                if isinstance(p2, str):
                    status = "{}: {} {}".format(match.name, match.status.upper(), p1).ljust(len_ljust)
                else:
                    if id_win == p2.id:
                        status = ("{}: {} {} {}".format(
                            match.name, match.status.upper(), p2.lastname, p2.firstname
                            ).ljust(len_ljust))
                    else:
                        status = "{}: {} {}".format(match.name, match.status.upper(), p1).ljust(len_ljust)
            else:
                if isinstance(p2, str):
                    if id_win == p1.id:
                        status = "{}: {} {} {}".format(
                            match.name, match.status.upper(), p1.lastname, p1.firstname
                            ).ljust(len_ljust)
                    else:
                        status = "{}: {} {}".format(match.name, match.status.upper(), p2).ljust(len_ljust)
                else:
                    p_win = p1 if p1.id == id_win else p2
                    status = "{}: {} {} {}".format(
                        match.name, match.status.upper(), p_win.lastname, p_win.firstname
                        ).ljust(len_ljust)

        else:
            status = "{}: {}".format(match.name, match.status.upper()).ljust(len_ljust)

        l1 = "{}| {} |\n".format(MEDIUM_SPACE, status)

        if isinstance(p1, str):
            l2 = "{}|{}  |\n".format(MEDIUM_SPACE, p1.ljust(len_ljust))
        else:
            l2 = (self.player_in_match_total_pts(p1, match, len_id) if current else
                  self.player_in_match(p1, match, len_id))
        if isinstance(p2, str):
            l3 = "{}|{}  |\n".format(MEDIUM_SPACE, p2.ljust(len_ljust))
        else:
            l3 = (self.player_in_match_total_pts(p2, match, len_id) if current else
                  self.player_in_match(p2, match, len_id))
        r += l1 + l2 + l3
        print(r, end='')

    def player_in_match_total_pts(self, player, match, len_id):
        name = '{} {}'.format(player.lastname, player.firstname)
        if len(name) > MAX_CHAR_NAME_NO_GRID:
            name = name[:MAX_CHAR_NAME_NO_GRID - 4] + '... '
        name = name.ljust(MAX_CHAR_NAME_NO_GRID)
        rank = ' ' * (4 - len(str(player.rank))) + str(player.rank)
        point = player.points
        point = ' ' * (3 - len(str(player.points))) + str(player.points)
        _id = ' ' * (len_id - len(str(player.id))) + str(player.id)
        color = match.color_id1 if player.id == match.id1 else match.color_id2
        return '{}| ({})  {} ({}) -->  sex: {}   rank: {}   points: {} |\n'.format(
            MEDIUM_SPACE, _id, name, color, player.sex,  rank, point)

    def player_in_match(self, player, match, len_id):
        name = '{} {}'.format(player.lastname, player.firstname)
        if len(name) > MAX_CHAR_NAME_NO_GRID:
            name = name[:MAX_CHAR_NAME_NO_GRID - 4] + '... '
        name = name.ljust(MAX_CHAR_NAME_NO_GRID)
        rank = ' ' * (4 - len(str(player.rank))) + str(player.rank)
        point = match.score_id1 if player.id == match.id1 else match.score_id2
        color = match.color_id1 if player.id == match.id1 else match.color_id2
        point = ' ' * (3 - len(str(point))) + str(point)
        _id = ' ' * (len_id - len(str(player.id))) + str(player.id)
        return '{}| ({})  {} ({}) -->  sex: {}   rank: {}   points: {} |\n'.format(
            MEDIUM_SPACE, _id, name, color, player.sex,  rank, point)
