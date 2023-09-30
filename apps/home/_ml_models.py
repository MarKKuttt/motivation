import re
from typing import Dict
import datetime

# import pandas as pd
# import numpy as np

from ._metadesc import REPLACEMENTS_TEXT
# from .kkd.aggregator import EstimationAggregator, UserEstimationSettings
# from .kkd.exceptions import EmptySequenceError, NotEnoughSequenceLength
# from .kkd.utils import (DataHolder, DEFAULT_LOW_QUALITY_MEASURE,
#                        DEFAULT_MIDDLE_QUALITY_MEASURE)
#
# np.seterr(divide='ignore', invalid='ignore')
#
#
# # NER (find people mentions)
# # TODO: Вера
# def make_ner(appeal_msg_processed: object(str)) -> object:
#     ...
#
#
# # TOXIC (find sentiment)
# # TODO: Вера
# def make_toxic(appeal_msg_processed: object(str)) -> object:
#     ...
#
#
# # POS + TF-IDF (find tags and filter POS == noun)
# # TODO: Аня
# def find_tags(full_data: List[object]) -> List[object] / Tag:
#     # Choose nouns using POS tags (only nouns)
#     ...
#     # TF-IDF matrix for all docs (rating for nouns + sort)
#     ...
#     # Choose top-30 nouns by TF-IDF
#     ...
#
#
# # TAG (find tags)
# # TODO: Аня
# def make_tag(appeal_msg_processed: object(str)) -> List[object]:
#     # Similarity
#     ...
#     tags = Tags.objects.filter(name=...)
#     return tags


def process_msg_text(appeal_msg: str) -> str:
    for pattern, replace in REPLACEMENTS_TEXT.items():
        appeal_msg = re.sub(re.escape(pattern), replace, str(appeal_msg))
    return appeal_msg
#
#
# def make_kkd(full_data: List[object]) -> List[object]:
#     estimations_to_apply = (
#         UserEstimationSettings(level="basic", name="KolmogorovSmirnov", weight=.34),
#         UserEstimationSettings(level="basic", name="AndersonDarlingKSampled", weight=.33),
#         UserEstimationSettings(level="basic", name="TrendDegreeSampled", weight=.33),
#     )
#
#     def evaluate(data):  # -> Dict[object]:
#         all_sequence_estimations: Dict[str, float] = dict()
#         data_holder: DataHolder = DataHolder(data,
#                                              dates_column='Дата создания обращения',
#                                              filter_column="Тэги",
#                                              values_column="Токсичность обращения")
#         data_holder.collect()
#         for sequence in data_holder.sequences_to_validate:
#             try:
#                 estim_agg = EstimationAggregator(user_estimations=estimations_to_apply,
#                                                  sequence_to_validate=sequence)
#                 estim_agg.apply()
#                 all_sequence_estimations[sequence.name] = estim_agg.data_quality_measure
#             except EmptySequenceError as e:
#                 all_sequence_estimations[sequence.name] = DEFAULT_LOW_QUALITY_MEASURE
#             except NotEnoughSequenceLength as e:
#                 all_sequence_estimations[sequence.name] = DEFAULT_MIDDLE_QUALITY_MEASURE
#             return pd.DataFrame({
#                 'Тэг': all_sequence_estimations.keys(),
#                 'Аномалия по тегу': all_sequence_estimations.values(),
#                 'Время расчета': datetime.datetime.now()
#             })
