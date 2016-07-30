import json
import xlwt

from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from cakes.helpers import fetch_all_cakes
from cakes.models import Cake, Category
from cakes.drf import CakeSerializer


class CakeView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        category_id = request.GET.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            cakes = category.cakes.all()
        else:
            cakes = Cake.objects.all()
        return render(request, 'home.html', {'cakes': cakes, 'categories': categories})


class FetchCakes(View):

    def get(self, request, *args, **kwargs):
        fetch_all_cakes()
        return redirect(reverse('home'))


class ExportCakes(View):

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('format')
        if export_format == 'json':
            categories = Category.objects.all()
            cake_data = []
            for category in categories:
                category_dict = {'category': category.name, 'cakes': []}
                cakes = category.cakes.all()
                for cake in cakes:
                    category_dict['cakes'].append({
                        'title': cake.title,
                        'price': cake.price,
                        'image': cake.image.url
                    })
                cake_data.append(category_dict)
            filename = 'cakes.json'
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="%s.txt"' % filename
            response.write(json.dumps({'objects': cake_data}))
            return response
        elif export_format == 'excel':
            categories = Category.objects.all()
            workbook = xlwt.Workbook()
            for category in categories:
                worksheet = workbook.add_sheet(category.name)
                worksheet.write(0, 0, '#')
                worksheet.write(0, 1, 'Title')
                worksheet.write(0, 2, 'Image')
                cakes = category.cakes.all()
                for row, cake in enumerate(cakes, start=1):
                    worksheet.write(row, 0, row)
                    worksheet.write(row, 1, cake.title)
                    worksheet.write(row, 2, cake.image.url)
                    worksheet.write(row, 3, cake.price)
            filename = 'cakes.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=' + filename
            workbook.save(response)
            return response
        else:
            return HttpResponse('Invalid format', status=400)


class CakeViewSet(ModelViewSet):
    serializer_class = CakeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('title', 'price')

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = category.cakes.all()
        else:
            queryset = Cake.objects.all()

        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=max_price)
        if min_price and min_price.isdigit():
            queryset = queryset.filter(price__gte=min_price)
        return queryset


