# Generated by Django 4.0.2 on 2022-04-27 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskWarning', '0004_riskvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskvalue',
            name='if_solve',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
