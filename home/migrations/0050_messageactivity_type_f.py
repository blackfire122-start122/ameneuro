# Generated by Django 4.0.1 on 2022-03-10 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_messageactivity_from_user_alter_messageactivity_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageactivity',
            name='type_f',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_file_ma', to='home.typefile'),
        ),
    ]
