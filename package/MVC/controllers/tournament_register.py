'''
Controlleur qui permet d'afficher un tournoi en
status d'enregistrement et permet d'intéragir
avec les différentes commandes:
    -start
    -add
    -remove
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
from ..views.tournament_register import ViewTournamentRegister
from .. views.player import ViewPlayer
from ...component.form.tournament_register import FormTournamentRegister

from ...component.constructor.match import Match

from ...constante import SMALL_SPACE
from ...component.exception import TournamentNotFound, PlayerNotFound, DatabaseError


class ControllerTournamentRegister:

    def __init__(self):
        self.controller_name = 'tournament_register'
        self.model_tournament = ModelTournament()
        self.model_player = ModelPlayer()
        self.view_in_register = ViewTournamentRegister()
        self.view_player = ViewPlayer()
        self.error = ''
        self.target = 0

        self.dispatcher = {
            'start': self.start,
            'add': self.add,
            'remove': self.remove,
            'update': self.update,
            'b': self.back,
            'h': self.help,
        }

    # Principales méthodes pour lancer le controller et afficher les données
    # du tournois en status 'register'.
    def run(self, path, value):
        self.target = int(path.split('/')[-2])
        value = None if value is not None and not value.strip() else value

        self.error = FormTournamentRegister.is_valid(value)

        if not self.error:
            action, *values = FormTournamentRegister._format_input(value)
            try:
                new_path = self.dispatcher[action.lower()](values)
                if new_path:
                    return new_path
            except (TournamentNotFound, PlayerNotFound, DatabaseError) as e:
                self.error = "{}{}".format(SMALL_SPACE, e.args[0])

        self.show()

        print(self.error) if self.error and value is not None else None
        self.view_in_register.quit_back_help()
        return path

    def show(self):
        tournament = self.model_tournament.read(self.target)
        self.view_in_register.tournament_focus(tournament)
        self.view_in_register.tournament_focus_register(tournament)
        len_id = len(str(max([p for p in tournament.players]))) if tournament.players else 1
        for id in tournament.players:
            player = self.model_player.read(id)
            self.view_player.in_register_mode(player, len_id)

    # Méthodes des différentes commandes de l'utilisateur.
    def start(self, values):
        place = self.model_tournament.number_of_place(self.target)
        if place:
            self.error = "{}{} more player(s) must be registered to start".format(SMALL_SPACE, place)
        else:
            self.model_tournament.update(self.target, {'status': 'play'})
            for id_player in self.model_tournament.read(self.target).players:
                self.model_player.update(id_player, {'points': float(0), 'status': 'play on {}'.format(self.target)})
            # Création du premier Tour.
            self.start_tournament(self.target)
            return 'home/tournament/' + str(self.target) + '/play'

    def add(self, values):
        ids = list(set(map(int, values)))
        place = self.model_tournament.number_of_place(self.target)
        ids_available, ids_played, ids_registred, ids_wrong = self.model_player.check_ids(ids)

        [self.model_player.update(id, {'status': 'registered on {}'.format(self.target)})
            for id in ids_available[:place]]
        players_registered = self.model_tournament.read(self.target, 'players')
        self.model_tournament.update(self.target, {'players': players_registered + ids_available[:place]})

        self.error = self.view_in_register.ids_error(
            ids_wrong, ids_registred, ids_played, ids_available[:place], 'added')
        self.error += self.view_in_register.ids_not_place_error(ids_available, place)

    def remove(self, values):
        ids = list(set(map(int, values)))
        ids_in, ids_out = self.model_tournament.check_ids_registered(self.target, ids)
        [self.model_player.update(id, {'status': 'available'}) for id in ids_in]

        players_registered = self.model_tournament.read(self.target).players
        [players_registered.remove(id) for id in ids_in]
        self.model_tournament.update(self.target, {'players': players_registered})

        self.error = self.view_in_register.remove_player_registered_error(ids_in, ids_out)

    def update(self, values):
        data = self._format_update_values(values)
        self.model_tournament.update(self.target, data)

    def back(self, values):
        return 'home/tournament'

    def help(self, values):
        self.view_in_register.help()
        self.view_in_register.quit_back()
        user = input("{}> ".format(SMALL_SPACE))
        quit() if user.upper() == 'Q' else None
        os.system('cls') if os.name == 'nt' else os.system('clear')

    # Méthodes d'aide pour réaliser les commandes précédentes.
    def start_tournament(self, id):
        tournament = self.model_tournament.read(id)
        index_turn = len(tournament.turns)

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
        # Du plus petit au plus grand
        players = sorted(players, key=lambda player: player.rank)
        low = [p.id for p in players[:len(players)//2]]
        hight = [p.id for p in players[len(players)//2:]]
        paires = list(zip(low, hight))
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
