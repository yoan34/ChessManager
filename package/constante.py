'''
Ici sont stocké toutes les constantes utilisé dans le programme.
On peut changer le 'style' d'affichage à travers quelques constantes:
    -SMALL_SPACE
    -SMALL_DASH_TITLE

le maximum de caractère dans un champs d'en-tête dans l'affichage en mode
grille avec:
    -MAX_CHAR_IDS_TOURNAMENTS
    -MAX_CHAR_DESCRIPTION
    -MAX_CHAR_NAME
    -MAX_CHAR_PLACE
    -MAX_CHAR_IDS_PLAYERS

des paramètres pour borné les valeurs autorisé dans la création de tournois:
    -MAX_CHAR_DESCRIPTION_TOURNAMENT
    -MAX_CHAR_NAME_AND_PLACE_TOURNAMENT
    -MAX_CHAR_COUNTRY_TOURNAMENT
    -MIN_NUMBER_OF_TURN
    -MAX_NUMBER_OF_TURN
    -MIN_NUMBER_OF_PLAYER
    -MAX_NUMBER_OF_PLAYER

et dans la création de joueurs:
    -MAX_CHAR_LASTNAME_AND_FIRSTNAME_PLAYER
    -MIN_RANK_PLAYER
    -MAX_RANK_PLAYER
    -MIN_DATE_BIRTH
    -MAX_DATE_BIRTH

'''
import datetime
import os

# Le chemin ou sera créer le dossier 'report'.
location_report_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANDOM_PLAYER = 20


SMALL_SPACE = ' ' * 5
MEDIUM_SPACE = SMALL_SPACE * 2
LARGE_SPACE = SMALL_SPACE * 3
EXTRA_SPACE = SMALL_SPACE * 4

SMALL_DASH_TITLE = '-' * 8
MEDIUM_DASH_TITLE = SMALL_DASH_TITLE * 2
LARGE_DASH_TITLE = SMALL_DASH_TITLE * 4


# ############# VIEW ################
MAX_CHAR_BY_LINE_DESCRIPTION = 20
MAX_CHAR_NAME_NO_GRID = 16

# - - customisation de l'affichage en grille - - #
MAX_CHAR_IDS_TOURNAMENTS = 20
MAX_CHAR_DESCRIPTION = 10
MAX_CHAR_NAME = 10
MAX_CHAR_PLACE = 25
MAX_CHAR_IDS_PLAYERS = 30


# ############# FORM ################
# Tournament
MAX_CHAR_DESCRIPTION_TOURNAMENT = 250
MAX_CHAR_NAME_AND_PLACE_TOURNAMENT = 100
MAX_CHAR_COUNTRY_TOURNAMENT = 30

MIN_NUMBER_OF_TURN = 3
MAX_NUMBER_OF_TURN = 9

MIN_NUMBER_OF_PLAYER = 8
MAX_NUMBER_OF_PLAYER = 32

# Player
MAX_CHAR_LASTNAME_AND_FIRSTNAME_PLAYER = 30

MIN_RANK_PLAYER = 0
MAX_RANK_PLAYER = 1999

MIN_DATE_BIRTH = datetime.datetime(1961, 1, 1)
MAX_DATE_BIRTH = datetime.datetime(2008, 1, 1)
