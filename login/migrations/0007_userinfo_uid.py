# Generated by Django 4.0.2 on 2022-04-19 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_userinfo_loginfailure_days_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='uid',
            field=models.CharField(max_length=128, null=True),
        ),
    ]