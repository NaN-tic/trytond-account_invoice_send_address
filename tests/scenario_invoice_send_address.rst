=============================
Invoice Send Address Scenario
=============================

Imports::
    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install account_invoice::

    >>> config = activate_modules('account_invoice_send_address')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create party::

    >>> Party = Model.get('party.party')
    >>> party = Party(name='Party')
    >>> party.save()
    >>> address, = party.addresses

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create invoice without send address::

    >>> Invoice = Model.get('account.invoice')
    >>> InvoiceLine = Model.get('account.invoice.line')
    >>> invoice = Invoice()
    >>> invoice.party = party
    >>> invoice.invoice_address == address
    True
    >>> invoice.send_address == address
    True

Create a send address and check it's used::

    >>> send_address = party.addresses.new()
    >>> send_address.send_invoice = True
    >>> party.save()
    >>> _, send_address = party.addresses
    >>> bool(send_address.send_invoice)
    True
    >>> invoice = Invoice()
    >>> invoice.party = party
    >>> invoice.invoice_address == address
    True
    >>> invoice.send_address == send_address
    True

Credit invoice and check send address is copied::

    >>> invoice.payment_term = payment_term
    >>> invoice.save()
    >>> credit = Wizard('account.invoice.credit', [invoice])
    >>> credit.execute('credit')
    >>> refund_invoice, = Invoice.find([('id', '!=', invoice.id)])
    >>> refund_invoice.send_address == send_address
    True
