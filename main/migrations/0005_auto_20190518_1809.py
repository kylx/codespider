# Generated by Django 2.1.7 on 2019-05-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190518_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.TextField(),
        ),
    ]
