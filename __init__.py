# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Address,
        invoice.Invoice,
        module='account_invoice_send_address', type_='model')
    Pool.register(
        invoice.ContractConsumption,
        depends=['contract'],
        module='account_invoice_send_address', type_='model')
    Pool.register(
        invoice.Work,
        depends=['project_invoice'],
        module='account_invoice_send_address', type_='model')
    Pool.register(
        invoice.Sale,
        depends=['sale'],
        module='account_invoice_send_address', type_='model')
