# Generated by Django 4.0.4 on 2022-05-18 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_alter_userinfo_loginfailure_days_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='password',
            new_name='second_password',
        ),
    ]
