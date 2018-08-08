import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from bases.models import *


# # 工程进度表
# class JobSchedule(models.Model):
#     location = models.CharField('单项工程位置', max_length=64)
#     code = models.CharField('项目编号', max_length=64)
#     name = models.CharField('项目名称', max_length=64)
#     unit = models.ForeignKey('bases.Unit', on_delete=models.PROTECT, verbose_name='单位')
#     invnum = models.DecimalField('清单数量', max_digits=13, decimal_places=3, default=0)
#     invprice = models.DecimalField('清单单价', max_digits=13, decimal_places=2, default=0)
#     changenum = models.DecimalField('工程变更增减数量', max_digits=13, decimal_places=3, default=0)
#     changeprice = models.DecimalField('工程变更增减单价', max_digits=13, decimal_places=2, default=0)
#
#     def invmoney(self):
#         return format(self.invnum * self.invprice, '0,.2f')
#
#     def changemoney(self):
#         return format(self.changenum * self.changeprice, '0,.2f')
#
#     def nownum(self):
#         return format(self.invnum + self.changenum, '0.3f')
#
#     def nowmoney(self):
#         return format(self.invmoney() + self.changemoney(), '0,.2f')
#
#     invmoney.short_description = '清单金额'  # admin中要设置为只读
#     changemoney.short_description = '工程变更增减金额'
#     nownum.short_description = '变更后数量'
#     nowmoney.short_description = '变更后金额'
#     thisweekcomplatenum = models.DecimalField('到本期末累计完成数量', max_digits=13, decimal_places=3, default=0)
#     thisweekcomplatemoney = models.DecimalField('到本期末累计完成金额', max_digits=13, decimal_places=2, default=0)
#     lastweekcomplatenum = models.DecimalField('到上期末累计完成数量', max_digits=13, decimal_places=3, default=0)
#     lastweekcomplatemoney = models.DecimalField('到上期末累计完成金额', max_digits=13, decimal_places=2, default=0)
#     thiscomplatenum = models.DecimalField('本期完成数量', max_digits=13, decimal_places=3, default=0)
#     thiscomplatemoney = models.DecimalField('本期完成金额', max_digits=13, decimal_places=2, default=0)
#
#     def complatedratio(self):
#         return '{:0.2f}%'.format(self.thisweekcomplatenum / self.invnum * 200)
#
#     complatedratio.short_description = '已完成百分比'
#     maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
#     makedate = models.DateField('日期', auto_now=True)
#
#     class Meta:
#         verbose_name_plural = verbose_name = '工程进度表'
#
#     def __str__(self):
#         return self.location + ' ' + self.code + ' ' + self.name
#
#
# # 计量进度表
# class MeasuringSchedule(models.Model):
#     location = models.CharField('单项工程位置', max_length=64)
#     code = models.CharField('项目编号', max_length=64)
#     name = models.CharField('项目名称', max_length=64)
#     unit = models.ForeignKey('bases.Unit', on_delete=models.PROTECT, verbose_name='单位')
#     invnum = models.DecimalField('清单数量', max_digits=13, decimal_places=3, default=0)
#     invprice = models.DecimalField('清单单价', max_digits=13, decimal_places=2, default=0)
#     changenum = models.DecimalField('工程变更增减数量', max_digits=13, decimal_places=3, default=0)
#     changeprice = models.DecimalField('工程变更增减单价', max_digits=13, decimal_places=2, default=0)
#
#     def invmoney(self):
#         return format(self.invnum * self.invprice, '0,.2f')
#
#     def changemoney(self):
#         return format(self.changenum * self.changeprice, '0,.2f')
#
#     def nownum(self):
#         return format(self.invnum + self.changenum, '0.3f')
#
#     def nowmoney(self):
#         return format(self.invmoney() + self.changemoney(), '0,.2f')
#
#     invmoney.short_description = '清单金额'  # admin中要设置为只读
#     changemoney.short_description = '工程变更增减金额'
#     nownum.short_description = '变更后数量'
#     nowmoney.short_description = '变更后金额'
#     thisweekcomplatenum = models.DecimalField('到本期末累计完成数量', max_digits=13, decimal_places=3, default=0)
#     thisweekcomplatemoney = models.DecimalField('到本期末累计完成金额', max_digits=13, decimal_places=2, default=0)
#     lastweekcomplatenum = models.DecimalField('到上期末累计完成数量', max_digits=13, decimal_places=3, default=0)
#     lastweekcomplatemoney = models.DecimalField('到上期末累计完成金额', max_digits=13, decimal_places=2, default=0)
#     thiscomplatenum = models.DecimalField('本期完成数量', max_digits=13, decimal_places=3, default=0)
#     thiscomplatemoney = models.DecimalField('本期完成金额', max_digits=13, decimal_places=2, default=0)
#
#     def complatedratio(self):
#         return '{:0.2f}%'.format(self.thisweekcomplatenum / self.invnum * 200)
#
#     complatedratio.short_description = '已完成百分比'
#     maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
#     makedate = models.DateField('日期', auto_now=True)
#
#     class Meta:
#         verbose_name_plural = verbose_name = '计量进度表'
#
#     def __str__(self):
#         return self.location + ' ' + self.code + ' ' + self.name


