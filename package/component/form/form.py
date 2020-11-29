'''
La classe Form est hérité des autres classes Form pour leur transmettre des
méthodes qui servent à vérifier l'input de l'utilisateur, et de formater
l'input.
'''

import datetime

from ..exception import UserInputError
from ...constante import (
    MAX_CHAR_LASTNAME_AND_FIRSTNAME_PLAYER, MIN_RANK_PLAYER, MAX_RANK_PLAYER,
    MAX_CHAR_NAME_AND_PLACE_TOURNAMENT, MAX_CHAR_COUNTRY_TOURNAMENT, MIN_NUMBER_OF_TURN,
    MAX_NUMBER_OF_TURN, MIN_NUMBER_OF_PLAYER, MAX_NUMBER_OF_PLAYER, MAX_CHAR_DESCRIPTION_TOURNAMENT,
    MIN_DATE_BIRTH, MAX_DATE_BIRTH
    )


class Form:

    @classmethod
    def _format_input(cls, string):
        result = []
        s = string.split(',')
        for arr in s:
            arr2 = arr.split()
            arr2 = [item.strip() for item in arr2]
            [result.append(item) for item in arr2]
        return result

    @classmethod
    def _is_alpha(cls, value, attr, n):
        if len(value) > n:
            raise UserInputError('The {} must have {} characters max.'.format(attr, n))
        elif '-' in value:
            if value.count('-') > 2:
                raise UserInputError("{} can contain two dash maximum.".format(attr))
            lastName = value.split('-')
            for word in lastName:
                if not word.isalpha():
                    raise UserInputError("{} contain only alphanumeric and one dash between name.".format(attr))
        else:
            if not value.isalpha():
                raise UserInputError("{} contain only alphanumeric and one dash between name.".format(attr))

    @classmethod
    def _raise_error_if_value_user_wrong(cls, attr, value):
        if attr == 'lastname' or attr == 'firstname':
            cls._is_alpha(value, attr, MAX_CHAR_LASTNAME_AND_FIRSTNAME_PLAYER)

        elif attr == 'sex' and value.upper() != 'M' and value.upper() != 'F':
            raise UserInputError("Sex must be 'M' or 'F'.")

        elif attr == 'birth':
            cls._raise_error_if_date_wrong(value)

        elif attr == 'rank':
            try:
                rank = int(value)
                if rank < MIN_RANK_PLAYER or rank > MAX_RANK_PLAYER:
                    raise UserInputError("The rank {} out of range [{} - {}]."
                                         .format(rank, MIN_RANK_PLAYER, MAX_RANK_PLAYER))
            except ValueError:
                raise UserInputError("The rank must be a number.")

        elif attr == 'status':
            if value != 'available':
                raise UserInputError("Status can only take the value 'available'.")

        elif attr == 'name' or attr == 'place':
            if len(value.strip()) == 0:
                raise UserInputError("{} must contain one characters.".format(attr))
            if len(value) > MAX_CHAR_NAME_AND_PLACE_TOURNAMENT:
                raise UserInputError("The {} must have less than {} characters."
                                     .format(attr, MAX_CHAR_NAME_AND_PLACE_TOURNAMENT))

        elif attr == 'country' and value != '':
            cls._is_alpha(value, attr, MAX_CHAR_COUNTRY_TOURNAMENT)

        elif attr == 'time':
            if value.capitalize() not in ('Bullet', 'Blitz', 'Speed hit'):
                raise UserInputError("time must be 'bullet', 'blitz' or 'speed hit'.")

        elif attr == 'n_turn':
            if not value:
                return
            try:
                turn = int(value)
                if turn < MIN_NUMBER_OF_TURN or turn > MAX_NUMBER_OF_TURN:
                    raise UserInputError("The number of Turn out of range [{} - {}]."
                                         .format(MIN_NUMBER_OF_TURN, MAX_NUMBER_OF_TURN))
            except ValueError:
                raise UserInputError("The number of turn must be a number.")

        elif attr == 'n_player':
            if not value:
                return
            try:
                players = int(value)
                if players < MIN_NUMBER_OF_PLAYER or players > MAX_NUMBER_OF_PLAYER:
                    raise UserInputError("The number of players out of range [{} jjj- {}]."
                                         .format(MIN_NUMBER_OF_PLAYER, MAX_NUMBER_OF_PLAYER))
                if players % 2 == 1:
                    raise UserInputError("The number of players must be even.")
            except ValueError:
                raise UserInputError("The number of players must be a number.")

        elif attr == 'description':
            if len(value) > MAX_CHAR_DESCRIPTION_TOURNAMENT:
                raise UserInputError("The description have less then {} characters."
                                     .format(MAX_CHAR_DESCRIPTION_TOURNAMENT))

    @classmethod
    def _raise_error_if_date_wrong(cls, date):
        if ':' in date or '/' in date or '-' in date:
            for sep in (':', '/', '-'):
                if len(date.split(sep)) == 3:
                    break
            else:
                raise UserInputError("Birth must be of the form: DD/MM/YYYY, can change '/' with '-' or ':'")
            sep = -1
            for c in (':', '/', '-'):
                if date.count(c) == 2:
                    sep = c
                    break
            day, month, year = date.split(sep)
            validDate = True
            try:
                birth = datetime.datetime(int(year), int(month), int(day))
                if birth < MIN_DATE_BIRTH or birth > MAX_DATE_BIRTH:
                    raise UserInputError(
                        "The date {}/{}/{} out of range [{}/{}/{} - {}/{}/{}].".format(
                            day, month, year, MIN_DATE_BIRTH.day, MIN_DATE_BIRTH.month, MIN_DATE_BIRTH.year,
                            MAX_DATE_BIRTH.day, MAX_DATE_BIRTH.month, MAX_DATE_BIRTH.year))
            except ValueError:
                raise UserInputError("{}/{}/{} doesn't exist.".format(day, month, year))

            if not validDate:
                raise UserInputError("Birth must be of the form: DD/MM/YYYY, can change '/' with '-' or ':'")
        else:
            raise UserInputError("Birth must be of the form: DD/MM/YYYY, can change '/' with '-' or ':'")
