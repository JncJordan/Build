from django.db import models

# 费用分类
# cost_choices = ((0, '人工费用'), (1, '租赁费用'), (2, '材料费用'), (3, '办公室费用'))
费用分类 = ((0, '人工费用'), (1, '租赁费用'), (2, '材料费用'), (3, '办公室费用'))

# 合同完成状态
# contract_choices = ((0, '未完成'), (1, '已完成'))
合同状态 = ((0, '未完成'), (1, '已完成'))


# 单位档案
class Unit(models.Model):
    # class 单位(models.Model):
    单位 = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.单位

    class Meta:
        verbose_name_plural = verbose_name = '单位'


# 材料档案
class Material(models.Model):
    # class 材料(models.Model):
    名称 = models.CharField(max_length=64)
    规格 = models.CharField(max_length=64)
    单位 = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return self.名称 + ' ' + self.规格

    class Meta:
        verbose_name_plural = verbose_name = '材料'
