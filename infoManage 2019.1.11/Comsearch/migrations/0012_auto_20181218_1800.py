# Generated by Django 2.1.2 on 2018-12-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comsearch', '0011_auto_20181218_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cominfo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
