# Generated by Django 2.1.2 on 2018-12-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comsearch', '0013_auto_20181219_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queryuser',
            name='condition',
            field=models.CharField(choices=[('name', '公司名称'), ('num', '公司注册号'), ('code', '组织机构代码'), ('style', '公司类型'), ('lawperson', '公司法人')], max_length=20),
        ),
    ]
