# Generated by Django 4.0.1 on 2022-02-01 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_alltheme_fon_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme_all',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_all_user', to='home.alltheme'),
        ),
    ]
