'''
Classes qui vérifie l'input de l'utilisateur pour
le controlleur 'ControllerReport'.
Chaque méthode est associé à une commande utilisateur:
    -players
    -tournaments
    -turns
    -matches
'''

from .form import Form

from ..exception import UserInputError
from ...constante import SMALL_SPACE


class FormReport(Form):

    name = 'report'
    INPUT_REPORT = ('players', 'tournaments', 'turns', 'matches')
    INPUT_REPORT_PLAYERS = ('lastname', 'firstname', 'sex', 'birth', 'rank', 'points', 'status', 'finished', 'id')
    INPUT_REPORT_TOURNAMENTS = ('name', 'place', 'country', 'date', 'max_turn', 'n_player',
                                'time', 'description', 'ids_player', 'status', 'id')

    # exemple input: players by lastname reverse
    # tournaments by .... *reverse
    # turns  id
    # players id
    # matches id

    @classmethod
    def is_valid(cls, value):
        try:
            try:
                value = Form._format_input(value)
            except AttributeError:
                raise UserInputError("empty")

            if value[0].lower() in FormReport.INPUT_REPORT:
                cls.__dict__[value[0].lower()].__get__(None, cls)(value[1:])
            else:
                if len(value) == 1 and (value[0].upper() == 'B' or value[0].upper() == 'H'):
                    return ''
                raise UserInputError("First argument doesn't exist.")
            return ''
        except UserInputError as e:
            return "\n{}{}".format(SMALL_SPACE, e.args[0])

    @classmethod
    def players(cls, values):
        if len(values) > 4:
            raise UserInputError("Too many arguments.")
        elif not values:
            raise UserInputError("Minimum one argument is required.")

        elif len(values) == 1:
            try:
                int(values[0])
            except ValueError:
                if values[0].lower() not in FormReport.INPUT_REPORT_PLAYERS:
                    raise UserInputError("Second argument must be an ID or a sort name.")

        elif len(values) == 2:
            if values[0].lower() not in FormReport.INPUT_REPORT_PLAYERS:
                try:
                    int(values[0])
                except ValueError:
                    raise UserInputError("Second argument must be an ID or a sort name.")
                else:
                    if values[1].lower() != 'file':
                        raise UserInputError("Third argument after ID must be 'file' or nothing.")
            else:
                if values[1].lower() != 'reverse' and values[1].lower() != 'file':
                    raise UserInputError("Third argument after a sort name must be 'reverse' or 'file'.")

        elif len(values) == 3:
            if values[0].lower() not in FormReport.INPUT_REPORT_PLAYERS:
                raise UserInputError("Can't sort by {}".format(values[0]))
            if values[1].lower() != 'reverse':
                raise UserInputError("Third argument must be 'reverse' or 'file'.")
            if values[2].lower() != 'file':
                raise UserInputError("Fourth argument must be 'file' or nothing.")

    @classmethod
    def tournaments(cls, values):
        if len(values) > 4:
            raise UserInputError("Too many arguments.")
        elif not len(values):
            raise UserInputError("Minimum one argument is required")

        elif len(values) == 1:
            if values[0].lower() not in FormReport.INPUT_REPORT_TOURNAMENTS:
                raise UserInputError("Second argument must be a sort name.")

        elif len(values) == 2:
            if values[0].lower() not in FormReport.INPUT_REPORT_TOURNAMENTS:
                raise UserInputError("Second argument must be a sort name.")
            else:
                if values[1].lower() != 'reverse' and values[1].lower() != 'file':
                    raise UserInputError("Third argument after a sort name must be 'reverse' or 'file'.")

        elif len(values) == 3:
            if values[0].lower() not in FormReport.INPUT_REPORT_TOURNAMENTS:
                raise UserInputError("Can't sort by {}".format(values[0]))
            if values[1].lower() != 'reverse':
                raise UserInputError("Third argument must be 'reverse' or 'file'.")
            if values[2].lower() != 'file':
                raise UserInputError("Fourth argument must be 'file' or nothing.")

    @classmethod
    def turns(cls, values):
        if len(values) > 2:
            raise UserInputError("Too many arguments.")
        elif not values:
            raise UserInputError("Minimum one argument is required.")
        try:
            int(values[0])
        except ValueError:
            raise UserInputError("Second argument must be an ID.")
        if len(values) == 2 and values[1].lower() != 'file':
            raise UserInputError("Third argument must be 'file' or nothing.")

    @classmethod
    def matches(cls, values):
        cls.turns(values)
