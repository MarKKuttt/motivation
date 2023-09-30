from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# sberbank-rubert-base-collection3
tokenizer = AutoTokenizer.from_pretrained("ner")
model = AutoModelForTokenClassification.from_pretrained("ner")

classifier = pipeline("ner", model=model, tokenizer=tokenizer)

from typing import Dict, List


def ner_instances(sentence: str) -> Dict[int, List]:
    queue = []
    last_end = None
    instances = {}

    result = classifier(sentence)
    _start = list(map(lambda _dict_: _dict_['start'], result))
    _end = list(map(lambda _dict_: _dict_['end'], result))
    _entity = list(map(lambda _dict_: _dict_['entity'], result))

    for start, end, entity in zip(_start, _end, _entity):
        if last_end and start == last_end:
            queue[-1][-1] = end
        else:
            queue.append([start, end])
        last_end = end
        instances[queue[-1][0]] = [end, entity]

    mask = {
        'I-PER': '<ИМЯ>',
        'I-LOC': '<МЕСТО>'
    }
    replace_tokens = {sentence[k: v[0]]: mask.get(v[1], '<ПРОЧЕЕ>') for k, v in instances.items()}
    replace_tokens = {k: v for k, v in replace_tokens.items() if v != '<ПРОЧЕЕ>'}
    return replace_tokens

