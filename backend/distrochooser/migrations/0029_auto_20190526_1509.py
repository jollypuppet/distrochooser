# Generated by Django 2.1.2 on 2019-05-26 13:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0028_auto_20190526_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerdistributionmatrix',
            name='isNeutralHit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 26, 15, 9, 7, 22214)),
        ),
    ]
