# Generated by Django 2.1.2 on 2018-12-19 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comsearch', '0012_auto_20181218_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cominfo',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='cominfo',
            table='imformation',
        ),
    ]