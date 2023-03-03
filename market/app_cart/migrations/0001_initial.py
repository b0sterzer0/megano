# Generated by Django 3.2.12 on 2023-02-20 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market_app', '0005_auto_20230206_2058'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_added', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=0, verbose_name='Количество товаров в корзине')),
                ('price', models.FloatField(default=None, verbose_name='Цена за товар')),
                ('products', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Товары', to='market_app.product', verbose_name='Товары в корзине')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User cart')),
            ],
            options={
                'verbose_name': 'Покупательская корзина',
                'verbose_name_plural': 'Покупательские корзины',
                'ordering': ['item_added'],
            },
        ),
    ]
