# Generated by Django 2.0.3 on 2019-07-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=80)),
                ('mobile', models.CharField(blank=True, max_length=16, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('reg_date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registrations',
            },
        ),
    ]
