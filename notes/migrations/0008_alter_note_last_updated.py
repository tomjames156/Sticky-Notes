# Generated by Django 4.1.7 on 2023-03-05 08:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_note_note_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 5, 8, 16, 18, 683856, tzinfo=datetime.timezone.utc)),
        ),
    ]
