from typing import Any

import torch
from transformers import AutoTokenizer, pipeline

tagger_model_name = "toxic"  # rubertconv_toxic_editor
tokenizer = AutoTokenizer.from_pretrained("toxic")
model = AutoModelForTokenClassification.from_pretrained("toxic")

tagger_pipe = pipeline(
    "token-classification",
    model=model,
    tokenizer=tokenizer,
    framework="pt",
    aggregation_strategy="max"
)


def calc_toxic_ratio(sentence: str) -> Dict[str, Any]:
    replaces = []
    sum_score = 0

    result: List[Dict[str, Any]] = tagger_pipe(sentence)

    _score = list(map(lambda _dict_: _dict_['score'], result))
    _entity = list(map(lambda _dict_: _dict_['entity_group'], result))
    _word = list(map(lambda _dict_: _dict_['word'], result))

    for score, entity, word in zip(_score, _entity, _word):
        if entity in ('replace', 'delete',):
            replaces.append(word)
            sum_score -= score
        else:
            sum_score += score

    #     return {'ratio': sum_score / len(_score), 'replace_tokens': {k: '<ЦЕНЗУРА>' for k in replaces}}
    return {'ratio': sum_score / len(_score), 'replace_tokens': {}}
