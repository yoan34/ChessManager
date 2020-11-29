'''
Controlleur qui permet d'afficher les joueurs et
d'intéragir avec les différentes commandes:
    -delete
    -sort
    -create
    -update
    -back
    -help

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

import os

from ..models.player import ModelPlayer
from ..models.tournament import ModelTournament
from ..views.player import ViewPlayer
from ...component.form.player import FormPlayer

from ...constante import SMALL_SPACE
from ...component.exception import TournamentNotFound, PlayerNotFound, DatabaseError


class ControllerPlayer:

    def __init__(self):
        self.controller_name = 'player'
        self.model_player = ModelPlayer()
        self.model_tournament = ModelTournament()
        self.view = ViewPlayer()
        self.error = ''
        self.sort_by = ['id']

        self.dispatcher = {
            'sort': self.sort,
            'update': self.update,
            'create': self.create,
            'delete': self.delete,
            'b': self.back,
            'h': self.help,
        }

    # Principales méthodes pour lancer le controller et afficher les données des joueurs.
    def run(self, path, value):

        value = None if value is not None and not value.strip() else value

        self.error = FormPlayer.is_valid(value)

        if not self.error:
            action, *values = FormPlayer._format_input(value)
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
        players = self.model_player.read_all(self.sort_by)
        self.view.read_all(players)

    # Méthodes des différentes commandes de l'utilisateur.
    def sort(self, values):
        self.sort_by = values

    def update(self, values):
        id, values = int(values[0]), values[1:]
        data = self._format_update_values(values)

        # Si le joueur est en tournoi, on peut pas le changer
        if self.model_player.read(id).status[0] == 'p':
            self.error = "{}Player in game can't be update.".format(SMALL_SPACE)
        else:
            # Si le status est changé et que le status est registered, on doit
            # mettre à jour le tournoi ou le joueur est inscrit pour l'enlever.
            if 'status' in data and self.model_player.read(id, 'status')[0] == 'r':
                id_tournament = int(self.model_player.read(id, 'status')[14:])
                players_registered = self.model_tournament.read(id_tournament, 'players')
                players_registered.remove(id)
                self.model_tournament.update(id_tournament, {'players': players_registered})
            self.model_player.update(id, data)

    def create(self, values):
        self.model_player.create(values)

    def delete(self, values):
        ids = list(set(map(int, values)))
        ids_available, ids_played, ids_registred, ids_wrong = self.model_player.check_ids(ids)
        self._delete_dependency_player(ids_registred, ids_available)
        [self.model_player.delete(id) for id in ids_available + ids_registred]
        self.error = self.view.ids_error(ids_wrong, [], ids_played, ids_available + ids_registred)

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
    def _delete_dependency_player(self, ids_registred, ids_available):
        for id in ids_registred:
            id_tournament = int(self.model_player.read(id, 'status')[14:])
            players_registered = self.model_tournament.read(id_tournament, 'players')
            players_registered.remove(id)
            self.model_tournament.update(id_tournament, {'players': players_registered})

        for id in ids_available:
            finished = self.model_player.read(id).ids_tournaments
            for id_finish in finished:
                tournament = self.model_tournament.read(id_finish)
                players_in_tournament = tournament.players
                players_in_tournament.remove(id)
                self.model_tournament.update(id_finish, {'players': players_in_tournament})

    # Méthodes d'aide pour formater des données en dictionnaire.
    def _format_update_values(self, values):
        data = {}
        for arg in values:
            attr, value = arg.split('=')
            data[attr] = value if attr != 'rank' else int(value)
        return data
