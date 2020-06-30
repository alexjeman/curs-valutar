from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    registered_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    website = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.registered_name}'


class Currency(models.Model):
    bank = models.ForeignKey(
        Bank, related_name='rateprovider', default=1, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=50)

    def __str__(self):
        return f'Bank: {self.bank}, {self.abbr}'


class RatesHistory(models.Model):
    currency = models.ForeignKey(
        Currency, related_name='currencyitem', on_delete=models.CASCADE
    )
    rate_sell = models.FloatField()
    rate_buy = models.FloatField()
    date = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f'{self.currency}, Rate Sell: {self.rate_sell} / Rate Buy: {self.rate_buy}, {self.date}'


class Wallet(models.Model):
    user = models.ForeignKey(
        User, related_name='walletitem', on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name='historyitem', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'User: {self.user}, Currency: {self.currency}'


class WalletOperation(models.Model):
    wallet = models.ForeignKey(
        Wallet, related_name='operationitem', on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name='currencyoperation', on_delete=models.CASCADE
    )
    rate = models.ForeignKey(
        RatesHistory, related_name='historyitem', on_delete=models.CASCADE
    )
    amount = models.FloatField()

    def __str__(self):
        return f'User: {self.wallet.user} | {self.wallet.currency} | Operation currency: {self.currency} | Price: {self.rate.rate_buy} | {self.amount}'
