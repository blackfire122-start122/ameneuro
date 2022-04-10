# Generated by Django 4.0.1 on 2022-04-07 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_alltheme_add_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('date', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='posts')),
                ('description', models.TextField(blank=True, null=True)),
                ('comments', models.ManyToManyField(blank=True, null=True, to='home.Comment')),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='likes_video', to=settings.AUTH_USER_MODEL)),
                ('user_pub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_pub_video', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
