# Generated by Django 2.1.2 on 2018-11-06 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comsearch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='c_code',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
