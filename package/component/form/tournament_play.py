'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerTournamentPlay'.
Chaque méthode est associé à une commande utilisateur:
    -match
    -next
    -update
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormTournamentPlay(Form):

    name = 'tournament_play'

    INPUT_TOURNAMENT_PLAY = ('match', 'next', 'update', 'm')
    INPUT_TOURNAMENT_PLAY_UPDATE = ('place', 'country', 'description')

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")

            if value[0].lower() in FormTournamentPlay.INPUT_TOURNAMENT_PLAY:
                name = value[0].lower() if value[0].lower() != 'm' else 'match'
                cls.__dict__[name].__get__(None, cls)(value[1:])
            else:
                if len(value) == 1 and (value[0].upper() == 'B' or value[0].upper() == 'H'):
                    return ''
                if len(value) == 1 and (value[0] == '<' or value[0] == '>'):
                    return ''
                raise UserInputError("First argument doesn't exist.")
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])

    @classmethod
    def match(cls, values):
        if len(values) != 3:
            raise UserInputError("3 arguments are required after 'match'.")

        if values[1] != 'winner' and values[1] != 'w':
            raise UserInputError("The third argument must be 'winner' or 'w'.")
        try:
            int(values[0])
            int(values[2])
        except ValueError:
            raise UserInputError("The second and the fourth argument must be ID number.")

    @classmethod
    def next(cls, values):
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
        if attr.lower() not in FormTournamentPlay.INPUT_TOURNAMENT_PLAY_UPDATE:
            raise UserInputError("Attribute '{}' doesn't exist.".format(attr.lower()))

        cls._raise_error_if_value_user_wrong(attr.lower(), new_value)
