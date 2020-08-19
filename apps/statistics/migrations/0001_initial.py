# Generated by Django 3.0.8 on 2020-08-19 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatesPredictionText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.Currency')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RatesPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('rate_sell', models.FloatField()),
                ('date', models.DateField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currencypredictions', to='wallet.Currency')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
