# Generated by Django 3.2.12 on 2023-03-06 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0024_alter_characteristic_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristic',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='market_app.characteristicsgroup', verbose_name='группа характеристик'),
            preserve_default=False,
        ),
    ]
