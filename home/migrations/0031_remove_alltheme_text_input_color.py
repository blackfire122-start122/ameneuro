# Generated by Django 4.0.1 on 2022-02-14 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_alltheme_text_input_color_alter_alltheme_back_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alltheme',
            name='text_input_color',
        ),
    ]