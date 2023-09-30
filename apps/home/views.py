# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import TimeSeriesAnomaly, Appeal, AppealInitiator


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def recalc_anomaly():
    # template=''
    anomalies = TimeSeriesAnomaly.objects.all()
    context = {'anomalies': anomalies}
    return context
    # return render(request, template, context)


def download_data():
    # Выгрузка датасета Appeal
    ...


def main_page():
    context = {
        'Все обращения с тэгами + токсик + конструктив': Appeal.objects.all(),
        'Аномалия по тэгам': TimeSeriesAnomaly.objects.all(),
        'Пользователи с рейтингом': AppealInitiator.objects.all(),

    }
    # from django.db.models import Count, Avg
    # Количество сообщений на дату
    # Appeal.objects.values('date_create').annotate(dcount=Count('date_create')).order_by()
    # Средний конструктив на дату
    # Appeal.objects.values('date_create').annotate(avg=Avg('constructive')).order_by()
    # Средний токсик на дату
    # Appeal.objects.values('date_create').annotate(avg=Avg('toxic')).order_by()
    # Конструктив по юзерам
    # Appeal.objects.values('initiator__name').annotate(avg=Avg('constructive')).order_by()
    # Сообщения по тегам
    # Appeal.objects.values('tags__name').annotate(avg=Count('id')).order_by()
    return context
