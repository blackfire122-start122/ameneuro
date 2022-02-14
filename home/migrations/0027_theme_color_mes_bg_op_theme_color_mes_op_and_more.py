# Generated by Django 4.0.1 on 2022-02-13 13:31

import colorful.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_typefile_message_type_file_alter_post_type_p_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='color_mes_bg_op',
            field=models.FloatField(default=1, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AddField(
            model_name='theme',
            name='color_mes_op',
            field=models.FloatField(default=1, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='theme',
            name='color_mes',
            field=colorful.fields.RGBColorField(null=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='color_mes_bg',
            field=colorful.fields.RGBColorField(null=True),
        ),
    ]