# Generated by Django 3.0 on 2021-01-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.IntegerField(default=0),
        ),
    ]
