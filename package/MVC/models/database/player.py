'''
Fichier qui fait la communication entre la table 'player' de
la base de donnée et le model 'Player'.
'''

from .database import db
from ....component import exception

try:
    players = db.table('players')
except Exception as e:
    raise exception.DatabaseError(e.args[0])


def read_all():
    global players
    try:
        ids = [p.doc_id for p in players]
        _players = players.all()
        for i, player in enumerate(_players):
            player['id'] = ids[i]
        return _players
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def read(id):
    global players
    try:
        player = players.get(doc_id=id)
    except Exception as e:
        raise exception.DatabaseError(e.args[0])
    if not player:
        raise exception.PlayerNotFound("Player with id={} doesn't exist.".format(id))
    player['id'] = id
    return player


def create(player):
    global players
    try:
        players.insert(player)
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def update(id, data):
    global players
    try:
        read(id)
        players.update(data, doc_ids=[id])
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def delete(id):
    global players
    try:
        read(id)
        players.remove(doc_ids=[id])
    except Exception as e:
        raise exception.DatabaseError(e.args[0])
