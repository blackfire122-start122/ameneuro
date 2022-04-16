# Generated by Django 4.0.1 on 2022-04-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_remove_alltheme_back_img_remove_alltheme_chats_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='back_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/back_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='chats_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/chats_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='comment_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/comment_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='file_send_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/file_send_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='find_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/find_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='fon_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/fon_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='friends_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/friends_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='like_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/like_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='menu_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/menu_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='music_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/music_imgs'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='music_share_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/music_share_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='no_media_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/no_media_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='options_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/options_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='pause_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/pause_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='play_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/play_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='play_in_all_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/play_in_all_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='save_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/save_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='settings_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/settings_img'),
        ),
    ]