# Generated by Django 2.2.2 on 2020-03-16 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_auto_20200316_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='companyLogo',
            field=models.ImageField(default='company_logo/buggie.png', upload_to='company_logo'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='image',
            field=models.ImageField(default='profile_image/person.png', upload_to='profile_image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='profile_image/person.png', upload_to='profile_image'),
        ),
    ]