# Generated by Django 2.0.3 on 2019-07-30 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sells', '0007_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.FloatField(blank=True, default=0, verbose_name='Maximum Discount'),
        ),
    ]
