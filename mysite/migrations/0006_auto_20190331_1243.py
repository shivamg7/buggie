# Generated by Django 2.1.7 on 2019-03-31 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_auto_20190331_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='postedOn',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 31, 12, 43, 5, 541471)),
        ),
    ]
