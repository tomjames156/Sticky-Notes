# Generated by Django 4.1.7 on 2023-04-13 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0023_alter_note_login_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='login_details',
        ),
        migrations.DeleteModel(
            name='LoginDetails',
        ),
    ]
