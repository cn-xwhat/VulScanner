# Generated by Django 3.2.1 on 2021-07-11 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScanTaskModel', '0009_scantask_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scantask',
            name='ip_range',
            field=models.CharField(default='', max_length=100),
        ),
    ]
