# Generated by Django 4.0.1 on 2022-04-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0057_video_preview_alter_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='preview',
            field=models.ImageField(default=None, upload_to='videos_preview'),
        ),
    ]
