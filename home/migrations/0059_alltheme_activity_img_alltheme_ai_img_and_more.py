# Generated by Django 4.0.1 on 2022-04-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0058_alter_video_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='activity_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/activity_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='ai_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/ai_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='chats_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/chats_img'),
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
            name='friends_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/friends_img'),
        ),
        migrations.AddField(
            model_name='alltheme',
            name='menu_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/menu_img'),
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
            name='settings_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='theme_all/settings_img'),
        ),
    ]
