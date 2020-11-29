'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerTournamentNew'.
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormTournamentNew(Form):

    name = 'tournament_new'

    @classmethod
    def is_valid(cls, value, question):
        try:
            cls._raise_error_if_value_user_wrong(question, value)
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])
