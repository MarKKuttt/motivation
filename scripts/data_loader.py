import csv
from pathlib import Path

import pandas as pd

from apps.home.models import AppealInitiator, Tag, TimeSeriesAnomaly, Appeal


PARENT_PATH = Path(__file__).resolve().parent.parent.parent


def run():
    Tag.objects.all().delete()
    LOCAL_FILE_PATH = 'motivation/data/tags.csv'
    with open(PARENT_PATH / LOCAL_FILE_PATH, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            Tag(
                name=row[0],
                color=row[1],
                group=row[2]
            ).save()

    AppealInitiator.objects.all().delete()
    LOCAL_FILE_PATH = 'motivation/data/initiators.csv'
    with open(PARENT_PATH / LOCAL_FILE_PATH, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            AppealInitiator(
                name=row[0],
                tab_number=row[1],
                date_register=row[2],
                ratio=row[3]
            ).save()

    TimeSeriesAnomaly.objects.all().delete()
    LOCAL_FILE_PATH = 'motivation/data/anomalies.csv'
    with open(PARENT_PATH / LOCAL_FILE_PATH, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            _tag_id = row[0]
            TimeSeriesAnomaly(
                tag=Tag.objects.get(pk=_tag_id),
                date_update=row[1],
                ratio=row[2]
            ).save()

    Appeal.objects.all().delete()
    LOCAL_FILE_PATH_A = 'motivation/data/appeals.csv'
    LOCAL_FILE_PATH_AT = 'motivation/data/appeal_tags.csv'
    ap_tags = pd.read_csv(PARENT_PATH / LOCAL_FILE_PATH_AT, encoding='utf-8', header=None)
    with open(PARENT_PATH / LOCAL_FILE_PATH_A, encoding='utf-8') as ap:
        reader = csv.reader(ap)
        for i, row in enumerate(reader):
            _tags_ids = ap_tags[ap_tags[0] == i][1].tolist()
            _tags = [Tag.objects.get(pk=_tag_id) for _tag_id in _tags_ids]
            appeal = Appeal(
                initiator=AppealInitiator.objects.get(pk=row[0]),
                message=row[1],
                initial_theme=row[2],
                date_create=row[3],
                zno_id=row[4],
                attachment=row[5],
                processed_message=row[6],
                mentioned=row[7],
                toxic=row[8],
                constructive=row[9],
            )
            appeal.save()
            appeal.tags.set(_tags)
