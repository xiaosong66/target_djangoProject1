# Generated by Django 4.0.2 on 2022-04-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_userinfo_common_login_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='login_failure',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
