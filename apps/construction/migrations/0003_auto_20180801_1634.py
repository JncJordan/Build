# Generated by Django 2.0.7 on 2018-08-01 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_auto_20180801_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractpay',
            name='制单人',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
