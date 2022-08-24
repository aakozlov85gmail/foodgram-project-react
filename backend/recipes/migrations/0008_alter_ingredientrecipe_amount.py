# Generated by Django 3.2.15 on 2022-08-24 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20220823_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.001, message='Ингредиентов должно быть больше нуля')], verbose_name='Количество'),
        ),
    ]
