# Generated by Django 4.0.1 on 2022-02-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_alter_typefile_type_f_magic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typefile',
            name='type_f_magic',
            field=models.TextField(null=True),
        ),
    ]