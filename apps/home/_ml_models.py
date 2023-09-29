# NER (find people mentions)
# TODO: Вера
def make_ner(appeal_msg_processed: object(str)) -> object:
    ...


# TOXIC (find sentiment)
# TODO: Вера
def make_toxic(appeal_msg_processed: object(str)) -> object:
    ...


# POS + TF-IDF (find tags and filter POS == noun)
# TODO: Аня
def find_tags(full_data: List[object]) -> List[object] / Tag:
    # Choose nouns using POS tags (only nouns)
    ...
    # TF-IDF matrix for all docs (rating for nouns + sort)
    ...
    # Choose top-30 nouns by TF-IDF
    ...


# TAG (find tags)
# TODO: Аня
def make_tag(appeal_msg_processed: object(str)) -> List[object]:
    # Similarity
    ...
    tags = Tags.objects.filter(name=...)
    return tags


# MAKE KKD
# TODO: Эмилия
def process_msg_text(appeal_msg_processed: object(str)) -> object:
    # На вход одно обращение
    ...
    # На выход обращение после регулярок - убираем цифры, звездочки, ...
    ...


# MAKE KKD
# TODO: Эмилия
def make_kkd(full_data: List[object]) -> List[object]:
    # Принимаем полный датафрейм
    ...
    # Возвращаем датафрейм с тэгом + метрика
    ...
