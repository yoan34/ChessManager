'''
Controlleur qui permet d'afficher un tournoi en
status de jeu et permet d'intéragir
avec les différentes commandes:
    -match
    -next
    -pagination avec '<' et '>'
    -update
    -back
    -help

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

import os
import datetime

from ..models.tournament import ModelTournament
from ..models.player import ModelPlayer
from ..views.tournament_play import ViewTournamentPlay
from .. views.player import ViewPlayer
from ...component.form.tournament_play import FormTournamentPlay

from ...component.constructor.match import Match

from ...constante import SMALL_SPACE
from ...component.exception import TournamentNotFound, PlayerNotFound, DatabaseError


class ControllerTournamentPlay:

    def __init__(self):

        self.controller_name = 'tournament_play'
        self.model_tournament = ModelTournament()
        self.model_player = ModelPlayer()
        self.view_in_play = ViewTournamentPlay()
        self.view_player = ViewPlayer()
        self.error = ''
        self.target = 0
        self.on_turn = 0
        self.page = -1
        self.page_action = ''

        self.dispatcher = {
            'match': self.match,
            'next': self.next,
            'pagination': self.pagination,
            'update': self.update,
            'b': self.back,
            'h': self.help,
        }

    # Principales méthodes pour lancer le controller et afficher les données
    # du tournois en status 'play'.
    def run(self, path, value):
        self.target = int(path.split('/')[-2])
        self.on_turn = len(self.model_tournament.read(self.target, 'turns')) - 1
        self.page = self.on_turn

        value = None if value is not None and not value.strip() else value

        self.error = FormTournamentPlay.is_valid(value)

        if not self.error:
            action, *values = FormTournamentPlay._format_input(value)
            try:
                self.page_action = action if (action == '<' or action == '>') else ''
                action = ('match' if action.lower() == 'm' else
                          'pagination' if (action == '<' or action == '>') else action)

                new_path = self.dispatcher[action.lower()](values)
                if new_path:
                    return new_path
            except (TournamentNotFound, PlayerNotFound, DatabaseError) as e:
                self.error = "{}{}".format(SMALL_SPACE, e.args[0])

        self.show()

        print(self.error) if self.error and value is not None else None
        self.view_in_play.quit_back_help() if self.on_turn == 0 else self.view_in_play.quit_back_help_pagination()
        return path

    def show(self):
        tournament = self.model_tournament.read(self.target)
        players = [self.model_player.read(id) for id in tournament.players]
        self.view_in_play.tournament_focus(tournament)
        self.view_in_play.tournament_focus_play(tournament, self.page)
        self.view_player.matches_current_turn(tournament, players, self.page)

    # Méthodes des différentes commandes de l'utilisateur.
    def match(self, values):
        tournament = self.model_tournament.read(self.target)
        if tournament.turns[self.page].status == 'finish':
            self.error = "\n{}Can't change a match of turn finished.".format(SMALL_SPACE)
        else:
            # check si le match existe.
            id_match, id_win = int(values[0]), int(values[2])

            if id_match > 0 and id_match <= len(tournament.turns[self.page].matchs):
                match = tournament.turns[self.page].matchs[id_match-1]
                try:
                    previous = match.read()
                    match.write(id_win)
                    self.model_tournament.update_match(self.target, self.page, match)
                    self.model_player.update_player_in_match(match, previous)
                except PlayerNotFound as e:
                    self.error = "\n{}{}".format(SMALL_SPACE, e.args[0])
            else:
                self.error = "\n{}Match ID doesn't exist.".format(SMALL_SPACE)

    def next(self, values):
        tournament = self.model_tournament.read(self.target)
        self.error = self.check_if_turn_is_over(self.target)
        if not self.error:
            turns = self.model_tournament.read(self.target, 'turns')
            turn = turns[self.on_turn]
            date = datetime.datetime.today()
            turn.end = "{:02}/{:02}/{} at {:02}:{:02}".format(date.day, date.month, date.year, date.hour, date.minute)
            turns = [t.serialize() for t in turns]
            self.model_tournament.update(self.target, {'turns': turns})
            if tournament.n_turn == len(tournament.turns):
                players = [self.model_player.read(id) for id in tournament.players]
                return self.tournament_is_over(self.target, players)
            else:
                self.new_turn(tournament)
                self.on_turn += 1
                self.page = self.on_turn

    def pagination(self, values):
        tournament = self.model_tournament.read(self.target)
        if self.page_action == '>':
            if len(tournament.turns) > self.page + 1:
                self.page += 1
            else:
                self.error = "\n{}Maximum turn reached.".format(SMALL_SPACE)

        elif self.page_action == '<':
            if self.page > 0:
                self.page -= 1
            else:
                self.error = "\n{}Minimum turn reached.".format(SMALL_SPACE)

    def update(self, values):
        data = self._format_update_values(values)
        self.model_tournament.update(self.target, data)

    def back(self, values):
        return 'home/tournament'

    def help(self, values):
        self.view_in_play.help()
        self.view_in_play.quit_back()
        user = input("{}> ".format(SMALL_SPACE))
        quit() if user.upper() == 'Q' else None
        os.system('cls') if os.name == 'nt' else os.system('clear')

    # Méthodes d'aide pour réaliser les commandes précédentes.
    def tournament_is_over(self, id, players):
        ranking = sorted(players, key=lambda p: (p.points, p.rank), reverse=True)
        ranking = [(p.id, p.points, p.rank, p.lastname, p.firstname) for p in ranking]
        tournament = self.model_tournament.read(id)

        # Mise à jour des rang du tournois, on remet le status des joueurs à 'availabe'
        # et leur points à ''.
        self.model_tournament.update(id, {'ranking': ranking})
        [self.model_player.update(id, {'status': 'available'}) for id in tournament.players]
        [self.model_player.update(id, {'points': ''}) for id in tournament.players]

        for player in players:
            finished = player.ids_tournaments.copy()
            finished.append(id)
            self.model_player.update(player.id, {'ids_tournaments': finished})

        self.model_tournament.update(id, {'status': 'finish'})
        return 'home/tournament/' + str(self.target) + '/over'

    def check_if_turn_is_over(self, id):
        turns = self.model_tournament.read(id, 'turns')
        turn = turns[len(turns)-1]
        match_in_play = []

        for match in turn.matchs:
            if match.status == 'play':
                match_in_play.append(match.n + 1)
        if match_in_play:
            matchs = ', '.join(map(str, match_in_play))
            return '\n{}Match(es) ({}) are not finished.'.format(SMALL_SPACE, matchs)
        else:
            turn.status = 'finish'
            turns = [t.serialize() for t in turns]
            self.model_tournament.update(id, {'turns': turns})

    def new_turn(self, tournament):
        index_turn = len(tournament.turns)
        id = tournament.id

        # On ajoute un nouveau turn au tournois
        # On initialise les matchs
        self.model_tournament.add_turn(id, index_turn)

        players = [self.model_player.read(id) for id in tournament.players]

        matchs = self.matchmaking(players)
        for match in matchs:
            self.model_player.update(match['id1'], {'opponent': match['id2']})
            self.model_player.update(match['id2'], {'opponent': match['id1']})

        # On récupère les tours, on ajoute les matches au nouveau tour.
        turns = self.model_tournament.read(id, 'turns')
        turn = turns[index_turn]
        turn.matchs = matchs
        turns = [t.serialize() for t in turns]
        # On update la liste des tours après avoir ajouter les matches au tour.
        self.model_tournament.update(id, {'turns': turns})

    def matchmaking(self, players):
        players = sorted(players, key=lambda player: (player.points, player.rank))
        paires = list(map(list, zip(players[::2], players[1::2])))
        flag = True
        while flag:
            for n, paire in enumerate(paires):
                if paire[0].opponent == paire[1].id:
                    a = paires[n][1]
                    if n == len(paires)-1:
                        paires[n][1] = paires[n-1][0]
                        paires[n-1][0] = a
                    else:
                        paires[n][1] = paires[n+1][0]
                        paires[n+1][0] = a
                    break
            else:
                flag = False
        paires = [(p1.id, p2.id) for p1, p2 in paires]
        return [Match(*paire, n).serialize() for n, paire in enumerate(paires)]

    def _format_update_values(self, values):
        attr, value = [v.strip() for v in values[0].split('=', 1)]
        if value:
            value = ' '.join([value.strip()] + [v.strip() for v in values[1:]])
        else:
            value = ' '.join([v.strip() for v in values[1:]])
        if attr == 'n_turn':
            value = int(value)
        return {attr: value}
