# Generated by Django 5.0.7 on 2024-07-20 14:23

import media_files.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_files', '0002_alter_thumbnail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='image',
            field=models.ImageField(null=True, upload_to='media/thumbnails/', validators=[media_files.models.validate_image_file]),
        ),
    ]
