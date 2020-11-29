'''
Fichier qui créer/récupère la base de donnée
qui servira à stocker les tournois et joueurs.
'''

import os
from tinydb import TinyDB
from ....component.exception import DatabaseError

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    db = TinyDB(__location__ + '/db.json')
except Exception as e:
    raise DatabaseError(e.args[0])
