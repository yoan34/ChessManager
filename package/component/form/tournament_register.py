'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerTournamentRegister'.
Chaque méthode est associé à une commande utilisateur:
    -add
    -remove
    -start
    -update
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormTournamentRegister(Form):

    name = 'tournament_register'

    INPUT_TOURNAMENT_REGISTER = ('add', 'remove', 'start', 'update')
    INPUT_TOURNAMENT_REGISTER_UPDATE = ('name', 'place', 'country', 'n_turn', 'time', 'description')

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")

            if value[0].lower() in FormTournamentRegister.INPUT_TOURNAMENT_REGISTER:
                cls.__dict__[value[0].lower()].__get__(None, cls)(value[1:])
            else:
                if len(value) == 1 and (value[0].upper() == 'B' or value[0].upper() == 'H'):
                    return ''
                raise UserInputError("First argument doesn't exist.")
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])

    @classmethod
    def add(cls, values):
        if not values:
            raise UserInputError("at least one ID is required.")
        if len(values) > 100:
            raise UserInputError("Too many arguments for command 'add'.")
        try:
            for value in values:
                int(value)
        except ValueError:
            raise UserInputError("The ID must be a number.")

    @classmethod
    def remove(cls, values):
        if not values:
            raise UserInputError("at least one ID is required.")
        if len(values) > 100:
            raise UserInputError("Too many arguments for command 'remove'.")
        try:
            for value in values:
                int(value)
        except ValueError:
            raise UserInputError("The ID must be a number.")

    @classmethod
    def start(cls, values):
        if values:
            raise UserInputError("This command doesn't take argument.")

    @classmethod
    def update(cls, values):
        if not len(values):
            raise UserInputError("One argument is required after 'update'.")

        if '=' not in values[0]:
            raise UserInputError("Argument must be of the form name=value'.")

        attr, value = [v.strip() for v in values[0].split('=', 1)]
        if value:
            new_value = ' '.join([value.strip()] + [v.strip() for v in values[1:]])
        else:
            new_value = ' '.join([v.strip() for v in values[1:]])
        if attr.lower() not in FormTournamentRegister.INPUT_TOURNAMENT_REGISTER_UPDATE:
            raise UserInputError("Attribute '{}' doesn't exist.".format(attr.lower()))

        cls._raise_error_if_value_user_wrong(attr.lower(), new_value)
