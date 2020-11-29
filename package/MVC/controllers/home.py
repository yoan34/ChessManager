'''
Controlleur qui permet d'afficher le menu
principal et d'intéragir avec l'utilisateur
pour diriger retourner le bon 'path'.
    -delete
    -sort
    -focus
    -back
    -help

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

from ..views.home import ViewHome
from ...component.form.home import FormHome


class ControllerHome:

    def __init__(self):
        self.controller_name = 'home'
        self.view = ViewHome()
        self.error = ''

    # Principales méthodes pour lancer le controller et afficher le menu principal.
    def run(self, path, value):

        value = None if value is not None and not value.strip() else value

        self.error = FormHome.is_valid(value)

        if not self.error:
            if value == '1':
                return 'home/tournament_new'
            elif value == '2':
                return 'home/tournament'
            elif value == '3':
                return 'home/player'
            elif value == '4':
                return 'home/report'

        self.view.home()
        print(self.error) if self.error and value is not None else None
        self.view.quit()

        return path
