# Generated by Django 2.1.5 on 2019-10-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0017_auto_20191018_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(max_length=15),
        ),
    ]
