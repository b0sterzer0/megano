# Generated by Django 3.2.12 on 2022-10-21 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compare_app', '0003_auto_20221020_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparemodel',
            name='type_for_compare',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='compare_app.testgoodtypemodel', verbose_name='категория товаров для сравнения'),
        ),
    ]
