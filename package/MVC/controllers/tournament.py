'''
Controlleur qui permet d'afficher les tournois et
d'intéragir avec les différentes commandes:
    -delete
    -sort
    -focus
    -back
    -help

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

import os

from ..models.tournament import ModelTournament
from ..models.player import ModelPlayer
from ..views.tournament import ViewTournament
from ...component.form.tournament import FormTournament

from ...constante import SMALL_SPACE
from ...component.exception import TournamentNotFound, PlayerNotFound, DatabaseError


class ControllerTournament:

    def __init__(self):
        self.controller_name = 'tournament'
        self.model_tournament = ModelTournament()
        self.model_player = ModelPlayer()
        self.view = ViewTournament()
        self.error = ''
        self.sort_by = ['id']

        self.dispatcher = {
            'sort': self.sort,
            'focus': self.focus,
            'delete': self.delete,
            'b': self.back,
            'h': self.help,
        }

    # Principales méthodes pour lancer le controller et afficher les données des tournois.
    def run(self, path, value):

        value = None if value is not None and not value.strip() else value

        self.error = FormTournament.is_valid(value)

        if not self.error:
            action, *values = FormTournament._format_input(value)
            try:
                back = self.dispatcher[action.lower()](values)
                if back:
                    return back
            except (TournamentNotFound, PlayerNotFound, DatabaseError) as e:
                self.error = "{}{}".format(SMALL_SPACE, e.args[0])

        self.show()

        print(self.error) if self.error and value is not None else None
        self.view.quit_back_help()
        return path

    def show(self):
        self.view.title()
        tournaments = self.model_tournament.read_all(self.sort_by)
        self.view.read_all(tournaments)

    # Méthodes des différentes commandes de l'utilisateur.
    def delete(self, values):
        ids = list(set(map(int, values)))
        # On check le status des tournois et retourne des listes d'IDs en fonction du status.
        ids_finish, ids_played, ids_registred, ids_wrong = self.model_tournament.check_ids(ids)

        # On supprime les dépendance lié à la suppression du tournois.
        self._delete_dependency_tournament(ids_finish, ids_registred)

        # On supprime le(s) tournoi(s).
        [self.model_tournament.delete(id) for id in ids_finish + ids_registred]
        self.error = self.view.ids_error(ids_wrong, ids_played, ids_finish + ids_registred)

    def sort(self, values):
        self.sort_by = values

    def focus(self, values):
        status = self.model_tournament.read(int(values[0]), 'status')
        self.sort_by = ['id']
        status = 'over' if status == 'finish' else status
        return 'home/tournament/' + values[0] + '/' + status

    def back(self, values):
        self.sort_by = ['id']
        return 'home'

    def help(self, values):
        self.view.help()
        self.view.quit_back()
        user = input("{}> ".format(SMALL_SPACE))
        quit() if user.upper() == 'Q' else None
        os.system('cls') if os.name == 'nt' else os.system('clear')

    # Gère les dépendance lors d'une suppression avec la commande 'delete'.
    def _delete_dependency_tournament(self, ids_finish, ids_registred):
        self._delete_dependency_of_finished_tournament(ids_finish)
        self._delete_dependency_of_registered_tournament(ids_registred)

    def _delete_dependency_of_finished_tournament(self, ids):
        for id in ids:
            players = self.model_tournament.read(id, 'players')
            for id_player in players:
                player = self.model_player.read(id_player)
                player.ids_tournaments.remove(id)
                self.model_player.update(id_player, {'ids_tournaments': player.ids_tournaments})

    def _delete_dependency_of_registered_tournament(self, ids):
        for id in ids:
            players = self.model_tournament.read(id, 'players')
            for id_player in players:
                self.model_player.update(id_player, {'status': 'available'})
