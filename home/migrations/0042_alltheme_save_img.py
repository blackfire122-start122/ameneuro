# Generated by Django 4.0.1 on 2022-02-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_user_saves_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='save_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/save_img'),
        ),
    ]
