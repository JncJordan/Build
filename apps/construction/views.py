from django.shortcuts import render
from xadmin.views import BaseAdminView
import xadmin

from bases.models import Material
from .models import MaterialStock
from bases.adminx import MaterialAdmin


# Create your views here.
# class teststock(MaterialAdmin):
#     def get_list_queryset(self):
#         queryset = super(teststock, self).get_list_queryset()
#         return queryset.filter(id__in=MaterialStock.objects.exclude(库存数量=0).values_list('材料_id', flat=True))


# class material_stock(BaseAdminView):
    # def make_result_list(self):
    #     # Get search parameters from the query string.
    #     self.list_queryset = self.get_list_queryset()
    #     self.ordering_field_columns = self.get_ordering_field_columns()
    #     self.paginator = self.get_paginator()
    #
    #     # Get the number of objects, with admin filters applied.
    #     self.result_count = self.paginator.count
    #
    #     self.can_show_all = self.result_count <= self.list_max_show_all
    #     self.multi_page = self.result_count > self.list_per_page
    #
    #     # Get the list of objects to display on this page.
    #     if (self.show_all and self.can_show_all) or not self.multi_page:
    #         self.result_list = self.list_queryset._clone()
    #     else:
    #         try:
    #             self.result_list = self.paginator.page(
    #                 self.page_num + 1).object_list
    #         except InvalidPage:
    #             if ERROR_FLAG in self.request.GET.keys():
    #                 return SimpleTemplateResponse('xadmin/views/invalid_setup.html', {
    #                     'title': _('Database error'),
    #                 })
    #             return HttpResponseRedirect(self.request.path + '?' + ERROR_FLAG + '=1')
    #     self.has_more = self.result_count > (
    #             self.list_per_page * self.page_num + len(self.result_list))
    #
    # def get_list_display(self, list_display):
    #     list_fields = [field for field in self.request.GET.get('_fields', "").split(",")
    #                    if field.strip() != ""]
    #     if list_fields:
    #         return list_fields
    #     return list_display
    #
    # def get_result_list(self, response):
    #     av = self.admin_view
    #     base_fields = self.get_list_display(av.base_list_display)
    #     headers = dict([(c.field_name, force_text(c.text)) for c in av.result_headers(
    #     ).cells if c.field_name in base_fields])
    #
    #     objects = [dict([(o.field_name, escape(str(o.value))) for i, o in
    #                      enumerate(filter(lambda c: c.field_name in base_fields, r.cells))])
    #                for r in av.results()]
    #
    #     return self.render_response(
    #         {'headers': headers, 'objects': objects, 'total_count': av.result_count, 'has_more': av.has_more})

    # def get(self, request, *args, **kwargs):
    #     queryset = Material.objects.filter(id__in=MaterialStock.objects.exclude(库存数量=0).values_list('材料_id', flat=True))
    #
    #     return self.render_response(
    #         {'headers': {'id': 'ID', '__str__': '材料'}, 'objects': [{'id': '3', '__str__': '砂 [细] 吨'}], 'total_count': 3,
    #          'has_more': False})

# xadmin.site.register_view(r'^bases/material_stock/$', material_stock, name='material_stock')
