# Generated by Django 3.2.19 on 2023-05-31 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='if_staff',
            new_name='is_staff',
        ),
    ]