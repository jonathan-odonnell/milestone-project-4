# Generated by Django 3.1.4 on 2021-01-30 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0009_auto_20210130_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='duration',
            field=models.DurationField(),
        ),
    ]
