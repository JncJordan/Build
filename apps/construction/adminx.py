# *-* coding:utf-8 *-*
from xadmin.views import CommAdminView
import xadmin
from django.contrib import admin
from django.db.models import When, Case
from django.forms import Media
from django.http import HttpResponseRedirect

from .models import *


class ContractAdmin(object):
    '''
    合同列表
    '''
    list_display = ('合同名称', '合同内容', '合作联系人', '合作人电话', '合同单价', '已支付金额', '剩余金额', '完成状态', '制单人')
    # list_display_links = ()
    # list_display_links_details = False
    # list_exclude=()
    list_select_related = None
    aggregate_fields = {'合同单价': 'sum', '已支付金额': 'sum', '剩余金额': 'sum', '合同名称': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    # ordering = None

    # 去除增删改功能
    # remove_permissions = ['add', 'change', 'delete']

    show_bookmarks = False
    search_fields = ('合同名称', '合同内容', '合作联系人')
    list_filter = ('合同名称', '合同内容', '合作联系人', '合作人电话', '完成状态', '已支付金额', '剩余金额')
    exclude = ('已支付金额', '剩余金额', '制单人')
    list_editable = ['完成状态']
    model_icon = 'fa fa-sticky-note-o'
    relfield_style = 'fk-select'

    # Change list templates
    # object_list_template = None

    class ContractPayInline(object):
        '''
        已支付
        '''
        model = ContractPay
        exclude = ('制单人',)
        extra = 1
        style = 'table'

    inlines = [ContractPayInline]

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        super(ContractAdmin, self).save_models()

    def save_related(self):
        super(ContractAdmin, self).save_related()

        # 给刚添加的记录增加 "制单人"
        self.new_obj.contractpay_set.filter(制单人=None).update(制单人=self.request.user)

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
    list_per_page = 50
    list_max_show_all = 200

    def sumpay(self, contract_id):
        '''
        计算合同主表"已支付金额"和"剩余金额"
        :param contract_id: 合同.id
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
        # 首先保存所有要删除的合同id
        contractqueryset = queryset.order_by('合同_id').values('合同_id').distinct()
        item = []
        for ids in contractqueryset:
            item.append(ids['合同_id'])

        super(ContractPayAdmin, self).delete_models(queryset)

        for contract_id in item:
            self.sumpay(contract_id)

    def delete_model(self):
        contract_id = self.obj.合同_id
        super(ContractPayAdmin, self).delete_model()
        self.sumpay(contract_id)


class SubContractAdmin(object):
    '''
    子合同列表
    '''
    list_display = ('主合同', '合同名称', '合同内容', '合作联系人', '合作人电话', '合同单价', '已支付金额', '剩余金额', '完成状态', '制单人')
    search_fields = ('主合同__合同名称', '合同名称', '合同内容', '合作联系人')
    list_filter = ('主合同', '合同名称', '合同内容', '合作联系人', '合作人电话', '完成状态', '已支付金额', '剩余金额')
    exclude = ('已支付金额', '剩余金额', '制单人')
    model_icon = 'fa fa-file-word-o'
    relfield_style = 'fk-select'
    list_per_page = 50
    list_max_show_all = 200

    class SubContractPayInline(object):
        '''
        已支付
        '''
        model = SubContractPay
        exclude = ('制单人',)
        extra = 1
        style = 'table'

    inlines = [SubContractPayInline]

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        super(SubContractAdmin, self).save_models()

    def save_related(self):
        super(SubContractAdmin, self).save_related()

        # 给刚添加的记录增加 "制单人"
        self.new_obj.subcontractpay_set.filter(制单人=None).update(制单人=self.request.user)

        contract = SubContract.objects.filter(id=self.new_obj.id).first()
        summoney = SubContractPay.objects.filter(子合同=contract).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
        contract.剩余金额 = contract.合同总价 - contract.已支付金额
        contract.save()


class SubContractPayAdmin(object):
    '''
    子合同支付
    '''
    list_display = ('单号', '子合同', '日期', '支付金额', '制单人')
    list_display_links = ('单号', '子合同')
    search_fields = ('单号', '子合同__合同名称', '制单人')
    list_filter = ('单号', '子合同', '日期', '制单人', '支付金额')
    exclude = ('制单人',)
    model_icon = 'fa fa-credit-card-alt'
    aggregate_fields = {'支付金额': 'sum', '单号': 'count'}
    list_per_page = 50
    list_max_show_all = 200

    def sumpay(self, contract_id):
        '''
        计算子合同主表"已支付金额"和"剩余金额"
        :param contract_id: 子合同.id
        :return:
        '''
        contract = SubContract.objects.filter(id=contract_id).first()
        summoney = SubContractPay.objects.filter(子合同=contract).aggregate(payed=models.Sum('支付金额'))['payed']
        contract.已支付金额 = summoney if summoney is not None else 0
        contract.剩余金额 = contract.合同总价 - contract.已支付金额
        contract.save()

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        # self.new_obj.save()
        super(SubContractPayAdmin, self).save_models()
        self.sumpay(self.new_obj.合同_id)

    def delete_models(self, queryset):
        # 首先保存所有要删除的子合同id
        contractqueryset = queryset.order_by('子合同_id').values('子合同_id').distinct()
        item = []
        for ids in contractqueryset:
            item.append(ids['子合同_id'])

        super(SubContractPayAdmin, self).delete_models(queryset)

        for contract_id in item:
            self.sumpay(contract_id)

    def delete_model(self):
        contract_id = self.obj.合同_id
        super(SubContractPayAdmin, self).delete_model()
        self.sumpay(contract_id)


class BudgetAdmin(object):
    '''
    材料图算量
    '''
    list_display = ('材料', '单价', '图算量', '金额', '入库总数量', '入库总金额', '剩余还需购买数量', '剩余还需购买金额')
    # list_display_links = ()
    # list_display_links_details = False
    # list_exclude=()
    list_select_related = None
    aggregate_fields = {'图算量': 'sum', '金额': 'sum', '入库总数量': 'sum', '入库总金额': 'sum', '剩余还需购买数量': 'sum', '剩余还需购买金额': 'sum', '材料': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    # ordering = None

    # 去除增删改功能
    # remove_permissions = ['add', 'change', 'delete']

    # show_bookmarks = False
    search_fields = ('材料__名称', '材料__规格')
    list_filter = ('材料', '入库总数量', '入库总金额', '剩余还需购买数量', '剩余还需购买金额')
    exclude = ('入库总数量', '入库总金额', '剩余还需购买数量', '剩余还需购买金额', '制单人')
    model_icon = 'fa fa-file-text-o'

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        # self.new_obj.入库总数量=...
        # self.new_obj.入库总金额=...
        self.new_obj.金额 = self.new_obj.图算量 * self.new_obj.单价
        self.new_obj.剩余还需购买数量 = self.new_obj.图算量 - self.new_obj.入库总数量
        self.new_obj.剩余还需购买金额 = self.new_obj.金额 - self.new_obj.入库总金额
        super(BudgetAdmin, self).save_models()

    def get_media(self):
        return super(BudgetAdmin, self).get_media() + Media(js=[self.static('/js/budget.js')])


# 增加图算量对应入库
def addbudget(material, innum=0, inmoney=0):
    '''
    增加图算量对应入库
    :param self:
    :param material: 材料
    :param innum: 入库数量
    :param inmoney: 入库金额
    :return:
    '''
    budget = Budget.objects.filter(材料=material).first()
    if budget is None:
        budget = Budget(材料=material)
    budget.入库总数量 += innum
    budget.入库总金额 += inmoney
    budget.剩余还需购买数量 = budget.图算量 - budget.入库总数量
    budget.剩余还需购买金额 = budget.金额 - budget.入库总金额
    budget.save()


# 减去图算量对应入库
def subbudget(material, innum=0, inmoney=0):
    '''
    减去图算量对应入库
    :param self:
    :param material: 材料
    :param innum: 入库数量
    :param inmoney: 入库金额
    :return:
    '''
    budget = Budget.objects.filter(材料=material).first()
    if budget is None:
        budget = Budget(材料=material)
    budget.入库总数量 -= innum
    budget.入库总金额 -= inmoney
    budget.剩余还需购买数量 = budget.图算量 - budget.入库总数量
    budget.剩余还需购买金额 = budget.金额 - budget.入库总金额
    budget.save()


# 材料汇总表
class MaterialStockAdmin(object):
    '''
    材料汇总表
    '''
    list_display = ('材料', '入库数量', '出库数量', '库存数量')
    # list_display_links = ()
    # list_display_links_details = False
    list_exclude = ('入库金额', '出库金额', '库存金额', '平均单价', '结算金额', '支付金额', '欠款金额')
    list_select_related = None
    aggregate_fields = {'入库数量': 'sum', '出库数量': 'sum', '库存数量': 'sum', '材料': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    # ordering = None

    # 去除增删改功能
    remove_permissions = ['add', 'change', 'delete']

    # show_bookmarks = False
    search_fields = ('材料__名称', '材料__规格')
    list_filter = ('材料', '入库数量', '出库数量', '库存数量')
    # exclude = ('入库金额', '出库金额', '库存金额', '平均单价', '结算金额', '支付金额', '欠款金额')
    model_icon = 'fa fa-database'


# 材料费用表
class MaterialCostAdmin(object):
    '''
        材料费用汇总表
        '''
    list_display = ('材料', '入库数量', '入库金额', '结算金额', '支付金额', '欠款金额')
    # list_display_links = ()
    # list_display_links_details = False
    list_exclude = ('出库数量', '出库金额', '库存数量', '库存金额', '平均单价', '结算金额', '支付金额', '欠款金额')
    list_select_related = None
    aggregate_fields = {'入库数量': 'sum', '入库金额': 'sum', '结算金额': 'sum', '支付金额': 'sum', '欠款金额': 'sum', '材料': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    # ordering = None

    # 去除增删改功能
    remove_permissions = ['add', 'change', 'delete']

    # show_bookmarks = False
    search_fields = ('材料__名称', '材料__规格')
    list_filter = ('材料', '材料__名称', '入库数量', '入库金额', '结算金额', '支付金额', '欠款金额')
    # exclude = ('入库金额', '出库金额', '库存金额', '平均单价', '结算金额', '支付金额', '欠款金额')
    model_icon = 'fa fa-table'


def addinstock(material, num, money):
    '''
    增加对应材料库存数量
    '''
    # 查找对应的材料库存
    materialstock = MaterialStock.objects.filter(材料=material).first()
    if materialstock is None:  # 没有则新增
        materialstock = MaterialStock(材料=material)
    materialstock.入库数量 += num
    materialstock.入库金额 += money
    materialstock.库存数量 += num
    materialstock.库存金额 += money
    materialstock.平均单价 = materialstock.库存金额 / materialstock.库存数量 if materialstock.库存数量 != 0 else 0
    materialstock.save()


def subinstock(material, num, money):
    '''
    减去对应材料库存数量
    '''
    materialstock = MaterialStock.objects.filter(材料=material).first()
    if materialstock is None:  # 没有则新增
        materialstock = MaterialStock(材料=material)
    materialstock.入库数量 -= num
    materialstock.入库金额 -= money
    materialstock.库存数量 -= num
    materialstock.库存金额 -= money
    materialstock.平均单价 = materialstock.库存金额 / materialstock.库存数量 if materialstock.库存数量 != 0 else 0
    materialstock.save()


def addoutstock(material, num, money):
    '''
    增加对应材料出库库存数量
    '''
    # 查找对应的材料库存
    materialstock = MaterialStock.objects.filter(材料=material).first()
    if materialstock is None:  # 没有则新增
        materialstock = MaterialStock(材料=material)
    materialstock.出库数量 += num
    materialstock.出库金额 += money
    materialstock.库存数量 -= num
    materialstock.库存金额 -= money
    materialstock.平均单价 = materialstock.库存金额 / materialstock.库存数量 if materialstock.库存数量 != 0 else 0
    materialstock.save()


def suboutstock(material, num, money):
    '''
    减去对应材料出库库存数量
    '''
    materialstock = MaterialStock.objects.filter(材料=material).first()
    if materialstock is None:  # 没有则新增
        materialstock = MaterialStock(材料=material)
    materialstock.出库数量 -= num
    materialstock.出库金额 -= money
    materialstock.库存数量 += num
    materialstock.库存金额 += money
    materialstock.平均单价 = materialstock.库存金额 / materialstock.库存数量 if materialstock.库存数量 != 0 else 0
    materialstock.save()


# 材料入库
class MaterialInRecordAdmin(object):
    '''
    材料入库
    '''
    list_display = ('单号', '材料', '单价', '数量', '金额', '日期', '制单人')
    list_display_links = ('单号', '材料')
    # list_display_links_details = False
    # list_exclude = ('出库数量', '出库金额', '库存数量', '库存金额', '平均单价', '结算金额', '支付金额', '欠款金额')
    list_select_related = None
    aggregate_fields = {'数量': 'sum', '金额': 'sum', '单号': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    ordering = ('-id',)

    # 去除增删改功能
    # remove_permissions = ['add', 'change', 'delete']

    # show_bookmarks = False
    search_fields = ('单号', '材料__名称', '材料__规格')
    list_filter = ('单号', '材料', '单价', '数量', '金额', '日期', '制单人')
    exclude = ('制单人',)
    model_icon = 'fa fa-plus-square'

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        flag = self.org_obj is None and 'create' or 'change'
        if flag == 'change':
            oldobj = MaterialInRecord.objects.get(id=self.org_obj.id)
            subinstock(oldobj.材料, oldobj.数量, oldobj.金额)
            subbudget(oldobj.材料, oldobj.数量, oldobj.金额)
        super(MaterialInRecordAdmin, self).save_models()
        addinstock(self.new_obj.材料, self.new_obj.数量, self.new_obj.金额)
        addbudget(self.new_obj.材料, self.new_obj.数量, self.new_obj.金额)

    def delete_models(self, queryset):
        # 首先保存所有要删除的记录
        inrecords = []
        for item in queryset:
            inrecords.append(item)

        super(MaterialInRecordAdmin, self).delete_models(queryset)

        for inrecord in inrecords:
            subinstock(inrecord.材料, inrecord.数量, inrecord.金额)
            subbudget(inrecord.材料, inrecord.数量, inrecord.金额)

    def delete_model(self):
        inrecord = self.obj
        super(MaterialInRecordAdmin, self).delete_model()
        subinstock(inrecord.材料, inrecord.数量, inrecord.金额)
        subbudget(inrecord.材料, inrecord.数量, inrecord.金额)

    def get_media(self):
        return super(MaterialInRecordAdmin, self).get_media() + Media(js=[self.static('/js/materialin.js')])


# 材料出库
class MaterialOutRecordAdmin(object):
    '''
    材料出库
    '''
    list_display = ('单号', '材料', '平均单价', '数量', '金额', '日期', '制单人')
    list_display_links = ('单号', '材料')
    # list_display_links_details = False
    # list_exclude = ('平均单价')
    list_select_related = None
    aggregate_fields = {'数量': 'sum', '金额': 'sum', '单号': 'count'}

    list_per_page = 50
    list_max_show_all = 200
    # paginator_class = Paginator
    ordering = ('-id',)

    # 去除增删改功能
    # remove_permissions = ['add', 'change', 'delete']

    # show_bookmarks = False
    search_fields = ('单号', '材料__名称', '材料__规格')
    list_filter = ('单号', '材料', '平均单价', '数量', '金额', '日期', '制单人')
    exclude = ('平均单价', '金额', '制单人',)
    model_icon = 'fa fa-minus-square'

    relurl = {'材料': '/bases/material_stock/'}

    # 限定材料必须是有库存的
    def get_context(self):
        context = super(MaterialOutRecordAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['材料'].queryset = Material.objects.filter(
                id__in=MaterialStock.objects.exclude(库存数量=0).values_list('材料_id', flat=True))
            # Material.objects.filter(id__in=list(MaterialStock.objects.exclude(库存数量=0).values_list('材料_id',flat=True)))
        return context
        # Model.objects.filter(xx__in=queryset)
        # Model.objects.filter(xx__in=list(queryset.values_list('id',flat=True)))
        # 后一种更有效率

    def save_models(self):
        self.new_obj.制单人 = self.request.user
        flag = self.org_obj is None and 'create' or 'change'
        if flag == 'change':
            oldobj = MaterialOutRecord.objects.get(id=self.org_obj.id)
            suboutstock(oldobj.材料, oldobj.数量, oldobj.金额)
        stock = MaterialStock.objects.filter(材料=self.new_obj.材料).first()
        if stock is None:
            raise Exception('库存中没有此材料')
        self.new_obj.平均单价 = stock.平均单价
        self.new_obj.金额 = self.new_obj.数量 * self.new_obj.平均单价
        super(MaterialOutRecordAdmin, self).save_models()
        addoutstock(self.new_obj.材料, self.new_obj.数量, self.new_obj.金额)

    # 捕捉保存的异常, 会报错 has_header
    def post(self, request, *args, **kwargs):
        try:
            response = super(MaterialOutRecordAdmin, self).post(request, *args, **kwargs)
        except Exception as err:
            self.message_user('库存中没有此材料', 'error')
            return HttpResponseRedirect(request.path)
        return response

    def delete_models(self, queryset):
        # 首先保存所有要删除的记录
        inrecords = []
        for item in queryset:
            inrecords.append(item)

        super(MaterialOutRecordAdmin, self).delete_models(queryset)

        for inrecord in inrecords:
            suboutstock(inrecord.材料, inrecord.数量, inrecord.金额)

    def delete_model(self):
        inrecord = self.obj
        super(MaterialOutRecordAdmin, self).delete_model()
        suboutstock(inrecord.材料, inrecord.数量, inrecord.金额)


xadmin.site.register(Contract, ContractAdmin)
xadmin.site.register(ContractPay, ContractPayAdmin)
xadmin.site.register(SubContract, SubContractAdmin)
xadmin.site.register(SubContractPay, SubContractPayAdmin)
xadmin.site.register(Budget, BudgetAdmin)
xadmin.site.register(MaterialStock, MaterialStockAdmin)
xadmin.site.register(MaterialCost, MaterialCostAdmin)
xadmin.site.register(MaterialInRecord, MaterialInRecordAdmin)
xadmin.site.register(MaterialOutRecord, MaterialOutRecordAdmin)

from .views import *

xadmin.site.register_view(r'^bases/material_stock/$', material_stock, name='material_stock')
