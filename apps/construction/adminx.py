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
        super(ContractAdmin, self).save_related()

        contract = Contract.objects.filter(id=self.new_obj.id).first()
        summoney = ContractPay.objects.filter(合同=contract).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
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

    def sumpay(self, contract_id):
        '''
        计算合同主表"已支付金额"和"剩余金额"
        :param contract_id:合同 id
        :return:
        '''
        contract = Contract.objects.filter(id=contract_id).first()
        summoney = ContractPay.objects.filter(合同=contract).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
        contract.剩余金额 = contract.合同总价 - contract.已支付金额
        contract.save()

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        # self.new_obj.save()
        super(ContractPayAdmin, self).save_models()
        self.sumpay(self.new_obj.合同_id)

    def delete_models(self, queryset):
        contract_id = queryset.first().合同_id
        super(ContractPayAdmin, self).delete_models(queryset)
        self.sumpay(contract_id)


xadmin.site.register(Contract, ContractAdmin)
xadmin.sites.site.register(ContractPay, ContractPayAdmin)
