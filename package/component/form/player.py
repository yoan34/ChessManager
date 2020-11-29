'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerPlayer'.
Chaque méthode est associé à une commande utilisateur:
    -sort
    -update
    -delete
    -create
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormPlayer(Form):

    name = 'player'

    INPUT_PLAYER = ('sort', 'update', 'delete', 'create')
    INPUT_PLAYER_UPDATE = ('lastname', 'firstname', 'sex', 'birth', 'rank', 'status')
    INPUT_PLAYER_CREATE = ('lastname', 'firstname', 'sex', 'birth', 'rank')
    INPUT_PLAYER_SORT = ('lastname', 'firstname', 'sex', 'birth', 'rank', 'points', 'status', 'finished', 'id')

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")

            if value[0].lower() in FormPlayer.INPUT_PLAYER:
                cls.__dict__[value[0].lower()].__get__(None, cls)(value[1:])
            else:
                if len(value) == 1 and (value[0].upper() == 'B' or value[0].upper() == 'H'):
                    return ''
                raise UserInputError("First argument doesn't exist.")
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])

    @classmethod
    def sort(cls, values):
        if not values:
            raise UserInputError("One argument is required after 'sort'.")
        if len(values) > 2:
            raise UserInputError("Too many arguments for command 'sort'.")

        if not values[0].lower() in FormPlayer.INPUT_PLAYER_SORT:
            raise UserInputError("Can't sort by {}. This argument doesn't exist.".format(values[0]))

        if len(values) == 2 and values[1].lower() != 'reverse':
            raise UserInputError("The third argument can be 'reverse' nothing else.")

    @classmethod
    def update(cls, values):
        # on analyse les arguments après avoir vérifier que le premier est bien 'update'.
        if len(values) < 2:
            raise UserInputError("Minimum two argument is required after 'update'.")

        # Vérifier si le premier argument est bien un nombre signifiant un ID.
        try:
            int(values[0])
        except ValueError:
            raise UserInputError("The ID must be a number.")

        # Si on est ici tout s'est bien passé, on a le ID et il existe au moins un argument derriere.
        args = values[1:]
        for arg in args:
            if arg.count('=') == 0 or arg.count('=') > 1:
                raise UserInputError("Arguments must be of the form: name=value")
            attr, value = arg.split('=')
            if attr.lower() not in FormPlayer.INPUT_PLAYER_UPDATE:
                raise UserInputError("Attribute '{}' doesn't exist.".format(attr.lower()))

            # Vérifier la value en fonction de l'attr
            cls._raise_error_if_value_user_wrong(attr.lower(), value)

    @classmethod
    def delete(cls, values):
        if not values:
            raise UserInputError("at least one ID is required.")
        if len(values) > 100:
            raise UserInputError("Too many arguments for command 'delete'.")
        try:
            for value in values:
                int(value)
        except ValueError:
            raise UserInputError("The ID must be a number.")

    @classmethod
    def create(cls, values):
        if not len(values) == 5:
            raise UserInputError("Arguments [lastname, firstname, sex, birth, rank] are required.")

        for attr, value in zip(FormPlayer.INPUT_PLAYER_CREATE, values):
            cls._raise_error_if_value_user_wrong(attr, value)
