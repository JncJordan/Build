# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin
from django.contrib import admin

from .models import *


class ContractAdmin(object):
    '''
    合同列表
    '''
    list_display = ('合同名称', '合同内容', '合作联系人', '合作人电话', '合同单价', '已支付金额', '剩余金额', '完成状态')
    search_fields = ('合同名称', '合同内容', '合作联系人')
    list_filter = ('合同名称', '合同内容', '合作联系人', '合作人电话', '完成状态', '已支付金额', '剩余金额')
    exclude = ('已支付金额', '剩余金额')
    model_icon = 'fa fa-sticky-note-o'
    relfield_style = 'fk-select'

    class ContractPayInline(object):
        '''
        已支付
        '''
        model = ContractPay
        exclude = ('制单人',)
        extra = 1

    inlines = [ContractPayInline]

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        self.new_obj.save()

    def save_related(self):
        self.form_obj.save_m2m()
        contract = Contract.objects.filter(id=self.new_obj.id).first()
        summoney = ContractPay.objects.filter(合同=contract).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
        # contract.已支付金额 = contract.已支付金额 + self.new_obj.支付金额
        contract.剩余金额 = contract.合同总价 - contract.已支付金额
        contract.save()



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
        self.new_obj.制单人 = self.request.user
        self.new_obj.save()
        contract = Contract.objects.filter(id=self.new_obj.合同_id).first()
        # summoney = ContractPay.objects.filter(合同=contract).exclude(id=self.new_obj.id).values('合同').annotate(payed=models.Sum('支付金额'))[0]
        # contract.已支付金额 = summoney['payed'] if (summoney['payed'] is not None) else 0
        summoney = ContractPay.objects.filter(合同=contract).exclude(id=self.new_obj.id).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
        contract.已支付金额 = contract.已支付金额 + self.new_obj.支付金额
        contract.剩余金额 = contract.合同总价 - contract.已支付金额
        contract.save()


xadmin.site.register(Contract, ContractAdmin)
xadmin.sites.site.register(ContractPay, ContractPayAdmin)
