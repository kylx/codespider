# Generated by Django 2.1.7 on 2019-03-26 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190326_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='diagnosis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Diagnosis'),
        ),
    ]