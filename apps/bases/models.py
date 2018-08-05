from django.db import models

# 费用分类
# cost_choices = ((0, '人工费用'), (1, '租赁费用'), (2, '材料费用'), (3, '办公室费用'))
费用分类 = ((0, '人工费用'), (1, '租赁费用'), (2, '材料费用'), (3, '办公室费用'))

# 合同完成状态
# contract_choices = ((0, '未完成'), (1, '已完成'))
合同状态 = ((0, '未完成'), (1, '已完成'))


# 单位档案
class Unit(models.Model):
    单位 = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.单位

    class Meta:
        verbose_name_plural = verbose_name = '单位'


# 材料档案
class Material(models.Model):
    名称 = models.CharField(max_length=64)
    规格 = models.CharField(max_length=64)
    单位 = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return self.名称 + ' [' + self.规格 + '] ' + str(self.单位)

    class Meta:
        verbose_name_plural = verbose_name = '材料'


# 项目
class Project(models.Model):
    项目名称 = models.CharField(max_length=64)

    def __str__(self):
        return self.项目名称

    class Meta:
        verbose_name_plural = verbose_name = '项目'


# 单项工程位置
class SubProject(models.Model):
    单项工程位置 = models.CharField(max_length=64)
    项目名称 = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.项目名称) + ' ' + self.单项工程位置

    class Meta:
        verbose_name_plural = verbose_name = '单项工程位置'
