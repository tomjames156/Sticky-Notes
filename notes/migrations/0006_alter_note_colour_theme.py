# Generated by Django 4.1.7 on 2023-02-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_note_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='colour_theme',
            field=models.CharField(choices=[('yellow-theme', 'yellow'), ('green-theme', 'green'), ('pink-theme', 'pink'), ('purple-theme', 'purple'), ('blue-theme', 'blue'), ('gray-theme', 'gray'), ('charcoal-theme', 'charcoal')], default='yellow-theme', max_length=19),
        ),
    ]