'''
La classes 'FileManager' est utilisé pour créer des rapports.
Elles à plusieurs méthodes pour cela:
    -create(values): Crée le fichier en fabriquant un nom de
        fichier avec les données d'entrée, récupère le 'stdout'
        d'origine et renvoi celui-ci avec le fichier.

    -close(file, origin_std): Ferme le fichier et remet le 'stdout'
        d'origine.

    -make_folder(): Apeller la première fois du lancement du controlleur
        'ControllerReport' pour vérifier et créer les dossiers qui vont
        receptionner les différents rapports.

    -get_name(values): Méthodes pour créer un nom de fichier.
'''

import datetime
import sys
import os

from .exception import FileError
from ..constante import location_report_folder, SMALL_SPACE


class FileManager:

    @classmethod
    def create(cls, values):
        name = cls.get_name(values)
        path = os.path.join(location_report_folder, 'report', values[0], name)
        try:
            file = open(path, 'w', encoding='utf-8')
            origin_stdout = sys.stdout
            sys.stdout = file
            return file, origin_stdout
        except IOError:
            raise FileError("{}Problem with the file.".format(SMALL_SPACE))

    @classmethod
    def close(cls, file, origin_stdout):
        file.close()
        sys.stdout = origin_stdout

    @classmethod
    def make_folder(cls):
        if not os.path.exists(os.path.join(location_report_folder, 'report')):
            os.mkdir(os.path.join(location_report_folder, 'report'))
            os.mkdir(os.path.join(location_report_folder, 'report/players'))
            os.mkdir(os.path.join(location_report_folder, 'report/tournaments'))
            os.mkdir(os.path.join(location_report_folder, 'report/turns'))
            os.mkdir(os.path.join(location_report_folder, 'report/matches'))

    @classmethod
    def get_name(cls, values):
        try:
            int(values[1])
        except ValueError:
            name = '_'.join(values[1:])
            name = "by_"+name
        else:
            name = "on_tournament_" + values[1]

        d = datetime.datetime.today()
        date = "{:02}-{:02}-{} {:02}h{:02}".format(d.day, d.month, str(d.year)[2:], d.hour, d.minute)
        name = "{} {}.txt".format(name, date)
        return name
