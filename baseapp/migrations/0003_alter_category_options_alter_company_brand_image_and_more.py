# Generated by Django 4.0.6 on 2022-07-23 20:19

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_company_google_map_company_website_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='company',
            name='brand_image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image/logo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='google_map',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(max_length=255),
        ),
    ]
