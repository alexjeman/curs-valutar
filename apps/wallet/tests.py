from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date as datecreated

from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)


class WalletTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # User table test data
        testuser1 = User.objects.create_user(
            username='testuser1', password='password123'
        )
        testuser1.save()

        # Currency table test data
        testcurrency1 = Currency.objects.create(
            name='Australian Dollar', abbr='AUD'
        )
        testcurrency1.save()

        # Wallet table test data
        wallet1 = Wallet.objects.create(
            user=testuser1, currency=testcurrency1
        )
        wallet1.save()

        # Rates history table test data
        ratehistory1 = RatesHistory.objects.create(
            currency=testcurrency1, rate='11.8621'
        )
        ratehistory1.save()

        # Wallet operations table test data
        walletoperations1 = WalletOperation.objects.create(
            wallet=wallet1, rate=ratehistory1, amount=100000
        )
        walletoperations1.save()

        walletoperations2 = WalletOperation.objects.create(
            wallet=wallet1, rate=ratehistory1, amount=70000
        )
        walletoperations2.save()

    def test_currency(self):
        currency = Currency.objects.get(id=1)
        abbr = f'{currency.abbr}'
        currency_name = f'{currency.name}'
        self.assertEqual(abbr, 'AUD')
        self.assertEqual(currency_name, 'Australian Dollar')

    def test_wallet(self):
        wallet = Wallet.objects.get(id=1)
        user = f'{wallet.user}'
        currency = f'{wallet.currency}'
        self.assertEqual(user, 'testuser1')
        self.assertEqual(currency, f'{Currency.objects.get(id=1)}')

    def test_rates_history(self):
        rate_history = RatesHistory.objects.get(id=1)
        currency = f'{rate_history.currency}'
        rate = f'{rate_history.rate}'
        date = f'{rate_history.date}'
        self.assertEqual(currency, f'{Currency.objects.get(id=1)}')
        self.assertEqual(rate, '11.8621')
        self.assertEqual(date, f'{datecreated.today()}')

    def test_wallet_operations(self):
        wallet_operations = WalletOperation.objects.filter(wallet=1)
        amount = sum([i.amount for i in wallet_operations])
        self.assertEqual(amount, float(170000))
