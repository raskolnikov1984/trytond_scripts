#!/usr/bin/env python3
from proteus import Model, config
import datetime

database = 'tryton'
config_file = '/etc/trytond.conf'

config.set_trytond(database, config_file=config_file)
Moves = Model.get('stock.move')

moves = Moves.find([
    ('from_location.type', '=', 'supplier'),
    ('state', '=', 'draft'), ('shipment', '=', None)])

# print(len(moves))

for move in moves:
    invoice_lines = bool(move.invoice_lines)
    invoice_date = bool(move.invoice_lines[0].invoice.invoice_date)
    year = bool(move.invoice_lines[0].invoice.invoice_date.year)
    if invoice_lines and invoice_date and year == 2023:
        print(move.invoice_lines[0].invoice.number)
        move.effective_date = datetime(2023, 12, 31)
        try:
            if move.to_location == 1:
                move.to_location = 3
            else:
                if move.to_location == 12:
                    move.to_location = 11

            move.click('do')
        except ValueError:
            raise Exception("Oops!  That was no valid number.  Try again...")
