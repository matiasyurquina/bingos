# Generated by Django 4.2.3 on 2023-08-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicidad',
            name='imagen',
            field=models.ImageField(upload_to=''),
        ),
    ]