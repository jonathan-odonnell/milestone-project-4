# Generated by Django 3.1.4 on 2021-02-22 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0013_package_extras'),
        ('extras', '0001_initial'),
        ('checkout', '0008_booking_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
            ],
        ),
        migrations.CreateModel('BookingPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.IntegerField()),
                ('departure_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='BookingPassengers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('passport_number', models.CharField(max_length=9)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='paid',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='paypal_pid',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='booking',
            name='county',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='booking',
            name='postcode',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='PackageBooking',
        ),
        migrations.AddField(
            model_name='bookingpassengers',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking_passengers', to='checkout.booking'),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking_package', to='checkout.booking'),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='outbound_flight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_outbound_flight', to='holidays.flight'),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='holidays.package'),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='return_flight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_inbound_flight', to='holidays.flight'),
        ),
        migrations.AddField(
            model_name='bookingextra',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking_extras', to='checkout.booking'),
        ),
        migrations.AddField(
            model_name='bookingextra',
            name='extra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extras.extra'),
        ),
    ]
