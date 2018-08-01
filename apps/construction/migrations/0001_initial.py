# Generated by Django 2.0.7 on 2018-08-01 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('合同名称', models.CharField(max_length=64)),
                ('合同内容', models.CharField(max_length=64)),
                ('合作联系人', models.CharField(max_length=64)),
                ('合作人电话', models.CharField(max_length=64)),
                ('合同单价', models.DecimalField(decimal_places=2, max_digits=13)),
                ('合同总价', models.DecimalField(decimal_places=2, max_digits=13)),
                ('完成状态', models.SmallIntegerField(choices=[(0, '未完成'), (1, '已完成')], default=0)),
                ('日期', models.DateField(auto_now=True)),
                ('已支付金额', models.DecimalField(decimal_places=2, max_digits=13)),
                ('剩余金额', models.DecimalField(decimal_places=2, max_digits=13)),
                ('制单人', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '合同',
                'verbose_name': '合同',
            },
        ),
        migrations.CreateModel(
            name='ContractPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('单号', models.CharField(max_length=64)),
                ('日期', models.DateField()),
                ('支付金额', models.DecimalField(decimal_places=2, max_digits=13)),
                ('制单人', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('合同', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.Contract')),
            ],
            options={
                'verbose_name_plural': '合同支付',
                'verbose_name': '合同支付',
            },
        ),
    ]