# 合同支付
class ContractPay(models.Model):
    单号 = models.CharField(max_length=64)
    合同 = models.ForeignKey('Contract', on_delete=models.CASCADE)
    日期 = models.DateField()
    支付金额 = models.DecimalField(max_digits=13, decimal_places=2)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '合同支付'

    def __str__(self):
        return str(self.单号)


# 合同
class Contract(models.Model):
    合同名称 = models.CharField(max_length=64)
    合同内容 = models.CharField(max_length=64)
    合作联系人 = models.CharField(max_length=64)
    合作人电话 = models.CharField(max_length=64)
    合同单价 = models.DecimalField(max_digits=13, decimal_places=2)
    合同总价 = models.DecimalField(max_digits=13, decimal_places=2)
    完成状态 = models.SmallIntegerField(choices=合同状态, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    日期 = models.DateField(auto_now=True)
    已支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    剩余金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = verbose_name = '合同'

    def __str__(self):
        return self.合同名称


# 子合同支付
class SubContractPay(models.Model):
    单号 = models.CharField(max_length=64)
    子合同 = models.ForeignKey('SubContract', on_delete=models.CASCADE)
    日期 = models.DateField('日期')
    支付金额 = models.DecimalField(max_digits=13, decimal_places=2)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '子合同支付'

    def __str__(self):
        return self.单号


# 子合同
class SubContract(models.Model):
    主合同 = models.ForeignKey('Contract', on_delete=models.CASCADE)
    合同名称 = models.CharField(max_length=64)
    合同内容 = models.CharField(max_length=64)
    合作联系人 = models.CharField(max_length=64)
    合作人电话 = models.CharField(max_length=64)
    合同单价 = models.DecimalField(max_digits=13, decimal_places=2)
    合同总价 = models.DecimalField(max_digits=13, decimal_places=2)
    完成状态 = models.SmallIntegerField(choices=合同状态, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    日期 = models.DateField(auto_now=True)
    已支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    剩余金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = verbose_name = '子合同'

    def __str__(self):
        return self.合同名称


# 材料图算量
class Budget(models.Model):
    材料 = models.ForeignKey(Material, on_delete=models.PROTECT)
    单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    图算量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    日期 = models.DateField(auto_now=True)
    入库总数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    入库总金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    剩余还需购买数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    剩余还需购买金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = verbose_name = '材料图算量'

    def __str__(self):
        return str(self.材料)


# 材料库存表
class MaterialStock(models.Model):
    '''
    材料库存表
    '''
    材料 = models.ForeignKey(Material, on_delete=models.PROTECT)
    入库数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    入库金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    库存数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    库存金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    平均单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    出库数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    出库金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    结算数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    结算金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    未结算数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    未结算金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    欠款金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = verbose_name = '材料汇总表'

    def __str__(self):
        return str(self.材料)


# 材料费用表
class MaterialCost(MaterialStock):
    class Meta:
        verbose_name_plural = verbose_name = "材料费汇总"
        proxy = True


# 材料入库
class MaterialInRecord(models.Model):
    '''
    材料入库
    '''
    单号 = models.CharField(max_length=64)
    材料 = models.ForeignKey(Material, on_delete=models.PROTECT)
    单价 = models.DecimalField(max_digits=13, decimal_places=2)
    数量 = models.DecimalField(max_digits=13, decimal_places=3)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    日期 = models.DateField()
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '材料入库'

    def __str__(self):
        return self.单号 + ' ' + str(self.材料)


# 材料出库
class MaterialOutRecord(models.Model):
    单号 = models.CharField(max_length=64)
    材料 = models.ForeignKey(Material, on_delete=models.PROTECT)
    平均单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    日期 = models.DateField()
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '材料出库'

    def __str__(self):
        return self.单号 + ' ' + str(self.材料)


# 材料结算单
class MaterialCloseBill(models.Model):
    结算单 = models.CharField(max_length=64)
    材料 = models.ForeignKey(Material, on_delete=models.PROTECT)
    单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    已支付 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    未支付 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    日期 = models.DateField()

    def update_materialstock(self, material, num, money, payed, direction=1):
        materialstock = MaterialStock.objects.filter(材料=material).first()
        materialstock.结算数量 += direction * num
        materialstock.结算金额 += direction * money
        materialstock.未结算数量 = materialstock.入库数量 - materialstock.结算数量
        materialstock.未结算金额 = materialstock.入库金额 - materialstock.结算金额
        materialstock.支付金额 += direction * payed
        materialstock.欠款金额 = materialstock.结算金额 - materialstock.支付金额
        materialstock.save()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            oldobj = MaterialCloseBill.objects.get(pk=self.pk)
            if oldobj is not None:
                self.update_materialstock(oldobj.材料, oldobj.数量, oldobj.金额, oldobj.已支付, -1)
        self.未支付 = self.金额 - self.已支付
        super().save(*args, **kwargs)
        self.update_materialstock(self.材料, self.数量, self.金额, self.已支付)

    # def delete(self, *args, **kwargs):
    #     oldobj = MaterialCloseBill.objects.get(pk=self.pk)
    #     if oldobj is not None:
    #         self.update_materialstock(oldobj.材料, oldobj.数量, oldobj.金额, oldobj.已支付, -1)
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = verbose_name = '材料结算'

    def __str__(self):
        return self.结算单 + ' ' + str(self.材料)


# 已删除"材料结算"触发器
@receiver(post_delete, sender=MaterialCloseBill)
def update_materialclosebill(sender, instance, **kwargs):
    materialstock = MaterialStock.objects.filter(材料=instance.材料).first()
    materialstock.结算数量 -= instance.数量
    materialstock.结算金额 -= instance.金额
    materialstock.未结算数量 = materialstock.入库数量 - materialstock.结算数量
    materialstock.未结算金额 = materialstock.入库金额 - materialstock.结算金额
    materialstock.支付金额 -= instance.已支付
    materialstock.欠款金额 = materialstock.结算金额 - materialstock.支付金额
    materialstock.save()


# 材料支付
class MaterialPay(models.Model):
    结算单 = models.ForeignKey(MaterialCloseBill, on_delete=models.PROTECT)
    支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    日期 = models.DateField()

    def update_materialclosebill(closebill, payed, direction=1):
        materialclosebill = MaterialCloseBill.objects.filter(pk=closebill.pk).first()
        materialclosebill.已支付 += direction * payed
        materialclosebill.未支付 = materialclosebill.金额 - materialclosebill.已支付
        materialclosebill.save()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            oldobj = MaterialPay.objects.get(pk=self.pk)
            if oldobj is None:
                pass
            self.update_materialclosebill(oldobj.结算单, oldobj.支付金额, -1)
        super().save(*args, **kwargs)
        self.update_materialclosebill(self.结算单, self.支付金额)

    class Meta:
        verbose_name_plural = verbose_name = '材料支付'

    def __str__(self):
        return str(self.结算单)


# 已删除"材料支付"触发器
@receiver(post_delete, sender=MaterialPay)
def update_materialclosebill(sender, instance, **kwargs):
    materialclosebill = MaterialCloseBill.objects.filter(pk=instance.结算单.pk).first()
    materialclosebill.已支付 += -1 * instance.支付金额
    materialclosebill.未支付 = materialclosebill.金额 - materialclosebill.已支付
    materialclosebill.save()


# 租赁管理-库存
class LeaseStock(models.Model):
    '''
    租赁库存
    '''
    材料设备 = models.ForeignKey(Material, on_delete=models.PROTECT)
    租赁日期 = models.DateField()
    租赁数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    归还数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    剩余数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    归还金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    结算金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    欠款金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def money(self):
        days = Decimal((datetime.date.today() - self.租赁日期).days)
        return round(days * self.单价 * self.剩余数量, 2) + self.归还金额

    金额 = property(money)

    class Meta:
        verbose_name_plural = verbose_name = '租赁管理'
        unique_together = ('材料设备', '租赁日期', '单价')

    def __str__(self):
        return str(self.材料设备)


# 租赁费用
class LeaseCost(LeaseStock):
    class Meta:
        verbose_name_plural = verbose_name = '租赁费用'
        proxy = True


# 租赁管理-租入
class LeaseIn(models.Model):
    租赁日期 = models.DateField()
    材料设备 = models.ForeignKey(Material, on_delete=models.PROTECT)
    单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)

    def update_leasestock(self, leasein, direction=1):
        leasestock = LeaseStock.objects.filter(材料设备=leasein.材料设备, 租赁日期=leasein.租赁日期, 单价=leasein.单价).first()
        if leasestock is None:
            leasestock = LeaseStock(材料设备=leasein.材料设备, 租赁日期=leasein.租赁日期, 单价=leasein.单价)
        leasestock.租赁数量 += direction * leasein.数量
        leasestock.剩余数量 = leasestock.租赁数量 - leasestock.归还数量
        leasestock.save()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            oldobj = LeaseIn.objects.get(pk=self.pk)
            if oldobj is not None:
                self.update_leasestock(oldobj, -1)
        super().save(*args, **kwargs)
        self.update_leasestock(self)

    class Meta:
        verbose_name_plural = verbose_name = '租赁租入'
        unique_together = ('租赁日期', '材料设备', '单价')

    def __str__(self):
        return str(self.id) + ' ' + str(self.材料设备)


# 已删除"租赁租入"触发器
@receiver(post_delete, sender=LeaseIn)
def update_Leasein(sender, instance, **kwargs):
    leasestock = LeaseStock.objects.filter(材料设备=instance.材料设备, 租赁日期=instance.租赁日期, 单价=instance.单价).first()
    if leasestock is None:
        # leasestock = LeaseStock(材料设备=instance.材料设备, 租赁日期=instance.租赁日期, 单价=instance.单价)
        return
    leasestock.租赁数量 -= instance.数量
    leasestock.剩余数量 = instance.租赁数量 - instance.归还数量
    leasestock.save()


# 租赁管理-归还
class LeaseOut(models.Model):
    租赁单 = models.ForeignKey(LeaseStock, on_delete=models.PROTECT)
    归还日期 = models.DateField()
    数量 = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
    租赁日期 = models.DateField(editable=False, default=datetime.date.today())
    单价 = models.DecimalField(max_digits=13, decimal_places=2, default=0, editable=False)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0, editable=False)

    def update_leasestock(self, leaseout, direction=1):
        leasestock = LeaseStock.objects.filter(材料设备=leaseout.租赁单.材料设备, 租赁日期=leaseout.租赁单.租赁日期, 单价=leaseout.租赁单.单价).first()
        if leasestock is None:
            # leasestock = LeaseStock(材料设备=leaseout.租赁单.材料设备, 租赁日期=leaseout.租赁单.租赁日期, 单价=leaseout.租赁单.单价)
            return
        leasestock.归还数量 += direction * leaseout.数量
        leasestock.剩余数量 = leasestock.租赁数量 - leasestock.归还数量
        days = (leaseout.归还日期 - leaseout.租赁单.租赁日期).days
        leasestock.归还金额 = days * leaseout.租赁单.单价 * leasestock.归还数量
        leasestock.save()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            oldobj = LeaseOut.objects.get(pk=self.pk)
            if oldobj is not None:
                self.update_leasestock(oldobj, -1)
        self.租赁日期 = self.租赁单.租赁日期
        self.单价 = self.租赁单.单价
        self.金额 = (self.归还日期 - self.租赁日期).days * self.单价
        super().save(*args, **kwargs)
        self.update_leasestock(self)

    class Meta:
        verbose_name_plural = verbose_name = '租赁归还'

    def __str__(self):
        return str(self.id) + str(self.租赁单.材料设备)


