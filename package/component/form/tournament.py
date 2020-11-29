'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerTournament'.
Chaque méthode est associé à une commande utilisateur:
    -sort
    -delete
    -focus
'''
from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormTournament(Form):

    name = 'tournament'

    INPUT_TOURNAMENT = ('sort', 'focus', 'delete')
    INPUT_TOURNAMENT_SORT = ('id', 'name', 'place', 'country', 'max_turn', 'date',
                             'n_player', 'time', 'description', 'ids_player', 'status')

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")

            if value[0].lower() in FormTournament.INPUT_TOURNAMENT:
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

        if not values[0].lower() in FormTournament.INPUT_TOURNAMENT_SORT:
            raise UserInputError("Can't sort by {}. This argument doesn't exist.".format(values[0]))

        if len(values) == 2 and values[1].lower() != 'reverse':
            raise UserInputError("The third argument can be 'reverse' nothing else.")

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
    def focus(cls, values):
        if len(values) != 1:
            raise UserInputError("One ID is required after 'show'.")

        # Vérifier si le premier argument est bien un nombre signifiant un ID.
        try:
            int(values[0])
        except ValueError:
            raise UserInputError("The ID must be a number.")
