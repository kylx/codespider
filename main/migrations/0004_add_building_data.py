# Generated by Django 2.1.7 on 2019-04-09 15:07

from django.db import migrations

def create_buildings(apps, schema_editor):
    b = apps.get_model('main', 'Building')
    b(name='main').save()
    b(name='annex').save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_add_sample_data'),
    ]

    operations = [
        migrations.RunPython(create_buildings),
    ]