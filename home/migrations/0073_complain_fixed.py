# Generated by Django 4.0.1 on 2022-06-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0072_complain'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='fixed',
            field=models.BooleanField(default=False),
        ),
    ]