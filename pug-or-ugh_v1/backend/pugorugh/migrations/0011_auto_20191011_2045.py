# Generated by Django 2.1.5 on 2019-10-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0010_auto_20191011_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'liked'), ('d', 'disliked')], default='undecided', max_length=1),
        ),
    ]