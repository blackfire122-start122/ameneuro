# Generated by Django 4.0.1 on 2022-02-01 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alltheme_text_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='coment_img',
            field=models.ImageField(default='', null=True, upload_to='theme_all/comment_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='like_img',
            field=models.ImageField(default='', null=True, upload_to='theme_all/like_imgs'),
        ),
        migrations.AlterField(
            model_name='alltheme',
            name='fon_img',
            field=models.ImageField(null=True, upload_to='theme_all/fon_imgs'),
        ),
    ]