# Generated by Django 3.2.12 on 2023-02-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=9, verbose_name='номер карты')),
                ('balance', models.FloatField(verbose_name='баланс карты')),
            ],
            options={
                'verbose_name': 'номер карты',
                'verbose_name_plural': 'номера карт',
            },
        ),
        migrations.CreateModel(
            name='PaymentStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.CharField(max_length=5, verbose_name='код статуса')),
                ('status_description', models.CharField(max_length=100, verbose_name='описание статуса')),
            ],
            options={
                'verbose_name': 'статус оплаты',
                'verbose_name_plural': 'статусы оплаты',
            },
        ),
    ]
