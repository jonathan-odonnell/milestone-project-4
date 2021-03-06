# Generated by Django 3.1.4 on 2021-03-06 23:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('town_or_city', models.CharField(blank=True, max_length=40, null=True)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=254, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
