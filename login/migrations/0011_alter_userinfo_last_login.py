# Generated by Django 4.0.2 on 2022-04-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_userinfo_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
    ]