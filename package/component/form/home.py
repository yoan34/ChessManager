'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerHome'.
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormHome(Form):

    name = 'home'
    INPUT = (1, 2, 3, 4)

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")
            if len(value) > 1:
                raise UserInputError("Too many arguments.")
            try:
                int(value[0])
            except ValueError:
                raise UserInputError("Argument must be a number.")

            if int(value[0]) not in FormHome.INPUT:
                raise UserInputError("Argument not available.")
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])
