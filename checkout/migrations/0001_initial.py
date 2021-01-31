# Generated by Django 3.1.4 on 2021-01-30 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('holidays', '0012_remove_flight_layover_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_number', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=40)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('street_address1', models.CharField(max_length=80)),
                ('street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.CharField(blank=True, max_length=20, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PackageBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.IntegerField()),
                ('departure_date', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('package_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('Package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='holidays.package')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_booking', to='checkout.booking')),
            ],
        ),
    ]