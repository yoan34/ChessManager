'''
Controlleur qui permet d'afficher un tournoi en
status terminer et permet d'intéragir
avec les différentes commandes:
    -pagination
    -back

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

from ..models.tournament import ModelTournament
from ..models.player import ModelPlayer
from ..views.tournament_over import ViewTournamentOver
from ..views.tournament_play import ViewTournamentPlay
from .. views.player import ViewPlayer

from ...constante import SMALL_SPACE


class ControllerTournamentOver:

    def __init__(self):

        self.controller_name = 'tournament_over'
        self.model_tournament = ModelTournament()
        self.model_player = ModelPlayer()
        self.view_in_over = ViewTournamentOver()
        self.view_in_play = ViewTournamentPlay()
        self.view_player = ViewPlayer()
        self.error = ''
        self.page = -1
        self.page_action = ''

    # Principales méthodes pour lancer le controller et afficher les données
    # du tournois en status 'finish'.
    def run(self, path, value):
        self.target = int(path.split('/')[-2])
        self.error = ''
        self.page = self.model_tournament.read(self.target, 'n_turn') if self.page == -1 else self.page

        value = None if value is not None and not value.strip() else value

        self.page_action = value if (value == '<' or value == '>') else ''

        self.pagination() if self.page_action else None
        if value is not None and value.upper() == 'B':
            return self.back()

        self.show()

        print(self.error) if self.error and value is not None else None
        self.view_in_play.quit_back_pagination()
        return path

    def show(self):
        tournament = self.model_tournament.read(self.target)
        players = [self.model_player.read(id) for id in tournament.players]
        if self.page == len(tournament.turns):
            self.view_in_play.tournament_focus(tournament)
            self.view_in_over.result(tournament)
        else:
            self.view_in_play.tournament_focus(tournament)
            self.view_in_over.tournament_focus_over(tournament, self.page)
            self.view_player.matches_current_turn(tournament, players, self.page, True)

    # Méthodes pour gérer le retour de l'utilisateur.
    def back(self):
        return 'home/tournament'

    # Méthodes pour naviguer à travers les tours du tournoi.
    def pagination(self):
        tournament = self.model_tournament.read(self.target)
        if self.page_action == '>':
            if len(tournament.turns) + 1 > self.page + 1:
                self.page += 1
            else:
                self.error = "\n{}Maximum turn reached.".format(SMALL_SPACE)

        elif self.page_action == '<':
            if self.page > 0:
                self.page -= 1
            else:
                self.error = "\n{}Minimum turn reached.".format(SMALL_SPACE)
