# Generated by Django 2.1.7 on 2019-04-01 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_voted'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='voted',
            new_name='vote',
        ),
    ]