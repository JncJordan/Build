# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin
from django.contrib import admin

from .models import *


class GlobalSetting(CommAdminView):
    site_title = '建筑管理系统'
    site_footer = 'Copyright © 2018 JIT'
    menu_style = 'accordion'  # 菜单设置成折叠


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
    raw_id_fields = ('单位',)  # 原 admin 才有此效果
    relfield_style = 'fk-ajax'


# 项目
class ProjectAdmin(object):
    list_display = ('项目名称',)
    search_fields = ('项目名称',)
    model_icon = 'fa fa-university'
    relfield_style = 'fk-select'

    class SubProjectInline(object):
        model = SubProject
        extra = 1
        # style = 'tab'

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
