# Generated by Django 3.1.4 on 2021-03-24 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0005_auto_20210324_0059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['id'], 'verbose_name_plural': 'Activities'},
        ),
        migrations.AlterModelOptions(
            name='itinerary',
            options={'ordering': ['day'], 'verbose_name_plural': 'Itineraries'},
        ),
        migrations.AlterModelOptions(
            name='package',
            options={'ordering': ['id']},
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='activity',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='itinerary',
            old_name='title',
            new_name='name',
        ),
    ]
