# Generated by Django 4.0.1 on 2022-02-13 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_theme_color_mes_bg_op_theme_color_mes_op_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='color_mes_op',
        ),
    ]
