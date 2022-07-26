# Generated by Django 4.0.2 on 2022-04-05 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyManage', '0003_alter_individual_property_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual_property',
            name='myFile',
        ),
        migrations.AddField(
            model_name='individual_property',
            name='fileName',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='individual_property',
            name='backup',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='individual_property',
            name='encryption',
            field=models.BooleanField(null=True),
        ),
    ]
