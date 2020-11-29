# Si le forme de l'input utilisateur est éronné.
class UserInputError(Exception):
    pass


# Si l'ID du joueur n'est pas dans le base de donnée.
class PlayerNotFound(Exception):
    pass


# Si l'ID du tournoi n'est pas dans le base de donnée.
class TournamentNotFound(Exception):
    pass


# Si la connexion avec la base de donnée n'est pas correct.
class DatabaseError(Exception):
    pass


# Si un problème à eu lieu avec un fichier lié à un rapport.
class FileError(Exception):
    pass
