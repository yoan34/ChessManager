'''
Controlleur qui permet d'afficher/créer un rapport
à l'aide de différentes commandes:
    -players
    -tournaments
    -turns
    -matches
    -back
    -help

On peut demander à créer un rapport sur fichier en ajoutant
en paramètre de fin 'file'.

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

import os
import copy

from ..models.tournament import ModelTournament
from ..models.player import ModelPlayer
from ..views.report import ViewReport
from ..views.player import ViewPlayer
from ..views.tournament import ViewTournament
from ...component.form.report import FormReport

from ...component.file_manager import FileManager
from ...constante import SMALL_SPACE, MEDIUM_SPACE, LARGE_SPACE, MEDIUM_DASH_TITLE
from ...component.exception import TournamentNotFound, PlayerNotFound, DatabaseError, FileError


class ControllerReport:

    def __init__(self):

        self.controller_name = 'report'
        self.model_tournament = ModelTournament()
        self.model_player = ModelPlayer()
        self.view_report = ViewReport()
        self.view_player = ViewPlayer()
        self.view_tournament = ViewTournament()
        self.file_manager = False
        self.error = ''

        self.dispatcher = {
            'players': self.players,
            'tournaments': self.tournaments,
            'turns': self.turns,
            'matches': self.matches,
            'b': self.back,
            'h': self.help,
        }

    # Principales méthodes pour lancer le controller et afficher le rapport.
    def run(self, path, value):
        value = None if value is not None and not value.strip() else value
        if not self.file_manager:
            FileManager.make_folder()
            self.file_manager = True

        self.error = FormReport.is_valid(value)

        if not self.error:
            action, *values = FormReport._format_input(value)
            try:
                new_path = self.dispatcher[action.lower()](values)
                if new_path:
                    return new_path
            except (TournamentNotFound, PlayerNotFound, DatabaseError, FileError) as e:
                self.error = "{}{}".format(SMALL_SPACE, e.args[0])

        self.show() if (value is None or self.error or value.lower() == 'h') else None

        print(self.error) if self.error and value is not None else None
        (self.view_report.quit_back_help() if (value is None or self.error or value.lower() == 'h')
            else self.view_report.quit_back())
        return path

    def show(self):
        self.view_report.title()
        self.view_report.report()

    # Méthodes des différentes commandes de l'utilisateur.
    def players(self, values):
        all_ = False
        try:
            int(values[0])
        except ValueError:
            all_ = True
            sort_by = [values[0]]
            if len(values) > 1:
                sort_by += [values[1]]
            players = self.model_player.read_all(sort_by)
            subtitle = '{}{} List of all players {}\n'.format(
                LARGE_SPACE, MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE
                ).center(50)
            if not players:
                self.error = "{}No player in the database.".format(SMALL_SPACE)
        else:
            players = self.model_tournament.read(int(values[0]), 'players')
            players = [self.model_player.read(id) for id in players]
            subtitle = '{}{} Player of tournament {} {}\n'.format(
                LARGE_SPACE, MEDIUM_DASH_TITLE, int(values[0]), MEDIUM_DASH_TITLE
                ).center(50)
            if not players:
                self.error = "{}No player in tournament id={}".format(SMALL_SPACE, values[0])

        if not self.error:
            print(subtitle)
            if not all_:
                ranking = self.model_tournament.read(int(values[0]), 'ranking')
                if ranking:
                    players_copied = copy.deepcopy(players)
                    for player_copy in players_copied:
                        rank = list(filter(lambda x: x[0] == player_copy.id, ranking))[0]
                        player_copy.points = rank[1]

                    players = sorted(players_copied, key=lambda x: (x.points, x.rank), reverse=True)
            self.view_player.read_all(players)

            if values[-1].lower() == 'file':
                file, origin_stdout = FileManager.create(['players', *values[:-1]])
                print(subtitle)
                self.view_player.read_all(players)
                FileManager.close(file, origin_stdout)
                print("{}The file has been created successfully.".format(SMALL_SPACE))

    def tournaments(self, values):
        sort_by = [values[0]]
        if len(values) > 1:
            sort_by += [values[1]]
        tournaments = self.model_tournament.read_all(sort_by)
        subtitle = '{}{} List of all tournaments {}\n'.format(
            LARGE_SPACE, MEDIUM_DASH_TITLE, MEDIUM_DASH_TITLE
            ).center(50)
        if not tournaments:
            self.error = "{}No tournament in the database.".format(SMALL_SPACE)

        if not self.error:
            print(subtitle)
            self.view_tournament.read_all(tournaments)

            if values[-1].lower() == 'file':
                file, origin_stdout = FileManager.create(['tournaments', *values[:-1]])
                print(subtitle)
                self.view_tournament.read_all(tournaments)
                FileManager.close(file, origin_stdout)
                print("{}The file has been created successfully.".format(SMALL_SPACE))

    def turns(self, values):
        id = int(values[0])
        turns = self.model_tournament.read(id, 'turns')
        status = self.model_tournament.read(id, 'status')
        if status == 'register':
            raise TournamentNotFound("Can't report turn on a tournament that doesn't have started.")
        subtitle = "{}{}List of turns - tournament {}: {} {}\n\n".format(
            MEDIUM_SPACE, MEDIUM_DASH_TITLE, id, status, MEDIUM_DASH_TITLE
            ).center(50)

        print(subtitle)
        for turn in turns:
            self.view_report.turn(turn)

        if values[-1].lower() == 'file':
            file, origin_stdout = FileManager.create(['turns', *values[:-1]])
            print(subtitle)
            for turn in turns:
                self.view_report.turn(turn)
            FileManager.close(file, origin_stdout)
            print("{}The file has been created successfully.".format(SMALL_SPACE))

    def matches(self, values):
        id = int(values[0])
        tournament = self.model_tournament.read(id)

        if tournament.status == 'register':
            raise TournamentNotFound("Can't report turn on a tournament that doesn't have started.")
        subtitle = "{}{}List of matches - tournament {}: {} {}\n\n".format(
            MEDIUM_SPACE, MEDIUM_DASH_TITLE, id, tournament.status, MEDIUM_DASH_TITLE
            ).center(50)

        self._show_turn(subtitle, tournament)

        if values[-1].lower() == 'file':
            file, origin_stdout = FileManager.create(['matches', *values[:-1]])
            self._show_turn(subtitle, tournament)
            FileManager.close(file, origin_stdout)
            print("{}The file has been created successfully.".format(SMALL_SPACE))

    def back(self, values):
        return 'home'

    def help(self, values):
        self.view_report.help()
        self.view_report.quit_back()
        user = input("{}> ".format(SMALL_SPACE))
        quit() if user.upper() == 'Q' else None
        os.system('cls') if os.name == 'nt' else os.system('clear')

    # Méthodes d'aide pour réaliser le rapport de la section 'matches'.
    def _show_turn(self, subtitle, tournament):
        turns = tournament.turns
        players = tournament.players
        players = [self.model_player.read(id) for id in players]
        print(subtitle)
        for i, turn in enumerate(turns):
            title = " {} - {} start at:  {}".format(turn.status, turn.name, turn.start).center(80, '-')
            print("{}{}\n".format(SMALL_SPACE, title))
            self.view_player.matches_current_turn(tournament, players, i, True, True)
            end = " end at: {} ".format(turn.end).center(80, '-')
            print("{}{}\n\n\n\n".format(SMALL_SPACE, end))
