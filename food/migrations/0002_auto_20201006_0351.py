# Generated by Django 3.1 on 2020-10-06 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='without_fork',
            field=models.BooleanField(default=False),
        ),
    ]