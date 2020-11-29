'''
Classe qui représente la view du controlleur
'ControllerNewTournament'.
'''

from .view import View

from ...constante import SMALL_SPACE, MEDIUM_SPACE, MAX_CHAR_BY_LINE_DESCRIPTION


class ViewTournamentNew(View):

    QUESTIONS = ('<Choice a name>', '<Choice a place>', '<Choice a country (optional)>',
                 "<Choice a control of time among ' bullet, blitz, speed hit'>",
                 "<Choice a number of players (default 8)>",
                 "<Choice a number of turn (default 4)>", "<Add a description (optional)>")

    def tournament_new(self, data):
        r = ''
        l1 = '{}New Tournament\n\n'.format(MEDIUM_SPACE)
        l2 = '{}name: {}\n'.format(SMALL_SPACE, data['name'])
        l3 = '{}place: {}\n'.format(SMALL_SPACE, data['place'])
        l4 = '{}country (optional): {}\n'.format(SMALL_SPACE, data['country'])
        l5 = '{}time control: {}\n'.format(SMALL_SPACE, data['time'])
        l6 = '{}number of players: {}\n'.format(SMALL_SPACE, data['n_player'])
        l7 = '{}number of turn: {}\n'.format(SMALL_SPACE, data['n_turn'])
        l8 = '{}description (optional): {}\n'.format(SMALL_SPACE, data['description'])
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8
        print(r)

    def tournament_new_over(self, data):
        r = ''
        l1 = '{}The tournament: {}\n'.format(MEDIUM_SPACE, data['name'])
        l2 = '{}was created sucessfully on {}\n\n'.format(MEDIUM_SPACE, data['date'])
        country = "in {}".format(data['country']) if data['country'] else ''
        l3 = '{}The place is {} {}\n\n'.format(SMALL_SPACE, data['place'], country)
        l4 = '{}The time control is {} and the number of turn is {}\n\n'.format(
            SMALL_SPACE, data['time'], data['n_turn'])
        r += l1 + l2 + l3 + l4
        if data['description']:
            r += "{}description:\n{}\n\n".format(
                SMALL_SPACE, self.description(data['description'], 10, MAX_CHAR_BY_LINE_DESCRIPTION))
        print(r)

    def tournament_new_question(self, index):
        print("\n{}{}".format(SMALL_SPACE, ViewTournamentNew.QUESTIONS[index]))
