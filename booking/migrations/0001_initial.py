# Generated by Django 3.1.4 on 2021-03-06 23:20

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('holidays', '0001_initial'),
        ('flights', '0001_initial'),
        ('profiles', '__first__'),
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_number', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('town_or_city', models.CharField(default='', max_length=40)),
                ('street_address1', models.CharField(default='', max_length=80)),
                ('street_address2', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('county', models.CharField(default='', max_length=80)),
                ('country', django_countries.fields.CountryField(default='', max_length=2)),
                ('postcode', models.CharField(default='', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.CharField(blank=True, max_length=20, null=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('paid', models.BooleanField(default=False, editable=False)),
                ('stripe_pid', models.CharField(default='', max_length=254)),
                ('paypal_pid', models.CharField(default='', max_length=254)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='BookingPassenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('passport_number', models.CharField(max_length=9)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_passengers', to='booking.booking')),
            ],
        ),
        migrations.CreateModel(
            name='BookingPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.IntegerField()),
                ('departure_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking_package', to='booking.booking')),
                ('outbound_flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_outbound_flight', to='flights.flight')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='holidays.package')),
                ('return_flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_inbound_flight', to='flights.flight')),
            ],
        ),
        migrations.CreateModel(
            name='BookingExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_extras', to='booking.booking')),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extras.extra')),
            ],
        ),
    ]
