'''
Classe qui sera hérité par toutes les views.
Certaine méthodes sont partager par toutes les views comme:
    -les indicateurs d'actions à l'utilisateur '[Q] --> quit'.
    -le système d'affichage en grille aavec grid(data).
    -les erreurs liés aux IDs avec 'ids_error'.
'''

from ...constante import SMALL_SPACE, LARGE_SPACE, EXTRA_SPACE, LARGE_DASH_TITLE


class View:

    # Afficher des indicateurs de choix.
    def quit(self):
        print('\n{}[Q] -> quit\n'.format(SMALL_SPACE))

    def quit_back(self):
        print('\n{}[Q] -> quit{}[B] -> back\n'.format(SMALL_SPACE, SMALL_SPACE))

    def quit_back_help(self):
        print('\n{}[Q] -> quit{}[B] -> back{}[H] -> help\n'.format(*[SMALL_SPACE for _ in range(3)]))

    def quit_back_pagination(self):
        print('\n{}[Q] -> quit{}[B] -> back'.format(SMALL_SPACE, SMALL_SPACE))
        print("{}[<] last turn   [>] next turn\n".format(SMALL_SPACE))

    def quit_back_help_pagination(self):
        print('\n{}[Q] -> quit{}[B] -> back{}[H] -> help'.format(*[SMALL_SPACE for _ in range(3)]))
        print("{}[<] last turn   [>] next turn\n".format(SMALL_SPACE))

    # Afficher les données en grille.
    def grid(self, data):
        col_len, r = [], ''
        [col_len.append(max(len(a) for a in arr)) for arr in zip(*data)]
        base_grid = self._base_grid(col_len)
        r += base_grid

        for index, line in enumerate(data):
            r += self._write_row(col_len, line)
            r += base_grid if index == 0 else ''
        r += base_grid
        print(r)

    def _write_row(self, col_len, line):
        row = ''
        for i, header in zip(col_len, line):
            row += '| {} '.format(header.rjust(i))
        return row + '|\n'

    def _base_grid(self, col_len):
        base = ''
        for i in col_len:
            base += '+{}'.format('-'*(i+2))
        return base + '+\n'

    # formate la façon d'afficher la description dans le formulaire.
    def description(self, message, jump, len_line):
        r, count = ' '*jump, 0
        message = message.split()
        for word in message:
            count += len(word) + 1
            if count > len_line:
                r += '\n' + ' '*jump + word + ' '
                count = 0
            else:
                r += word + ' '
        return r

    def tournament_focus(self, tournament):
        r = ''
        l1 = "{}{}Tournament: {} {}\n\n".format(SMALL_SPACE, LARGE_DASH_TITLE, tournament.name, LARGE_DASH_TITLE)
        l2 = "{}on {}\n\n".format(LARGE_SPACE, tournament.date)
        l3 = "{}place:   {}\n".format(EXTRA_SPACE, tournament.place)
        l4 = "{}country: {}\n".format(EXTRA_SPACE, tournament.country) if tournament.country else ''
        l5 = "{}time:    {}\n".format(EXTRA_SPACE, tournament.time)
        l6 = "{}turns:   {} turns\n\n".format(EXTRA_SPACE, tournament.n_turn)
        l7 = "{}description:\n".format(EXTRA_SPACE)
        l8 = "{}\n".format(self.description(tournament.description, 20, 40))
        r += l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8
        print(r)

    # Les views partage ces méthodes pour afficher les error d'IDs.
    def ids_error(self, wrong, registred, played, good, name='deleted'):
        r = ''
        wrong = list(set(wrong))
        registred = list(set(registred))
        played = list(set(played))
        good = list(set(good))
        r += self.id_exist(good, name) if good else ''
        r += self.id_no_exist_error(wrong) if wrong else ''
        r += self.id_registred_error(registred) if registred else ''
        r += self.id_on_play_error(played) if played else ''
        return r

    def id_exist(self, ids, name):
        ids = ', '.join(map(str, ids))
        return "\n{}Player(s) with id ({}) are {}.".format(SMALL_SPACE, ids, name)

    def id_no_exist_error(self, ids):
        wrong_ids = ', '.join(map(str, ids))
        return "\n{}Player(s) with id ({}) doesn't exist.".format(SMALL_SPACE, wrong_ids)

    def id_registred_error(self, ids):
        registred_ids = ', '.join(map(str, ids))
        return "\n{}Player(s) with id ({}) are already registred on a tournament.".format(SMALL_SPACE, registred_ids)

    def id_on_play_error(self, ids):
        played_ids = ', '.join(map(str, ids))
        return "\n{}Player(s) with id ({}) play in a tournament.".format(SMALL_SPACE, played_ids)
