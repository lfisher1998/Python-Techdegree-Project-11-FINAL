# Generated by Django 2.1.5 on 2019-10-11 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0008_auto_20191011_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'liked'), ('d', 'disliked')], default='', max_length=1, null=True),
        ),
    ]
