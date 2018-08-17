# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Address', 'Invoice', 'ContractConsumption', 'Work', 'Sale']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'
    send_invoice = fields.Boolean('Send Invoice',
        help='Indicates if the address will the one used to send invoices to.')


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    send_address = fields.Many2One('party.address', 'Send Address',
        domain=[
            ('party', '=', Eval('party')),
            ],
        states={
            'readonly': Eval('state') != 'draft',
            'invisible': Eval('type') != 'out',
            },
        depends=['state', 'party', 'type'], ondelete='RESTRICT',
        help="Address where the invoice will be sent to.")

    def on_change_party(self):
        super(Invoice, self).on_change_party()
        self.send_address = None
        if self.party and self.type == 'out':
            self.send_address = self.party.address_get(type='send_invoice')

    def _credit(self):
        credit = super(Invoice, self)._credit()
        credit.send_address = self.send_address
        return credit


class ContractConsumption(metaclass=PoolMeta):
    __name__ = 'contract.consumption'

    @classmethod
    def _get_invoice(cls, keys):
        invoice = super(ContractConsumption, cls)._get_invoice(keys)
        invoice.send_address = invoice.party.address_get(type='send_invoice')
        return invoice


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    def _get_invoice(self):
        # create invoice from project invoice or project invoice milestone
        invoice = super(Work, self)._get_invoice()
        invoice.send_address = self.party.address_get(type='send_invoice')
        return invoice


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def _get_invoice_sale(self):
        invoice = super(Sale, self)._get_invoice_sale()
        invoice.send_address = self.party.address_get(type='send_invoice')
        return invoice
