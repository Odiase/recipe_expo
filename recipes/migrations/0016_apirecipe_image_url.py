# Generated by Django 3.2.9 on 2022-07-03 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20220625_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirecipe',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
