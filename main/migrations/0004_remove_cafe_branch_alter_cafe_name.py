# Generated by Django 5.1.3 on 2024-11-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_cafe_is_open'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='branch',
        ),
        migrations.AlterField(
            model_name='cafe',
            name='name',
            field=models.CharField(max_length=300),
        ),
    ]
