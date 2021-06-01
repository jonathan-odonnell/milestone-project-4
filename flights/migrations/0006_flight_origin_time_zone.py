# Generated by Django 3.1.3 on 2021-06-01 19:47

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_flight_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='origin_time_zone',
            field=timezone_field.fields.TimeZoneField(default='Europe/London'),
            preserve_default=False,
        ),
    ]
