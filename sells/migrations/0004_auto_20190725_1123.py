# Generated by Django 2.0.3 on 2019-07-25 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sells', '0003_auto_20190723_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesproduct',
            name='discription',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discription',
            field=models.TextField(blank=True),
        ),
    ]
