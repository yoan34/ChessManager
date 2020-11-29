'''
Fichier qui fait la communication entre la table 'tournament' de
la base de donnée et le model 'Tournament'.
'''

from .database import db
from ....component import exception

try:
    tournaments = db.table('tournaments')
except Exception as e:
    raise exception.DatabaseError(e.args[0])


def read_all():
    global tournaments
    try:
        ids = [t.doc_id for t in tournaments]
        _tournaments = tournaments.all()
        for i, tournament in enumerate(_tournaments):
            tournament['id'] = ids[i]
        return _tournaments
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def read(id):
    global tournaments
    try:
        tournament = tournaments.get(doc_id=id)
    except Exception as e:
        raise exception.DatabaseError(e.args[0])
    if not tournament:
        raise exception.TournamentNotFound("Tournament with id={} doesn't exist.".format(id))
    tournament['id'] = id
    return tournament


def create(tournament):
    global tournaments
    try:
        tournaments.insert(tournament)
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def update(id, data):
    global tournaments
    try:
        read(id)
        tournaments.update(data, doc_ids=[id])
    except Exception as e:
        raise exception.DatabaseError(e.args[0])


def delete(id):
    global tournaments
    try:
        read(id)
        tournaments.remove(doc_ids=[id])
    except Exception as e:
        raise exception.DatabaseError(e.args[0])
