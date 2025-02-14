# Generated by Django 2.0.3 on 2019-07-22 12:27

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sells', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('brand_name', models.CharField(blank=True, max_length=150)),
                ('product_model_number', models.CharField(blank=True, max_length=100)),
                ('product_color', models.CharField(blank=True, max_length=50)),
                ('available_quantity', models.IntegerField(default=1)),
                ('total_quantity', models.IntegerField(default=1)),
                ('unit_price', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('discription', ckeditor.fields.RichTextField(blank=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductCat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='SalesProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('sale_quantity', models.IntegerField(default=1)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sells.Product')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sells.Registration')),
            ],
            options={
                'verbose_name': 'Sale Product',
                'verbose_name_plural': 'Sales Products',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sells.ProductCat'),
        ),
    ]
