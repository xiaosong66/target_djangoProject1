# Generated by Django 4.0.4 on 2022-05-27 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskWarning', '0005_riskvalue_if_solve'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskvalue',
            name='securityScore',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
    ]