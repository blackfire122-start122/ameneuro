# Generated by Django 4.0.5 on 2022-06-20 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0078_alter_message_emoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_file_mes', to='home.typefile'),
        ),
    ]
