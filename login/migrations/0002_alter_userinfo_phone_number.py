# Generated by Django 4.0.2 on 2022-03-31 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phone_number',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
