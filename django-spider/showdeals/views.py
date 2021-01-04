from django.shortcuts import render
from .models import DealInfo
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

# list all houses result
def show_deals(request):
    deal_list = DealInfo.objects.all().order_by('-timestamp')
    if deal_list:
        paginator = Paginator(deal_list, 20)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        return render(request, 'showdeals/index.html',
                      {'page_obj': page_obj, 'paginator': paginator,
                       'is_paginated': True, })
    else:
        return render(request, 'showdeals/index.html', { })