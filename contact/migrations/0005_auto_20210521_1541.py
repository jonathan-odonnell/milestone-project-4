# Generated by Django 3.1.4 on 2021-05-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20210509_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(choices=[('', 'Subject'), ('Holiday Information', 'Holiday Information'), ('Offers', 'Offers'), ('Bookings', 'Bookings'), ('General Enquiries', 'General Enquiries'), ('Other', 'Other')], max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
