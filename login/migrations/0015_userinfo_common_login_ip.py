# Generated by Django 4.0.4 on 2022-05-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_rename_password_userinfo_second_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='common_login_ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
