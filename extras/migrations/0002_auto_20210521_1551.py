# Generated by Django 3.1.4 on 2021-05-21 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extra',
            options={'ordering': ('id',)},
        ),
    ]
