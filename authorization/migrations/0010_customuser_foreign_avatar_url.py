# Generated by Django 3.0.7 on 2020-07-27 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0009_auto_20200708_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='foreign_avatar_url',
            field=models.FilePathField(null=True),
        ),
    ]
