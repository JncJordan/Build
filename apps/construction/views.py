from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import InvalidPage, Paginator
from django.utils.encoding import force_text, smart_text
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from xadmin.views import BaseAdminView
import xadmin

from bases.models import Material
from .models import MaterialStock


# Create your views here.

class material_stock(BaseAdminView):
    paginator_class = Paginator

    def get(self, request, *args, **kwargs):
        queryset = Material.objects.filter(id__in=MaterialStock.objects.exclude(库存数量=0).values_list('材料_id', flat=True))
        querystr = request.GET.get('_q_')
        if (querystr is not None and querystr != ''):
            queryset = queryset.filter(Q(名称__contains=querystr) | Q(规格__contains=querystr))
        result_list = queryset._clone()
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

# xadmin.site.register_view(r'^bases/material_stock/$', material_stock, name='material_stock')
