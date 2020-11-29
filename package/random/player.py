'''
Fichier pour créer des joueurs en les retournant
sous forme de tuple qui seront ensuite utilisé par
le constructeur 'Player'.
'''

from random import randint, choice, randrange
from datetime import date, timedelta

SEX = ['M', 'F']

LAST_NAMES_MEN = [
    'James', 'John', 'Robert', 'Michael', 'Wiliam', 'David', 'Joseph', 'Richard', 'Charles', 'Thomas', 'Christopher',
    'Daniel', 'Matthew', 'George', 'Anthony', 'Donald', 'Paul', 'Mark', 'Andrew', 'Edward', 'Steven', 'Kenneth',
    'Joshua', 'Kevin', 'Brian', 'Ronald', 'Timothy', 'Jason', 'Jeffrey', 'Ryan', 'Jacob', 'Frank', 'Gary', 'Nicholas',
    'Eric', 'Stephen', 'Jonathan', 'Larry', 'Justin', 'Raymond', 'Scott', 'Samuel', 'Brandon', 'Benjamin', 'Gregory',
    'Jack', 'Henry', 'Patrick', 'Alexander', 'Walter'
    ]

LAST_NAMES_WOMEN = [
    'Mary', 'Elizabeth', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Margaret', 'Susan', 'Dorothy', 'Sarah',
    'Jessica', 'Helen', 'Nancy', 'Betty', 'Karen', 'Lisa', 'Anna', 'Sandra', 'Emily', 'Ashley', 'Kimberly', 'Donna',
    'Ruth', 'Carol', 'Michelle', 'Laura', 'Amanda', 'Melissa', 'Rebecca', 'Deborah', 'Stephanie', 'Sharon', 'Kathleen',
    'Cynthia', 'Amy', 'Shirley', 'Emma', 'Angela', 'Catherine', 'Virginia', 'Katherine', 'Brenda', 'Pamela', 'Frances',
    'Nicole', 'Christine', 'Samantha', 'Evelyn', 'Rachel', 'Alice'
    ]

FIRST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
    'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Garcia', 'Martinez', 'Vidal', 'Marty', 'Fabre', 'Ruiz',
    'Pujol', 'Ferrer', 'Puig', 'Durand', 'Soler', 'Vila', 'Coste', 'Calvet', 'Pons', 'Mas', 'Batlle', 'Costa',
    'Ribes', 'Navarro', 'Olive', 'Grau', 'Moreno', 'Bosch', 'Munoz', 'Roca', 'Bousquet', 'Gimenez', 'Coll', 'Serra'
    ]

START_DATE_OF_BIRTH = date(1961, 1, 1)
END_DATE_OF_BIRTH = date(2008, 1, 1)


def get_random_player():
    sex = choice(SEX)
    last_name = choice(LAST_NAMES_MEN) if sex == 'M' else choice(LAST_NAMES_WOMEN)
    first_name = choice(FIRST_NAMES)
    date_of_birth = str(START_DATE_OF_BIRTH + timedelta(days=randrange((END_DATE_OF_BIRTH-START_DATE_OF_BIRTH).days)))
    year, month, day = date_of_birth.split('-')
    date_of_birth = '{}-{}-{}'.format(day, month, year)
    rank = randint(0, 1999)
    return (last_name, first_name, sex, date_of_birth, rank)
