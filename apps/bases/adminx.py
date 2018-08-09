# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin
from django.contrib import admin

from .models import *
from construction.models import *


class GlobalSetting(CommAdminView):
    site_title = '建筑管理系统'
    site_footer = 'Copyright © 2018 JIT'
    menu_style = 'accordion'  # 菜单设置成折叠

    def get_site_menu(self):
        return [
            {
                'title': '建筑合同管理', 'perm': self.has_model_perm(Contract, 'changelist'),
                'icon': 'fa fa-institution',
                'menus': (
                    {'title': '合同', 'url': self.get_model_url(Contract, 'changelist'), 'perm': self.get_model_perm(Contract, 'changelist')},
                    {'title': '合同支付', 'url': self.get_model_url(ContractPay, 'changelist'), 'perm': self.get_model_perm(ContractPay, 'changelist')},
                    {'title': '子合同', 'url': self.get_model_url(SubContract, 'changelist'), 'perm': self.get_model_perm(SubContract, 'changelist')},
                    {'title': '子合同支付', 'url': self.get_model_url(SubContractPay, 'changelist'),
                     'perm': self.get_model_perm(SubContractPay, 'changelist')},
                )
            },
            {
                'title': '建筑材料管理',  # 'perm': self.get_model_perm(Contract, 'view'),
                'icon': 'fa fa-cubes',
                'menus': (
                    {'title': '图算量', 'url': self.get_model_url(Budget, 'changelist'), 'perm': self.get_model_perm(Budget, 'changelist')},
                    {'title': '汇总表', 'url': self.get_model_url(MaterialStock, 'changelist'),
                     'perm': self.get_model_perm(MaterialStock, 'changelist')},
                    {'title': '费用表', 'url': self.get_model_url(MaterialCost, 'changelist'), 'perm': self.get_model_perm(MaterialCost, 'changelist')},
                    {'title': '入库', 'url': self.get_model_url(MaterialInRecord, 'changelist'),
                     'perm': self.get_model_perm(MaterialInRecord, 'changelist')},
                    {'title': '出库', 'url': self.get_model_url(MaterialOutRecord, 'changelist'),
                     'perm': self.get_model_perm(MaterialOutRecord, 'changelist')},
                    {'title': '结算', 'url': self.get_model_url(MaterialCloseBill, 'changelist'),
                     'perm': self.get_model_perm(MaterialCloseBill, 'changelist')},
                    {'title': '支付', 'url': self.get_model_url(MaterialPay, 'changelist'), 'perm': self.get_model_perm(MaterialPay, 'changelist')},
                )
            },
            {
                'title': '建筑租赁管理',  # 'perm': self.get_model_perm(Contract, 'view'),
                'icon': 'fa fa-shopping-cart',
                'menus': (
                    {'title': '租赁库存', 'url': self.get_model_url(LeaseStock, 'changelist'), 'perm': self.get_model_perm(LeaseStock, 'changelist')},
                    {'title': '租赁费用', 'url': self.get_model_url(LeaseCost, 'changelist'), 'perm': self.get_model_perm(LeaseCost, 'changelist')},
                    {'title': '租入', 'url': self.get_model_url(LeaseIn, 'changelist'), 'perm': self.get_model_perm(LeaseIn, 'changelist')},
                    {'title': '归还', 'url': self.get_model_url(LeaseOut, 'changelist'), 'perm': self.get_model_perm(LeaseOut, 'changelist')},
                    {'title': '结算', 'url': self.get_model_url(LeaseCloseBill, 'changelist'),
                     'perm': self.get_model_perm(LeaseCloseBill, 'changelist')},
                    {'title': '支付', 'url': self.get_model_url(LeasePay, 'changelist'), 'perm': self.get_model_perm(LeasePay, 'changelist')},
                )
            },
        ]


#
#
# xadmin.site.register_view('mystatistics/busexpensedetails/index', BusExpenseDetailsAdminView, name='index')
# xadmin.site.register_view('mystatistics/version/index', VersionInfoAdminView, name='index')
#
# class VersionInfoAdminView(CommAdminView):
#     def get_breadcrumb(self):
#         """获取头部面包屑导航"""
#         breadcrumb = CommAdminView.get_breadcrumb(self)
#         breadcrumb.append({'title': '版本信息', 'url': '/mystatistaics/version/index'})
#         return breadcrumb
#
#     def get(self, request, *args, **kwargs):
#         """
#         @return TemplateResponse
#         """
#         return TemplateResponse(request, 'version_info_index.html', self.get_context())


# 单位
class UnitAdmin(object):
    list_display = ('单位',)
    search_fields = ('单位',)  # 要查询的列
    list_filter = ('单位',)  # 要筛选的列
    model_icon = 'fa fa-cube'  # 模块的图标
    relfield_style = 'fk-select'


# 材料
class MaterialAdmin(object):
    list_display = ('名称', '规格', '单位')  # 添加要显示的列
    search_fields = ('名称', '规格')  # 要查询的列
    list_filter = ('名称', '规格')  # 要筛选的列
    model_icon = 'fa fa-cubes'
    # raw_id_fields = ('单位',)  # 原 django自带admin 才有此效果
    relfield_style = 'fk-select'  # 使用了之后，其他 Admin 中，自定义get_context获取材料的数据源失败


# 项目
class ProjectAdmin(object):
    list_display = ('项目名称',)
    search_fields = ('项目名称',)
    model_icon = 'fa fa-university'
    relfield_style = 'fk-select'

    class SubProjectInline(object):
        model = SubProject
        extra = 1
        # style = 'tab' # 有 'one', 'accordion', 'tab', 'table' 四种样式
        style = 'table'

    inlines = [SubProjectInline]


# 单项工程位置
class SubProjectAdmin(object):
    list_display = ('项目名称', '单项工程位置')
    search_fields = ('项目名称__项目名称', '单项工程位置')
    list_filter = ('项目名称', '单项工程位置')
    relfield_style = ('fk-select')
    model_icon = 'fa fa-building'


xadmin.site.register(CommAdminView, GlobalSetting)

xadmin.site.register(Material, MaterialAdmin)
xadmin.site.register(Unit, UnitAdmin)

xadmin.site.register(SubProject, SubProjectAdmin)
xadmin.site.register(Project, ProjectAdmin)
