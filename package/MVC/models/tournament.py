'''
Classe qui représente le model d'un tournoi pour
communiquer avec la base de donnée.
On peut créer, changer, supprimer des tournois.
'''

from .model import Model
from ...component.constructor.tournament import Tournament
from ...component.constructor.turn import Turn
from .database import tournament as db_tournament


class ModelTournament(Model):

    def read_all(self, sort_by):
        tournaments = [Tournament.deserialize(tournament) for tournament in db_tournament.read_all()]
        reverse = True if len(sort_by) == 2 else False
        y = ('n_turn' if sort_by[0] == 'max_turn' else
             'players' if sort_by[0] == 'ids_player' else sort_by[0])

        if sort_by[0] in ('description', 'ids_player'):
            def key(x): len(getattr(x, y))
        else:
            def key(x): getattr(x, y)

        self._format_birth_to_datetime(tournaments, 'date') if sort_by[0] == 'date' else None
        tournaments = sorted(tournaments, key=key, reverse=reverse)
        self._format_datetime_to_birth(tournaments, 'date') if sort_by[0] == 'date' else None

        return tournaments

    def read(self, id, attr=False):
        tournament = Tournament.deserialize(db_tournament.read(id))
        return getattr(tournament, attr) if attr else tournament

    def create(self, values):
        for name in ('name', 'place', 'country', 'time'):
            values[name] = values[name].strip()
            values[name] = values[name].capitalize()
        values['n_player'] = int(values['n_player'])
        values['n_turn'] = int(values['n_turn'])
        tournament = Tournament(**values)
        db_tournament.create(tournament.serialize())

    def update(self, id, data):
        for attr in data:
            if attr in ('name', 'place', 'country', 'time'):
                data[attr] = data[attr].capitalize()
            elif attr == 'n_turn':
                data[attr] = int(data[attr])
            else:
                data[attr] = data[attr]
        db_tournament.update(id, data)

    def update_match(self, id, index, match):
        turns = self.read(id, 'turns')
        matchs = turns[index].matchs
        matchs[match.n] = match

        turns[index].matchs = matchs
        turns = [t.serialize() for t in turns]
        self.update(id, {'turns': turns})

    def delete(self, ids):
        db_tournament.delete(ids)

    def number_of_place(self, id):
        tournament = self.read(id)
        return tournament.n_player - len(tournament.players)

    def check_ids(self, ids):
        ids_finish, ids_played, ids_registred, ids_wrong = [], [], [], []
        for id in ids:
            try:
                status = self.read(id, 'status')

                if status == 'finish':
                    ids_finish.append(id)
                elif status[:1].lower() == 'r':
                    ids_registred.append(id)
                elif status[:1].lower() == 'p':
                    ids_played.append(id)

            except Exception:
                ids_wrong.append(id)
        return ids_finish, ids_played, ids_registred, ids_wrong

    def check_ids_registered(self, id, ids_player):
        ids_in, ids_out = [], []
        for id_player in ids_player:
            if id_player in self.read(id).players:
                ids_in.append(id_player)
            else:
                ids_out.append(id_player)
        return ids_in, ids_out

    def add_turn(self, id, n):
        # On créer un nouveau turn serializé {}
        turn = Turn(n).serialize()
        # On récupère les turns du tournois
        turns = self.read(id, 'turns')
        turns = [t.serialize() for t in turns]
        turns.append(turn)
        self.update(id, {'turns': turns})
