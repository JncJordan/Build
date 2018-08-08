from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from xadmin.views import BaseAdminView

from bases.models import Material
from .models import MaterialStock, MaterialCloseBill, LeaseStock


# Create your views here.

# 材料出库_rel_材料(必须是库存中有的材料)
class material_outrecord(BaseAdminView):
    paginator_class = Paginator

    def get(self, request, *args, **kwargs):
        queryset = Material.objects.filter(id__in=MaterialStock.objects.filter(库存数量__gt=0).values_list('材料_id', flat=True))
        querystr = request.GET.get('_q_')
        if (querystr is not None and querystr != ''):
            queryset = queryset.filter(Q(名称__contains=querystr) | Q(规格__contains=querystr))
        paginator = self.paginator_class(queryset, 50, 0, True)
        result_count = paginator.count
        result_list = paginator.page(1).object_list
        has_more = result_count > 50

        objects = []
        for obj in result_list:
            objects.append({'id': obj.id, '__str__': escape(str(obj))})

        return self.render_response(
            {'headers': {'id': 'ID', '__str__': '材料'}, 'objects': objects, 'total_count': result_count,
             'has_more': has_more})


# 材料结算_rel_材料(必须是未结算数>0)
class material_closebill(BaseAdminView):
    paginator_class = Paginator

    def get(self, request, *args, **kwargs):
        queryset = Material.objects.filter(id__in=MaterialStock.objects.filter(未结算数量__gt=0).values_list('材料_id', flat=True))
        querystr = request.GET.get('_q_')
        if (querystr is not None and querystr != ''):
            queryset = queryset.filter(Q(名称__contains=querystr) | Q(规格__contains=querystr))
        paginator = self.paginator_class(queryset, 50, 0, True)
        result_count = paginator.count
        result_list = paginator.page(1).object_list
        has_more = result_count > 50

        objects = []
        for obj in result_list:
            objects.append({'id': obj.id, '__str__': escape(str(obj))})

        return self.render_response(
            {'headers': {'id': 'ID', '__str__': '材料'}, 'objects': objects, 'total_count': result_count,
             'has_more': has_more})


# 材料支付_rel_结算单(必须是未支付>0)
class material_pay(BaseAdminView):
    paginator_class = Paginator

    def get(self, request, *args, **kwargs):
        queryset = MaterialCloseBill.objects.filter(未支付__gt=0)
        querystr = request.GET.get('_q_')
        if (querystr is not None and querystr != ''):
            queryset = queryset.filter(Q(结算单__contains=querystr) | Q(材料__名称__contains=querystr) | Q(材料__规格__contains=querystr))
        paginator = self.paginator_class(queryset, 50, 0, True)
        result_count = paginator.count
        result_list = paginator.page(1).object_list
        has_more = result_count > 50

        objects = []
        for obj in result_list:
            objects.append({'id': obj.id, '__str__': escape(str(obj))})

        return self.render_response(
            {'headers': {'id': 'ID', '__str__': '结算单'}, 'objects': objects, 'total_count': result_count,
             'has_more': has_more})


# 租赁归还_rel_租赁材料(必须是剩余数量>0)
class leasestock_out(BaseAdminView):
    paginator_class = Paginator

    def get(self, request, *args, **kwargs):
        queryset = LeaseStock.objects.filter(剩余数量__gt=0)
        querystr = request.GET.get('_q_')
        if (querystr is not None and querystr != ''):
            queryset = queryset.filter(Q(材料设备__名称__contains=querystr) | Q(材料设备__规格__contains=querystr))
        paginator = self.paginator_class(queryset, 50, 0, True)
        result_count = paginator.count
        result_list = paginator.page(1).object_list
        has_more = result_count > 50

        objects = []
        for obj in result_list:
            objects.append({'id': obj.id, '__str__': escape(str(obj))})

        return self.render_response(
            {'headers': {'id': 'ID', '__str__': '材料设备'}, 'objects': objects, 'total_count': result_count,
             'has_more': has_more})
