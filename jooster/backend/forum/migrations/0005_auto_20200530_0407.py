# Generated by Django 3.0.5 on 2020-05-30 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20200530_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='postviewer',
            name='counter',
            field=models.SmallIntegerField(default=0, verbose_name='Счетчик просмотров'),
        ),
        migrations.AddField(
            model_name='threadviewer',
            name='counter',
            field=models.SmallIntegerField(default=0, verbose_name='Счетчик просмотров'),
        ),
    ]
