# Generated by Django 4.0.1 on 2022-03-06 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_alltheme_save_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('musics', models.ManyToManyField(blank=True, null=True, related_name='musics_playlist', to='home.Music')),
            ],
        ),
    ]
