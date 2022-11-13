from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog_categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='заголовок')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('image', models.ImageField(upload_to='images/banners', verbose_name='изображение')),
                ('image_alt', models.CharField(max_length=100, verbose_name='подсказка')),
                ('link', models.CharField(max_length=300, verbose_name='url')),
            ],
            options={
                'verbose_name': 'баннер',
                'verbose_name_plural': 'баннеры',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog_categories.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='market_app.product', verbose_name='Отзывы товаров')),
            ],
            options={
                'verbose_name': 'Комментарии',
                'verbose_name_plural': 'Комментарий',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market_app.product', verbose_name='Товар')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market_app.seller', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Товар-продавец',
                'verbose_name_plural': 'Товар-продавец',
            },
        ),
        migrations.CreateModel(
            name='ProductReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product_reviews/%Y/%m/%d', verbose_name='Картинка')),
                ('image_alt', models.CharField(default='Фото к отзыву', max_length=100, verbose_name='подсказка')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='market_app.productreview')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products/%Y/%m/%d', verbose_name='Картинка')),
                ('image_alt', models.CharField(default='Фото к отзыву', max_length=100, verbose_name='подсказка')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='market_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ManyToManyField(related_name='products', through='market_app.SellerProduct', to='market_app.Seller', verbose_name='Продавец'),
        ),
    ]
