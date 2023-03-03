# Generated by Django 3.2.12 on 2023-02-06 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_login', '0001_initial'),
        ('market_app', '0004_auto_20230111_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name': 'комментарии', 'verbose_name_plural': 'комментарий'},
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={'verbose_name': 'продавец', 'verbose_name_plural': 'продавцы'},
        ),
        migrations.AlterModelOptions(
            name='sellerproduct',
            options={'verbose_name': 'товар-продавец', 'verbose_name_plural': 'товар-продавец'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='market_app.category', verbose_name='категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ManyToManyField(related_name='products', through='market_app.SellerProduct', to='market_app.Seller', verbose_name='продавец'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='images/products/%Y/%m/%d', verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='покупатель'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='market_app.product', verbose_name='отзывы товаров'),
        ),
        migrations.AlterField(
            model_name='productreviewimage',
            name='image',
            field=models.ImageField(upload_to='images/product_reviews/%Y/%m/%d', verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='description',
            field=models.TextField(blank=True, max_length=2000, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(max_length=200, verbose_name='название магазина'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to='app_login.profile', verbose_name='профиль'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market_app.product', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='qty',
            field=models.PositiveIntegerField(verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market_app.seller', verbose_name='продавец'),
        ),
    ]
