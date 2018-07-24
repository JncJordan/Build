# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin


class GlobalSetting(CommAdminView):
    site_title = '建筑管理系统'
    site_footer = 'Copyright © 2018 JIT'


xadmin.site.register(CommAdminView, GlobalSetting)
