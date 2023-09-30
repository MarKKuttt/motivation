import io
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Dict, Any

from django.http import FileResponse



import xlwt

from django.http import HttpResponse

from .models import Appeal



from django.http import HttpResponse
from openpyxl import Workbook

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    print('export_users_xls')
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    # Add headers
    headers = ["Name", "Quantity"]
    ws.append(headers)

    # Add data from the model
    products = Appeal.objects.all()
    for product in products:
        ws.append([product.message, product.constructive])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


# def export_users_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Data')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = [
#         'ФИО инициатора', 'Сообщение', 'Дата создания', 'Исполнено', 'ЗНО', 'Тэг', 'Конструктивность'
#     ]

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()

#     rows = Appeal.objects.values_list(
#         'initiator__name', 'message', 'date_create', 'date_done', 'zno_id', 'tags__name', 'constructive'
#     )
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response


