# Generated by Django 3.1.4 on 2021-01-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0010_auto_20210130_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='arrival_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_time',
            field=models.DateTimeField(),
        ),
    ]
