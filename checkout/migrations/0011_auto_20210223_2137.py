# Generated by Django 3.1.4 on 2021-02-23 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_auto_20210223_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bookingpassenger',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_passengers', to='checkout.booking'),
        ),
    ]