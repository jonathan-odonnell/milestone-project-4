# Generated by Django 3.1.4 on 2021-03-31 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0011_auto_20210331_2314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ('id',)},
        ),
    ]