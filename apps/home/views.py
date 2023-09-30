# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

from .models import TimeSeriesAnomaly, Appeal, AppealInitiator


# @login_required(login_url="/login/")
# def index(request):
#     context = {'segment': 'index'}
#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
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


# def main_page():
#     context = {
#         'Все обращения с тэгами + токсик + конструктив': Appeal.objects.all(),
#         'Аномалия по тэгам': TimeSeriesAnomaly.objects.all(),
#         'Пользователи с рейтингом': AppealInitiator.objects.all(),

#     }
#     # from django.db.models import Count, Avg
#     # Количество сообщений на дату
#     # Appeal.objects.values('date_create').annotate(dcount=Count('date_create')).order_by()
#     # Средний конструктив на дату
#     # Appeal.objects.values('date_create').annotate(avg=Avg('constructive')).order_by()
#     # Средний токсик на дату
#     # Appeal.objects.values('date_create').annotate(avg=Avg('toxic')).order_by()
#     # Конструктив по юзерам
#     # Appeal.objects.values('initiator__name').annotate(avg=Avg('constructive')).order_by()
#     # Сообщения по тегам
#     # Appeal.objects.values('tags__name').annotate(avg=Count('id')).order_by()
#     return context



from collections import defaultdict
from datetime import timedelta
import json
from django.utils import timezone


def iso_week_format(date):
    return f"{date.isocalendar()[0]}-W{date.isocalendar()[1]:02d}"

def main_page(request):
    all_appeals = Appeal.objects.all()
    jsonData = defaultdict(lambda: defaultdict(int))
    uniqueConstructiveData = defaultdict(lambda: defaultdict(int))
    toxicDataByWeek = defaultdict(lambda: defaultdict(int))  # Новый словарь для токсичных данных
    anomalyjson = {}

    all_initiators = AppealInitiator.objects.all()
    users = [f"User {initiator.tab_number}" for initiator in all_initiators]
    ratings = [float(initiator.ratio) for initiator in all_initiators]
    data = {
        "users": users,
        "ratings": ratings,
    }
    all_anomalies = TimeSeriesAnomaly.objects.all()
    for anomaly in all_anomalies:
        anomalyjson[anomaly.tag.name] = float(anomaly.ratio)
        week_str = iso_week_format(anomaly.date_update)
        tag_name = anomaly.tag.name
        jsonData[week_str][tag_name] += 1

    for appeal in all_appeals:
        week_str = iso_week_format(appeal.date_create)
        tag_name = appeal.initial_theme

        # Для токсичных сообщений
        if appeal.toxic:
            toxicDataByWeek[week_str][tag_name] += 1

        # Для конструктивных сообщений
        if appeal.constructive:
            uniqueConstructiveData[week_str][tag_name] += 1

    if all_appeals.exists():
        earliest_appeal_date = all_appeals.order_by('date_create').first().date_create
        latest_appeal_date = all_appeals.order_by('-date_create').first().date_create

    today = timezone.localdate()
    appeals_today_count = all_appeals.filter(date_create=today).count()

    context = {
        'all_appeals': all_appeals,
        'time_series_anomaly': TimeSeriesAnomaly.objects.all(),
        'appeal_initiator': AppealInitiator.objects.all(),
        'appeal_count': len(all_appeals),
        'earliest_appeal_date': earliest_appeal_date,
        'latest_appeal_date': latest_appeal_date,
        'appeals_today_count': appeals_today_count,
        'anomalyjson': json.dumps(anomalyjson),
        'jsonData': json.dumps(jsonData),
        'uniqueConstructiveData': json.dumps(uniqueConstructiveData),
        'toxicDataByWeek': json.dumps(toxicDataByWeek),  # Новый элемент в контексте
        'data': json.dumps(data),
    }

    print(data)

    return render(request, 'home/index.html', context)


def your_view(request):
    appeals = Appeal.objects.all()
    return render(request, 'apps/templates/home/datatable.html', {'appeals': appeals})