# 已删除"租赁归还"触发器
@receiver(post_delete, sender=LeaseOut)
def update_Leasein(sender, instance, **kwargs):
    leasestock = LeaseStock.objects.filter(材料设备=instance.租赁单.材料设备, 租赁日期=instance.租赁单.租赁日期, 单价=instance.租赁单.单价).first()
    if leasestock is None:
        # leasestock = LeaseStock(材料设备=instance.材料设备, 租赁日期=instance.租赁日期, 单价=instance.单价)
        return
    leasestock.归还数量 -= instance.数量
    leasestock.剩余数量 = leasestock.租赁数量 - leasestock.归还数量
    days = (instance.归还日期 - instance.租赁单.租赁日期).days
    leasestock.归还金额 = days * instance.租赁单.单价 * leasestock.归还数量
    leasestock.save()


# 租赁结算
class LeaseCloseBill(models.Model):
    结算单号 = models.CharField(max_length=64)
    租赁单 = models.ForeignKey(LeaseStock, on_delete=models.PROTECT)
    结算金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    支付金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    欠款金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    备注 = models.CharField(max_length=256, blank=True, null=True)
    日期 = models.DateField()
    制单人 = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)

    def update_leasestock(self, instance, direction=1):
        leasestock = LeaseStock.objects.filter(pk=instance.租赁单).first()
        if leasestock is None:
            # leasestock = LeaseStock(材料设备=leaseout.租赁单.材料设备, 租赁日期=leaseout.租赁单.租赁日期, 单价=leaseout.租赁单.单价)
            return
        leasestock.结算金额 += direction * instance.结算金额
        leasestock.支付金额 += direction * instance.支付金额
        leasestock.欠款金额 = leasestock.结算金额 - leasestock.支付金额
        leasestock.save()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            oldobj = LeaseCloseBill.objects.get(pk=self.pk)
            if oldobj is not None:
                self.update_leasestock(oldobj, -1)
        self.欠款金额 = self.结算金额 - self.支付金额
        super().save(*args, **kwargs)
        self.update_leasestock(self)

    class Meta:
        verbose_name_plural = verbose_name = '租赁结算'

    def __str__(self):
        return self.结算单号 + ' ' + str(self.租赁单.材料设备)


