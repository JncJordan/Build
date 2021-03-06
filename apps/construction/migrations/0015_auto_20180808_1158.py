# Generated by Django 2.0.7 on 2018-08-08 11:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('construction', '0014_auto_20180808_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaseCloseBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('结算单号', models.CharField(max_length=64)),
                ('结算金额', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('累计结算金额', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('支付金额', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('欠款金额', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('备注', models.CharField(blank=True, max_length=256, null=True)),
                ('日期', models.DateField()),
                ('制单人', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('租赁单', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='construction.LeaseStock')),
            ],
            options={
                'verbose_name': '租赁结算',
                'verbose_name_plural': '租赁结算',
            },
        ),
        migrations.AddField(
            model_name='leaseout',
            name='单价',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=13),
        ),
        migrations.AddField(
            model_name='leaseout',
            name='租赁日期',
            field=models.DateField(default=datetime.date(2018, 8, 8), editable=False),
        ),
        migrations.AddField(
            model_name='leaseout',
            name='金额',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=13),
        ),
    ]
