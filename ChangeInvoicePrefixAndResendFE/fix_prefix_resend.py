#!/usr/bin/env python3
from proteus import Model, config
import csv
import psycopg
from time import sleep


with open('./Bicipizza_Facturas_Fallidas.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)

    registros = [
        {l: n for n, l in zip(row, header)} for row in reader]

with psycopg.connect(
        "dbname=tryton user=postgres host=db password=SUp3r-pass*DB") as conn:
    with conn.cursor() as cur:
        for invoice in registros:
            cur.execute(
                    """
                    UPDATE account_invoice set number=%s, reference=%s,
                    subtype=19 where number=%s """, (
                        invoice['Numero_Sustituto'],
                        invoice['Numero'],
                        invoice['Numero']))
            print(f"Facturas: {invoice['Numero']}")
    conn.commit()


database = 'tryton'
config_file = '/etc/trytond.conf'

config.set_trytond(database, config_file=config_file)

Invoice = Model.get('account.invoice')
failed_invoices = Invoice.find(
    [('number', 'ilike', 'LSPF%'),
     ('fe_delivery_state', 'in', ['draft', 'failure'])])

for invoice in failed_invoices:
    invoice.click('fe_send')
    sleep(1)
    print(invoice.number)
