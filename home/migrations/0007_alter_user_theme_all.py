# Generated by Django 4.0.1 on 2022-02-01 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_user_theme_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='theme_all',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_all_user', to='home.alltheme'),
        ),
    ]
