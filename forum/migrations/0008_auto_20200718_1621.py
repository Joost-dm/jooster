# Generated by Django 3.0.7 on 2020-07-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20200704_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='like',
            field=models.BooleanField(default=True, verbose_name='Нравится'),
        ),
        migrations.AddField(
            model_name='threadlike',
            name='like',
            field=models.BooleanField(default=True, verbose_name='Нравится'),
        ),
    ]
