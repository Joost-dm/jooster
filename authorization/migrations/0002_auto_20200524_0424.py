# Generated by Django 3.0.5 on 2020-05-24 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
