# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Address,
        invoice.Invoice,
        invoice.Sale,
        invoice.ContractConsumption,
        invoice.Work,
        module='account_invoice_send_address', type_='model')
