from django.db import models
from bases.models import *


# 进度表
class Schedule(models.Model):
    code = models.CharField('项目编号', max_length=64)
    name = models.CharField('项目名称', max_length=64)
    unit = models.ForeignKey('Unit', on_delete=models.PROTECT, verbose_name='单位')
    invnum = models.DecimalField('清单数量', max_digits=13, decimal_places=3)
    invprice = models.DecimalField('清单单价', max_digits=13, decimal_places=2)
    changenum = models.DecimalField('工程变更增减数量', max_digits=13, decimal_places=3)
    changeprice = models.DecimalField('工程变更增减单价', max_digits=13, decimal_places=2)

    def invmoney(self):
        return format(self.invnum * self.invprice, '0,.2f')

    invmoney.short_description = '清单金额'  # admin中要设置为只读

    def changemoney(self):
        return format(self.changenum * self.changeprice, '0,.2f')

    changemoney.short_description = '工程变更增减金额'


# 合同
class Contract(models.Model):
    name = models.CharField('合同名称', max_length=64)
    content = models.CharField('合同内容', max_length=64)
    contact = models.CharField('合作联系人', max_length=64)
    telphone = models.CharField('合作人电话', max_length=64)
    price = models.DecimalField('合同单价', max_digits=13, decimal_places=2)
    money = models.DecimalField('合同总价', max_digits=13, decimal_places=2)
    status = models.SmallIntegerField('完成状态', choices=contract_choices, default=0)

    class Meta:
        verbose_name_plural = verbose_name = '合同'

    def __str__(self):
        return self.name


# 合同支付
class ContractPay(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, verbose_name='合同')
    date = models.DateField('日期')
    money = models.DecimalField('支付金额', max_digits=13, decimal_places=2)

    class Meta:
        verbose_name_plural = verbose_name = '合同支付'

    def __str__(self):
        return self.contract


# 材料图算量
class Budget(models.Model):
    material = models.ForeignKey('Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('图算量', max_digits=13, decimal_places=3)
    money = models.DecimalField('图算金额', max_digits=13, decimal_places=2)

    class Meta:
        verbose_name_plural = verbose_name = '材料图算量'

    def __str__(self):
        return self.material


# 材料入库
class MaterialInRecord(models.Model):
    material = models.ForeignKey('Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)
    money = models.DecimalField('金额', max_digits=13, decimal_places=2)
    docdate = models.DateField('日期')

    class Meta:
        verbose_name_plural = verbose_name = '材料入库'

    def __str__(self):
        return self.material


# 材料出库
class MaterialOutRecord(models.Model):
    material = models.ForeignKey('Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)
    money = models.DecimalField('金额', max_digits=13, decimal_places=2)
    docdate = models.DateField('日期')

    class Meta:
        verbose_name_plural = verbose_name = '材料出库'

    def __str__(self):
        return self.material
