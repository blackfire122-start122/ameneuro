# Generated by Django 4.0.1 on 2022-02-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_alltheme_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alltheme',
            name='back_img',
            field=models.ImageField(default=None, null=True, upload_to='theme_all/back_imgs'),
        ),
        migrations.AlterField(
            model_name='alltheme',
            name='comment_img',
            field=models.ImageField(default=None, null=True, upload_to='theme_all/comment_imgs'),
        ),
        migrations.AlterField(
            model_name='alltheme',
            name='like_img',
            field=models.ImageField(default=None, null=True, upload_to='theme_all/like_imgs'),
        ),
    ]
