# Generated by Django 3.2.9 on 2022-06-18 22:03

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20220616_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='jpeg', keep_meta=True, quality=100, size=[600, 600], upload_to='uploads/recipe_images'),
        ),
    ]
