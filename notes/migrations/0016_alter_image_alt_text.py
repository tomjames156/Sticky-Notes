# Generated by Django 4.1.7 on 2023-03-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0015_alter_image_alt_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='alt_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]