'''
Classe qui représente la view du controlleur
'ControllerHome'.
'''

from .view import View

from ...constante import SMALL_SPACE, MEDIUM_SPACE


class ViewHome(View):

    def home(self):
        r = ''
        l1 = '{}Manager Chess\n\n'.format(MEDIUM_SPACE)
        l2 = '{}1. Create a tournament.\n'.format(SMALL_SPACE)
        l3 = '{}2. Tournaments.\n'.format(SMALL_SPACE)
        l4 = '{}3. Players.\n'.format(SMALL_SPACE)
        l5 = '{}4. Get a report.'.format(SMALL_SPACE)
        r += l1 + l2 + l3 + l4 + l5
        print(r)
