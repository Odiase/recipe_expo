# Generated by Django 3.2.9 on 2022-06-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20220616_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('Dessert', 'Dessert'), ('Drinks', 'Drinks'), ('Healthy and Tasty', 'Healthy and Tasty'), ('Native', 'Native'), ('Pastries', 'Pastries'), ('Soup', 'Soup'), ('Veggies', 'Veggies')], max_length=20),
        ),
    ]
