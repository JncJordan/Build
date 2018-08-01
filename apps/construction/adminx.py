# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin
from django.contrib import admin

from .models import *


class ContractAdmin(object):
    '''
    合同列表
    '''
    list_display = ('合同名称', '合同内容', '合作联系人', '合作人电话', '合同单价', 'payed', 'balance', '完成状态')
    search_fields = ('合同名称', '合同内容', '合作联系人')
    list_filter = ('合同名称', '合同内容', '合同联系人', '合作人电话', '完成状态', 'payed', 'balance')
    model_icon = 'fa fa-sticky-note-o'
    relfield_style = 'fk-select'

    class ContractPayInline(object):
        '''
        已支付
        '''
        model = ContractPay
        extra = 1

    inlines = [ContractPayInline]


class ContractPayAdmin(object):
    '''
    合同支付
    '''
    list_display = ('单号', '合同', '日期', '支付金额', '制单人')
    list_display_links = ('单号', '合同')
    search_fields = ('单号', '合同__合同名称', '制单人')
    list_filter = ('单号', '合同', '日期', '制单人', '支付金额')
    exclude = ('制单人',)
    model_icon = 'fa fa-credit-card'
    aggregate_fields = {'支付金额': 'sum', '单号': 'count'}

    def save_models(self):
        obj = self.new_obj
        obj.制单人 = self.request.user
        obj.save()


xadmin.site.register(Contract, ContractAdmin)
xadmin.site.register(ContractPay, ContractPayAdmin)
