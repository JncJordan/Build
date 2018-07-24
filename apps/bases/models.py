from django.db import models

# 费用分类
cost_choices = ((0, '人工费用'), (1, '租赁费用'), (2, '材料费用'), (3, '办公室费用'))

# 合同完成状态
contract_choices = ((0, '未完成'), (1, '已完成'))


# 单位档案
class Unit(models.Model):
    name = models.CharField('单位', max_length=32)

    class Meta:
        verbose_name = verbose_name_plural = '单位'

    def __str__(self):
        return self.name


# 材料档案
class Material(models.Model):
    name = models.CharField('名称', max_length=64)
    spec = models.CharField('规格', max_length=64)
    unit = models.ForeignKey('Unit', on_delete=models.PROTECT, verbose_name='单位')

    class Meta:
        verbose_name_plural = verbose_name = '材料'

    def __str__(self):
        return self.name + ' ' + self.spec
