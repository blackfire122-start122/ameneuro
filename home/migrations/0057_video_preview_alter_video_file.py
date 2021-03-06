# Generated by Django 4.0.1 on 2022-04-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_alter_video_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='preview',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='videos_preview'),
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to='videos'),
        ),
    ]
