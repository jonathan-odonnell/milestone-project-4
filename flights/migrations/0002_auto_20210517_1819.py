# Generated by Django 3.1.4 on 2021-05-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ('flight_number',)},
        ),
        migrations.AddField(
            model_name='flight',
            name='direction',
            field=models.CharField(choices=[('', 'Direction'), ('Outbound', 'Outbound'), ('Return', 'Return')], default='Outbound', max_length=50),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='name',
            new_name='flight_number',
        ),
        migrations.AlterField(
            model_name='flight',
            name='destination',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='flight',
            name='layover',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='origin',
            field=models.CharField(max_length=50),
        ),
    ]
