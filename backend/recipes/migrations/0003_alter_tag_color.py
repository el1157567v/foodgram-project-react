# Generated by Django 3.2.3 on 2023-07-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=50, unique=True, verbose_name='Цвет в HEX'),
        ),
    ]
