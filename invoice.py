# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Address', 'Invoice', 'Sale']
__metaclass__ = PoolMeta


class Address:
    __name__ = 'party.address'
    send_invoice = fields.Boolean('Send Invoice',
        help='Indicates if the address will the one used to send invoices to.')


class Invoice:
    __name__ = 'account.invoice'

    send_address = fields.Many2One('party.address', 'Send Address',
        domain=[
            ('party', '=', Eval('party')),
            ],
        states={
            'readonly': Eval('state') != 'draft',
            'invisible': ~Eval('type').in_(['out_invoice', 'out_credit_note']),
            },
        depends=['state', 'party', 'type'], ondelete='RESTRICT',
        help="Address where the invoice will be sent to.")

    def on_change_party(self):
        changes = super(Invoice, self).on_change_party()
        if self.party:
            if self.type in ('out_invoice', 'out_credit_note'):
                send_address = self.party.address_get(type='send_invoice')
                if send_address:
                    changes['send_address'] = send_address.id
                    changes['send_address.rec_name'] = send_address.rec_name
            else:
                changes['send_address'] = None
        return changes

    def _credit(self):
        values = super(Invoice, self)._credit()
        if self.send_address:
            values['send_address'] = self.send_address.id
        return values


class Sale:
    __name__ = 'sale.sale'

    def _get_invoice_sale(self, invoice_type):
        invoice = super(Sale, self)._get_invoice_sale(invoice_type)
        invoice.send_address = self.party.address_get(type='send_invoice')
        return invoice
