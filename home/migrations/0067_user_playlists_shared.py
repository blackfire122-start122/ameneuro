# Generated by Django 4.0.1 on 2022-04-25 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_remove_chat_friend_chat_chat_friend_alter_chat_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='playlists_shared',
            field=models.ManyToManyField(blank=True, null=True, related_name='playlists_shared_user', to='home.Playlist'),
        ),
    ]
