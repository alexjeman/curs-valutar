# Generated by Django 3.0.7 on 2020-06-23 19:09

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
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RatesHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='currencyitem', to='wallet.Currency')),
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
                ('rate_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='historyitem', to='wallet.RatesHistory')),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='operationitem', to='wallet.Wallet')),
            ],
        ),
    ]
