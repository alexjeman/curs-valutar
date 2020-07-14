# Generated by Django 3.0.7 on 2020-07-13 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=50)),
                ('website', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=50)),
                ('bank', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rateprovider', to='wallet.Bank')),
            ],
        ),
        migrations.CreateModel(
            name='RatesHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_sell', models.FloatField()),
                ('rate_buy', models.FloatField()),
                ('date', models.DateField(db_index=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currencyitem', to='wallet.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historyitem', to='wallet.Currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='walletitem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currencyoperation', to='wallet.Currency')),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historyitem', to='wallet.RatesHistory')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operationitem', to='wallet.Wallet')),
            ],
        ),
    ]
