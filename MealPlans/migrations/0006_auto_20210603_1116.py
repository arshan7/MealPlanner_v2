# Generated by Django 3.2.3 on 2021-06-03 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealPlans', '0005_mealplans_default_day'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodgroup',
            options={'ordering': ['time', 'order', 'preset']},
        ),
        migrations.AlterModelOptions(
            name='preset',
            options={'ordering': ['time', 'order', 'presets']},
        ),
    ]