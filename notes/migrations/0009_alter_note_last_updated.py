# Generated by Django 4.1.7 on 2023-03-05 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_alter_note_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]