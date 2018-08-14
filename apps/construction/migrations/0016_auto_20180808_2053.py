# Generated by Django 2.0.7 on 2018-08-08 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('construction', '0015_auto_20180808_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeasePay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('金额', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('日期', models.DateField()),
                ('制单人', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '租赁支付',
                'verbose_name_plural': '租赁支付',
            },
        ),
        migrations.RemoveField(
            model_name='leaseclosebill',
            name='累计结算金额',
        ),
        migrations.AlterField(
            model_name='leaseout',
            name='租赁日期',
            field=models.DateField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='leasepay',
            name='结算单',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='construction.LeaseCloseBill'),
        ),
    ]