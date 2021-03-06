# Generated by Django 3.0.7 on 2020-07-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0008_auto_20200708_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='images/avatars/default_avatar.png', upload_to='images/avatars/', verbose_name='аватар'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='displayed',
            field=models.CharField(max_length=40, unique=True, verbose_name='Отоброжаемое имя'),
        ),
    ]
