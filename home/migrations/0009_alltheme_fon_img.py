# Generated by Django 4.0.1 on 2022-02-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_user_theme_all'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltheme',
            name='fon_img',
            field=models.ImageField(null=True, upload_to='theme_all'),
        ),
    ]
