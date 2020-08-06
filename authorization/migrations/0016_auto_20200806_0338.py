# Generated by Django 3.0.7 on 2020-08-06 00:38

import authorization.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0015_auto_20200730_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=authorization.models.generate_avatar_path, verbose_name='аватар'),
        ),
    ]
