# Generated by Django 3.2.1 on 2021-07-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PocModel', '0003_poc_isuse'),
    ]

    operations = [
        migrations.AddField(
            model_name='poc',
            name='cmd',
            field=models.CharField(default='', max_length=50),
        ),
    ]
