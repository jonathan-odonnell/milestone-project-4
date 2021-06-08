# Generated by Django 3.1.3 on 2021-06-08 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_flight_origin_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='direction',
            field=models.CharField(choices=[('', ''), ('Outbound', 'Outbound'), ('Return', 'Return')], max_length=50),
        ),
    ]
