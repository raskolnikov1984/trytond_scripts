#!/usr/bin/env python3
from proteus import Model, config
import psycopg
import csv

fe_url = 'https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey='

database = 'tryton'
config_file = '/etc/trytond.conf'
config.set_trytond(database, config_file=config_file)


def read_csv(file_: str):
    with open(file_, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        header = next(reader)
        data = [
            {l: n for n, l in zip(row, header)} for row in reader]

    return data


def updateInvoiceInfoFe(id_, cufe):

    with psycopg.connect(
            f"dbname={database} user=postgres host=db password=SUp3r-pass*DB"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE account_invoice SET
                fe_delivery_state='done',
                fe_cufe=%s,
                fe_qrcode=%s,
                fe_delivery_error_message='' WHERE id=%s;
                """, (cufe, fe_url+cufe, id_))
        conn.commit()


if __name__ == '__main__':

    Invoice = Model.get('account.invoice')
    failed_invoices = Invoice.find([
        ('state', 'in', ['posted', 'paid']),
        ('fe_delivery_state', '=', 'failure'),
        ('type', '=', 'out')
    ])

    data = read_csv('./facturas_fallidas.csv')
    for invoice in failed_invoices:
        number, id_ = invoice.number, invoice.id
        register = list(filter(lambda item: item['Numero'] == number, data))
        if register:
            CUFE = register[0]['CUFE/CUDE']
            raise Exception(number)
            updateInvoiceInfoFe(id_, CUFE)
