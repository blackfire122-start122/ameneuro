# Generated by Django 4.0.1 on 2022-05-01 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0069_music_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='close_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/close_img'),
        ),
    ]
