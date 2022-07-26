# Generated by Django 4.0.2 on 2022-03-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='individual_property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=20)),
                ('fileName', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=10, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('describe', models.CharField(max_length=500, null=True)),
                ('backup', models.BooleanField()),
                ('encryption', models.BooleanField()),
                ('myFile', models.FileField(null=True, upload_to='picture')),
            ],
        ),
    ]