# 已删除"租赁结算"触发器
@receiver(post_delete, sender=LeaseCloseBill)
def update_Leasein(sender, instance, **kwargs):
    leasestock = LeaseStock.objects.filter(pk=instance.租赁单).first()
    if leasestock is None:
        # leasestock = LeaseStock(材料设备=instance.材料设备, 租赁日期=instance.租赁日期, 单价=instance.单价)
        return
    leasestock.结算金额 -= instance.结算金额
    leasestock.支付金额 -= instance.支付金额
    leasestock.欠款金额 = leasestock.结算金额 - leasestock.支付金额
    leasestock.save()


# 租赁支付
class LeasePay(models.Model):
    结算单 = models.ForeignKey(LeaseCloseBill, on_delete=models.PROTECT)
    金额 = models.DecimalField(max_digits=13, decimal_places=2, default=0)

# # 人工费用
# class LaborCost(models.Model):
#     code = models.CharField('结算单号', max_length=64)
#     name = models.CharField('项目', max_length=64)
#     settlementdate = models.DateField('结算时间', default=datetime.date.today())
#     settlementmoney = models.DecimalField('结算金额', max_digits=13, decimal_places=2)
#     memo = models.CharField('备注', max_length=128, blank=True, null=True)
#     maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
#     makedate = models.DateField('日期', auto_now=True)
#
#     class Meta:
#         verbose_name_plural = verbose_name = '人工费用'
#
#     def __str__(self):
#         return self.code + ' ' + self.name
#
#
# # 人工费用支付
# class LaborPay(models.Model):
#     laborcost = models.ForeignKey('LaborCost', on_delete=models.CASCADE, verbose_name='人工费用')
#     paydate = models.DateField('日期', default=datetime.date.today())
#     paymoney = models.DecimalField('支付金额', max_digits=13, decimal_places=2)
#     maker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='填表人')
#     makedate = models.DateField('日期', auto_now=True)
#
#     class Meta:
#         verbose_name_plural = verbose_name = '人工费用支付'
#
#     def __str__(self):
#         return self.laborcost
