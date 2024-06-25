#!/usr/bin/env python3
from proteus import Model, config
import os
import csv


def iterador_csv(path_folder: str):
    # Diccionario que contrendra la informacion
    file_data = {}

    # Obtener todos los nombres de los archivos csv
    file_list = os.listdir(path_folder)

    # iterar sobre las lista de los nombre de los archivos
    for file_name in file_list:
        if file_name.endswith('.csv'):
            file_path = os.path.join(path_folder, file_name)
            with open(file_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                header = next(reader)
                data = [
                    {l: n for n, l in zip(row, header)} for row in reader]
                file_data[file_name] = data

    return file_data


database = 'tryton'
config_file = '/etc/trytond.conf'


cuentas = {
    'Terminal LS - Efectivo TPV': 10297,
    'Terminal LS - Transferencia TPV': 10299,
    'Terminal LS - Tarjeta TPV': 10299,
    'Terminal SE - Transferencia TPV': 10298,
    'Terminal SE - Efectivo TPV': 9546
}
# StoreA
file_date: dict = iterador_csv("./StoreA/11050501 - Caja")
# file_date: dict = iterador_csv("./StoreA/11100503 - Bancolombia")

# StoreB
# file_date: dict = iterador_csv("./StoreB/11050502 - Caja")
# file_date: dict = iterador_csv("./StoreB/11100504 - Bancolombia")

config.set_trytond(database, config_file=config_file)
Moves = Model.get('account.move')

for key in file_date.keys():
    print(key)
    print(file_date[key])
    moves = file_date[key]

    for move in moves:
        move_ = Moves.find([
            ('number', '=', move['N° DOC']),
            ('journal', '=', 5)])
        for line in move_[0].lines:
            print(line.account.code)
            if line.account.code != '130505':
                line.account = cuentas['ORIGEN']
        move_[0].save()
