# Generated by Django 2.0.7 on 2018-07-24 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bases', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='材料',
            new_name='Material',
        ),
        migrations.RenameModel(
            old_name='单位',
            new_name='Unit',
        ),
    ]
