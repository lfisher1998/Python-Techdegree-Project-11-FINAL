# Generated by Django 2.1.5 on 2019-10-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0013_auto_20191011_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='age',
            field=models.IntegerField(),
        ),
    ]