'''
Classe qui représente le model d'un joueur pour
communiquer avec la base de donnée.
On peut créer, changer, supprimer des joueurs.
'''

from .model import Model
from ...component.constructor.player import Player
from .database import player as db_player


class ModelPlayer(Model):

    def read_all(self, sort_by):
        players = [Player.deserialize(player) for player in db_player.read_all()]

        reverse = True if len(sort_by) == 2 else False
        self._format_birth_to_datetime(players, 'birth') if sort_by[0] == 'birth' else None
        self._format_points_to_number(players) if sort_by[0] == 'points' else None
        if sort_by[0] == 'finished':
            players = sorted(players, key=lambda x: len(x.ids_tournaments), reverse=reverse)
        else:
            players = sorted(players, key=lambda x: getattr(x, sort_by[0]), reverse=reverse)

        self._format_datetime_to_birth(players, 'birth') if sort_by[0] == 'birth' else None
        self._format_points_to_str(players) if sort_by[0] == 'points' else None

        return players

    def read(self, id, attr=False):
        player = Player.deserialize(db_player.read(id))
        return getattr(player, attr) if attr else player

    def create(self, values):
        last_name, first_name, sex, birth, rank = values
        last_name, first_name = last_name.capitalize(), first_name.capitalize()
        sex, rank = sex.upper(), int(rank)
        birth = self._format_birth(birth, '-' if '-' in birth else ':' if ':' in birth else '/')
        player = Player(last_name, first_name, sex, birth, rank)
        db_player.create(player.serialize())

    def update(self, id, data):
        for attr in data:
            if attr in ('lastname', 'firstname', 'sex'):
                data[attr] = data[attr].capitalize()
            elif attr == 'birth':
                sep = '-' if '-' in data[attr] else ':' if ':' in data[attr] else '/'
                data[attr] = self._format_birth(data[attr], sep)
            elif attr == 'rank':
                data[attr] = int(data[attr])

            elif attr == 'points':
                data[attr] = float(data[attr]) if data[attr] else data[attr]
        db_player.update(id, data)

    def update_player_in_match(self, match, previous):
        id_p1, id_p2 = match.id1, match.id2
        p1 = self.read(id_p1)
        p2 = self.read(id_p2)

        # Si dans le match précédent, il n'y a pas de score
        if previous[0][1] is None:
            self.update(match.id1, {'points': p1.points + match.score_id1})
            self.update(match.id2, {'points': p2.points + match.score_id2})
        else:
            self.update(match.id1, {'points': p1.points + match.score_id1 - previous[0][1]})
            self.update(match.id2, {'points': p2.points + match.score_id2 - previous[1][1]})

    def delete(self, ids):
        db_player.delete(ids)

    def check_ids(self, ids):
        ids_available, ids_played, ids_registred, ids_wrong = [], [], [], []
        for id in ids:
            try:
                status = self.read(id, 'status')

                if status == 'available':
                    ids_available.append(id)
                elif status[:1].lower() == 'r':
                    ids_registred.append(id)
                elif status[:1].lower() == 'p':
                    ids_played.append(id)

            except Exception:
                ids_wrong.append(id)
        return ids_available, ids_played, ids_registred, ids_wrong
