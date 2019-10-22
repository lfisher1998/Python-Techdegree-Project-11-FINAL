# Generated by Django 2.1.5 on 2019-10-18 05:02

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0016_auto_20191016_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('b', 'Baby'), ('y', 'Young'), ('a', 'Adult'), ('s', 'Senior')], max_length=7),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=5),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=10),
        ),
    ]