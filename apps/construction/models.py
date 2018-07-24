from django.contrib.auth.models import User
import datetime
from bases.models import *


# 工程进度表
class JobSchedule(models.Model):
    location = models.CharField('单项工程位置', max_length=64)
    code = models.CharField('项目编号', max_length=64)
    name = models.CharField('项目名称', max_length=64)
    unit = models.ForeignKey('bases.Unit', on_delete=models.PROTECT, verbose_name='单位')
    invnum = models.DecimalField('清单数量', max_digits=13, decimal_places=3, default=0)
    invprice = models.DecimalField('清单单价', max_digits=13, decimal_places=2, default=0)
    changenum = models.DecimalField('工程变更增减数量', max_digits=13, decimal_places=3, default=0)
    changeprice = models.DecimalField('工程变更增减单价', max_digits=13, decimal_places=2, default=0)

    def invmoney(self):
        return format(self.invnum * self.invprice, '0,.2f')

    def changemoney(self):
        return format(self.changenum * self.changeprice, '0,.2f')

    def nownum(self):
        return format(self.invnum + self.changenum, '0.3f')

    def nowmoney(self):
        return format(self.invmoney() + self.changemoney(), '0,.2f')

    invmoney.short_description = '清单金额'  # admin中要设置为只读
    changemoney.short_description = '工程变更增减金额'
    nownum.short_description = '变更后数量'
    nowmoney.short_description = '变更后金额'
    thisweekcomplatenum = models.DecimalField('到本期末累计完成数量', max_digits=13, decimal_places=3, default=0)
    thisweekcomplatemoney = models.DecimalField('到本期末累计完成金额', max_digits=13, decimal_places=2, default=0)
    lastweekcomplatenum = models.DecimalField('到上期末累计完成数量', max_digits=13, decimal_places=3, default=0)
    lastweekcomplatemoney = models.DecimalField('到上期末累计完成金额', max_digits=13, decimal_places=2, default=0)
    thiscomplatenum = models.DecimalField('本期完成数量', max_digits=13, decimal_places=3, default=0)
    thiscomplatemoney = models.DecimalField('本期完成金额', max_digits=13, decimal_places=2, default=0)

    def complatedratio(self):
        return '{:0.2f}%'.format(self.thisweekcomplatenum / self.invnum * 200)

    complatedratio.short_description = '已完成百分比'
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '工程进度表'

    def __str__(self):
        return self.location + ' ' + self.code + ' ' + self.name


# 计量进度表
class MeasuringSchedule(models.Model):
    location = models.CharField('单项工程位置', max_length=64)
    code = models.CharField('项目编号', max_length=64)
    name = models.CharField('项目名称', max_length=64)
    unit = models.ForeignKey('bases.Unit', on_delete=models.PROTECT, verbose_name='单位')
    invnum = models.DecimalField('清单数量', max_digits=13, decimal_places=3, default=0)
    invprice = models.DecimalField('清单单价', max_digits=13, decimal_places=2, default=0)
    changenum = models.DecimalField('工程变更增减数量', max_digits=13, decimal_places=3, default=0)
    changeprice = models.DecimalField('工程变更增减单价', max_digits=13, decimal_places=2, default=0)

    def invmoney(self):
        return format(self.invnum * self.invprice, '0,.2f')

    def changemoney(self):
        return format(self.changenum * self.changeprice, '0,.2f')

    def nownum(self):
        return format(self.invnum + self.changenum, '0.3f')

    def nowmoney(self):
        return format(self.invmoney() + self.changemoney(), '0,.2f')

    invmoney.short_description = '清单金额'  # admin中要设置为只读
    changemoney.short_description = '工程变更增减金额'
    nownum.short_description = '变更后数量'
    nowmoney.short_description = '变更后金额'
    thisweekcomplatenum = models.DecimalField('到本期末累计完成数量', max_digits=13, decimal_places=3, default=0)
    thisweekcomplatemoney = models.DecimalField('到本期末累计完成金额', max_digits=13, decimal_places=2, default=0)
    lastweekcomplatenum = models.DecimalField('到上期末累计完成数量', max_digits=13, decimal_places=3, default=0)
    lastweekcomplatemoney = models.DecimalField('到上期末累计完成金额', max_digits=13, decimal_places=2, default=0)
    thiscomplatenum = models.DecimalField('本期完成数量', max_digits=13, decimal_places=3, default=0)
    thiscomplatemoney = models.DecimalField('本期完成金额', max_digits=13, decimal_places=2, default=0)

    def complatedratio(self):
        return '{:0.2f}%'.format(self.thisweekcomplatenum / self.invnum * 200)

    complatedratio.short_description = '已完成百分比'
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '计量进度表'

    def __str__(self):
        return self.location + ' ' + self.code + ' ' + self.name


# 合同支付
class ContractPay(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, verbose_name='合同')
    date = models.DateField('日期')
    money = models.DecimalField('支付金额', max_digits=13, decimal_places=2)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '合同支付'

    def __str__(self):
        return self.contract


# 合同
class Contract(models.Model):
    name = models.CharField('合同名称', max_length=64)
    content = models.CharField('合同内容', max_length=64)
    contact = models.CharField('合作联系人', max_length=64)
    telphone = models.CharField('合作人电话', max_length=64)
    price = models.DecimalField('合同单价', max_digits=13, decimal_places=2)
    money = models.DecimalField('合同总价', max_digits=13, decimal_places=2)
    status = models.SmallIntegerField('完成状态', choices=contract_choices, default=0)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    def payed(self):
        summoney = ContractPay.objects.filter(contract=self.id).annotate(payed=models.Sum('money')).only('payed')
        return summoney['payed'] if (summoney['payed'] is not None) else 0

    payed.short_description = '已支付'

    def balance(self):
        return self.money - self.payed()

    balance.short_description = '剩余金额'

    class Meta:
        verbose_name_plural = verbose_name = '合同'

    def __str__(self):
        return self.name


