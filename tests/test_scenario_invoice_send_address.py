import unittest
from decimal import Decimal

from proteus import Model, Wizard
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear, create_tax)
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Imports

        # Install account_invoice
        activate_modules('account_invoice_send_address')

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)

        # Create tax
        tax = create_tax(Decimal('.10'))
        tax.save()

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()
        address, = party.addresses

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create invoice without send address
        Invoice = Model.get('account.invoice')
        invoice = Invoice()
        invoice.party = party
        self.assertEqual(invoice.invoice_address, address)
        self.assertEqual(invoice.send_address, address)

        # Create a send address and check it's used
        send_address = party.addresses.new()
        send_address.send_invoice = True
        party.save()
        _, send_address = party.addresses
        self.assertEqual(bool(send_address.send_invoice), True)
        invoice = Invoice()
        invoice.party = party
        self.assertEqual(invoice.invoice_address, address)
        self.assertEqual(invoice.send_address, send_address)

        # Credit invoice and check send address is copied
        invoice.payment_term = payment_term
        invoice.save()
        credit = Wizard('account.invoice.credit', [invoice])
        credit.execute('credit')
        refund_invoice, = Invoice.find([('id', '!=', invoice.id)])
        self.assertEqual(refund_invoice.send_address, send_address)
