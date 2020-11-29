'''
Ce fichier est le fichier principal.
Il utilise le 'Router' et les 8 'Controllers' pour générer,
afficher, interagir avec la base de donnée.
'''

from package.component.router import Router

from package.MVC.controllers.home import ControllerHome
from package.MVC.controllers.player import ControllerPlayer
from package.MVC.controllers.tournament import ControllerTournament
from package.MVC.controllers.tournament_register import ControllerTournamentRegister
from package.MVC.controllers.tournament_play import ControllerTournamentPlay
from package.MVC.controllers.tournament_over import ControllerTournamentOver
from package.MVC.controllers.tournament_new import ControllerTournamentNew
from package.MVC.controllers.report import ControllerReport

controllers = (
    ControllerHome(),
    ControllerPlayer(),
    ControllerTournament(),
    ControllerTournamentRegister(),
    ControllerTournamentPlay(),
    ControllerTournamentOver(),
    ControllerTournamentNew(),
    ControllerReport(),
    )

action = ''
router = Router()

while True:
    router.routed(controllers, action)
    action = router.ask
    quit() if action.upper() == 'Q' else None
