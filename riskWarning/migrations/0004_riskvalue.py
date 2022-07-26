# Generated by Django 4.0.2 on 2022-04-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskWarning', '0003_remove_userrisk_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='riskValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, null=True)),
                ('riskType', models.CharField(max_length=20, null=True)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('riskDescribe', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
