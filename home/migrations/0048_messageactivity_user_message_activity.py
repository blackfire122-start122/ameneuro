# Generated by Django 4.0.1 on 2022-03-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_alter_playlist_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='message_file')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('readeble', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='message_activity',
            field=models.ManyToManyField(blank=True, null=True, related_name='message_activity', to='home.MessageActivity'),
        ),
    ]
