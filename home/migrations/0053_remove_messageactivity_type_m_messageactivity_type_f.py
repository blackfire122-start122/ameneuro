# Generated by Django 4.0.1 on 2022-03-10 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_remove_messageactivity_id_media_messageactivity_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageactivity',
            name='type_m',
        ),
        migrations.AddField(
            model_name='messageactivity',
            name='type_f',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_file_ma', to='home.typefile'),
        ),
    ]
