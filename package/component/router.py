'''
La classe Router sert à lancer le bon 'Controller' grâce a son 'path'.

La méthode 'routed' lance le 'Controller' associé au 'path' et retourne
un 'path'. Si le 'path' de retour est différent, la méthode  appelle
directement le 'Controller' associé au nouveau 'path'.

Les méthodes 'ask' et '_clear' servent respectivement à demander un
'input' à l'utilisateur et effacer le terminal.
'''

import os
from ..constante import SMALL_SPACE


class Router:

    def __init__(self):
        self.path = 'home'

    def routed(self, controllers, action):
        # Si le 'path' de sorti n'est pas le même que celui d'entré,
        # on apelle le bon controller pour afficher la page.

        new_path = self.run_controller(controllers, action)
        if self.path != new_path:
            self.path = new_path
            self.run_controller(controllers, None)

    def run_controller(self, controllers, action):
        # cette méthode apelle la méthode 'run()' du bon 'controller'.
        path_name = self.get_path_name()
        controller = list(filter(lambda c: c.controller_name == path_name, controllers))[0]
        self._clear()
        return controller.run(self.path, action)

    def get_path_name(self):
        # Transforme le format 'path' de manière à correspondre à des nom de Controller.
        path_section = self.path.split('/')
        if len(path_section) == 1:
            return path_section[0]

        path_name = []
        for section in path_section[1:]:
            try:
                int(section)
            except ValueError:
                path_name.append(section)
        return '_'.join(path_name)

    @property
    def ask(self):
        # Créer une demande d'input à l'aide de méthode transformer en attribut.
        return input("{}> ".format(SMALL_SPACE))

    def _clear(self):
        # Permet d'effacer la console sur Window / iOS.
        os.system('cls') if os.name == 'nt' else os.system('clear')
