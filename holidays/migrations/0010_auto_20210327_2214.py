# Generated by Django 3.1.4 on 2021-03-27 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0009_auto_20210327_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itinerary',
            options={'ordering': ('id',), 'verbose_name_plural': 'Itineraries'},
        ),
    ]