# 子合同支付
class SubContractPay(models.Model):
    subcontract = models.ForeignKey('SubContract', on_delete=models.CASCADE, verbose_name='子合同')
    date = models.DateField('日期')
    money = models.DecimalField('支付金额', max_digits=13, decimal_places=2)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '子合同支付'

    def __str__(self):
        return self.subcontract


# 子合同
class SubContract(models.Model):
    parentcontract = models.ForeignKey('Contract', on_delete=models.CASCADE, verbose_name='主合同')
    name = models.CharField('合同名称', max_length=64)
    content = models.CharField('合同内容', max_length=64)
    contact = models.CharField('合作联系人', max_length=64)
    telphone = models.CharField('合作人电话', max_length=64)
    price = models.DecimalField('合同单价', max_digits=13, decimal_places=2)
    money = models.DecimalField('合同总价', max_digits=13, decimal_places=2)
    status = models.SmallIntegerField('完成状态', choices=contract_choices, default=0)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    def payed(self):
        summoney = ContractPay.objects.filter(subcontract=self.id).annotate(payed=models.Sum('money')).only('payed')
        return summoney['payed'] if (summoney['payed'] is not None) else 0

    payed.short_description = '已支付'

    class Meta:
        verbose_name_plural = verbose_name = '子合同'

    def __str__(self):
        return self.name


# 材料图算量
class Budget(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('图算量', max_digits=13, decimal_places=3)
    money = models.DecimalField('图算金额', max_digits=13, decimal_places=2)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '材料图算量'

    def __str__(self):
        return self.material


# 材料入库
class MaterialInRecord(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)
    money = models.DecimalField('金额', max_digits=13, decimal_places=2)
    docdate = models.DateField('日期')
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '材料入库'

    def __str__(self):
        return self.material


# 材料出库
class MaterialOutRecord(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.PROTECT, verbose_name='材料')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)
    money = models.DecimalField('金额', max_digits=13, decimal_places=2)
    docdate = models.DateField('日期')
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '材料出库'

    def __str__(self):
        return self.material


# 材料仓库现存量
class Stock(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.CASCADE, verbose_name='材料')
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)

    class Meta:
        verbose_name_plural = verbose_name = '材料库存'

    def __str__(self):
        return self.material


# 租赁管理-归还
class LeaseOutRecord(models.Model):
    docid = models.ForeignKey('LeaseInRecord', on_delete=models.CASCADE, verbose_name='租入单号')
    returndate = models.DateField('归还时间')
    num = models.DecimalField('归还数量', max_digits=13, decimal_places=3)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '归还'

    def __str__(self):
        p = self.docid
        return p.material


# 租赁管理-租入
class LeaseInRecord(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.PROTECT, verbose_name='名称')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    leasedate = models.DateField('租赁时间')
    num = models.DecimalField('租赁数量', max_digits=13, decimal_places=3)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    def returnnum(self):
        sumreturn = LeaseOutRecord.objects.filter(docid=self.id).annotate(sumreturn=models.Sum('num')).only('sumreturn')
        return sumreturn['sumreturn'] if (sumreturn['sumreturn'] is not None) else 0

    returnnum.short_description = '归还数量'

    def remainder(self):
        return self.num - self.returnnum()

    remainder.short_description = '剩余数量'

    class Meta:
        verbose_name_plural = verbose_name = '租入'

    def __str__(self):
        return self.material


# 租赁管理-库存
class LeaseStock(models.Model):
    material = models.ForeignKey('bases.Material', on_delete=models.PROTECT, verbose_name='名称')
    price = models.DecimalField('单价', max_digits=13, decimal_places=2)
    num = models.DecimalField('数量', max_digits=13, decimal_places=3)
    startdate = models.DateField('租赁时间')
    enddate = models.DateField('归还时间', blank=True, null=True)

    def leaseday(self):
        return self.enddate - self.startdate if self.enddate is not None else datetime.date.today() - self.startdate

    leaseday.short_description = '租赁天数'

    def leasemoney(self):
        return self.leaseday() * self.price

    leasemoney.short_description = '租赁金额'

    class Meta:
        verbose_name_plural = verbose_name = '租赁库存'

    def __str__(self):
        return self.material


# 人工费用
class LaborCost(models.Model):
    code = models.CharField('结算单号', max_length=64)
    name = models.CharField('项目', max_length=64)
    settlementdate = models.DateField('结算时间', default=datetime.date.today())
    settlementmoney = models.DecimalField('结算金额', max_digits=13, decimal_places=2)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '人工费用'

    def __str__(self):
        return self.code + ' ' + self.name


# 人工费用支付
class LaborPay(models.Model):
    laborcost = models.ForeignKey('LaborCost', on_delete=models.CASCADE, verbose_name='人工费用')
    paydate = models.DateField('日期', default=datetime.date.today())
    paymoney = models.DecimalField('支付金额', max_digits=13, decimal_places=2)
    maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
    makedate = models.DateField('日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '人工费用支付'

    def __str__(self):
        return self.laborcost

# 租赁费用
# class LeaseCost(models.Model):
