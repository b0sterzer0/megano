# Generated by Django 3.2.12 on 2022-10-12 07:40

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
            name='TestBasketModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TestOrderDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_detail', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TestSaleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_info', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TestUserProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_info', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestOrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='perms_app.testbasketmodel')),
                ('order_detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='perms_app.testorderdetailmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestGoodProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_info', models.CharField(max_length=10)),
                ('sale', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='perms_app.testsalemodel')),
            ],
        ),
        migrations.CreateModel(
            name='TestGoodModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_name', models.CharField(max_length=10)),
                ('good_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='perms_app.testgoodprofilemodel')),
            ],
        ),
    ]