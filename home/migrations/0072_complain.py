# Generated by Django 4.0.1 on 2022-06-05 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0071_alltheme_turn_over_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autor_complain', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
