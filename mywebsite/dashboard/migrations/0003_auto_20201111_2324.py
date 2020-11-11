# Generated by Django 3.1.1 on 2020-11-11 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20201111_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardsetting',
            name='store_currency',
            field=models.CharField(choices=[('eur', 'Eur'), ('dollars', 'Dollars')], default='eur', max_length=10),
        ),
    ]