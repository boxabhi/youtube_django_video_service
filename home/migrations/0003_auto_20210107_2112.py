# Generated by Django 2.2.6 on 2021-01-07 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210107_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
