# Generated by Django 4.0.1 on 2022-02-11 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_remove_typemes_data_m'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_f', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='type_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_file_mes', to='home.typefile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='type_p',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_file_post', to='home.typefile'),
        ),
        migrations.DeleteModel(
            name='TypePost',
        ),
    ]
