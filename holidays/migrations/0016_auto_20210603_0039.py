# Generated by Django 3.1.3 on 2021-06-02 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0015_auto_20210517_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]
