'''
Controlleur qui permet d'afficher la création
d'un tournoi et d'entrer les différentes
informations nécessaires.

Chaque controlleur à une méthode 'run' qui est
appelé par le Router.
Chaque controlleur retourne le 'path' reçu en
entré ou en retourne un nouveau.
'''

from datetime import datetime

from ..models.tournament import ModelTournament
from ..views.tournament_new import ViewTournamentNew

from ...component.form.tournament_new import FormTournamentNew


class ControllerTournamentNew:

    QUESTIONS = ('name', 'place', 'country', 'time', 'n_player', 'n_turn', 'description', 'over')

    def __init__(self):
        self.controller_name = 'tournament_new'
        self.model = ModelTournament()
        self.view = ViewTournamentNew()
        self.error = ''
        self.index = 0
        self.tournament_over = False

        self.custom_tournament = {
            'name': '',
            'place': '',
            'country': '',
            'time': '',
            'n_turn': 4,
            'n_player': 8,
            'date': '',
            'description': '',
            'turns': [],
            'players': [],
            'status': 'register',
        }

    # Principales méthodes pour lancer le controller et afficher les données
    # du nouveau tournoi.
    def run(self, path, value):
        question = ControllerTournamentNew.QUESTIONS[self.index]

        # Si value == None c'est que la page à été charger en changeant de 'path'.
        # On veut alors simplement afficher le contenu.
        if value is not None:

            # On peut retourner à la page 'home' si on fait retour [B]; ou bien
            # avec n'importe quel 'input' si le formulaire est rempli.
            if value.upper() == 'B' or self.tournament_over:
                self.restart_custom_tournament()
                self.tournament_over = False
                return 'home'

            # On check si l'input est valide, une string comportant l'erreur est
            # retourner si l'input est non valide.
            self.error = FormTournamentNew.is_valid(value, question)

        # Si tout est ok, on avance dans le formulaire
        if not self.error and value is not None:
            self.custom_tournament[question] = value if value else self.custom_tournament[question]
            self.index += 1

        # On affiche la view du tournoi fini ou la view du formulaire.
        self.tournament_new_not_over() if self.index != 7 else self.tournament_new_over()

        print(self.error) if self.error and value is not None else None
        self.view.quit_back()

        return path

    def tournament_new_not_over(self):
        self.view.tournament_new(self.custom_tournament)
        self.view.tournament_new_question(self.index)

    def tournament_new_over(self):
        self.tournament_over = True
        date = "{}/{}/{}".format(datetime.today().day, datetime.today().month, datetime.today().year)
        self.custom_tournament['date'] = date

        # On affiche le rendu du nouveau tournois
        self.view.tournament_new_over(self.custom_tournament)

        # Ajouter le tournois dans la base de donnée
        self.model.create(self.custom_tournament)
        self.restart_custom_tournament()

    # Méthodes pour réinitialiser les données du nouveau tournoi.
    def restart_custom_tournament(self):
        self.custom_tournament = {
            'name': '',
            'place': '',
            'country': '',
            'time': '',
            'n_turn': 4,
            'n_player': 8,
            'date': '',
            'description': '',
            'turns': [],
            'players': [],
            'status': 'register',
        }
        self.index = 0
        self.error = ''
