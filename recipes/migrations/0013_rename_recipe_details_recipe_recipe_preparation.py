# Generated by Django 3.2.9 on 2022-06-19 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_alter_recipe_recipe_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='recipe_details',
            new_name='recipe_preparation',
        ),
    ]