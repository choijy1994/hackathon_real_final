# Generated by Django 2.2.3 on 2019-08-01 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagemodel',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
