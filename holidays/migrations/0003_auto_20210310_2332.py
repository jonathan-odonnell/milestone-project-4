# Generated by Django 3.1.4 on 2021-03-10 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0002_auto_20210310_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='category',
            new_name='categories',
        ),
    ]
