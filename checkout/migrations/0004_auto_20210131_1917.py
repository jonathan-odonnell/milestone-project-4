# Generated by Django 3.1.4 on 2021-01-31 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210131_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagebooking',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='package_bookings', to='checkout.booking'),
        ),
    ]
