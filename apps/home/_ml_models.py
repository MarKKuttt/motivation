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
def find_tags(full_data: List[object]) -> List[object]:
    ...


# TAG (find tags)
# TODO: Аня
def make_tag(appeal_msg_processed: object(str)) -> List[object]:
    ...


# MAKE KKD
# TODO: Эмилия
def process_msg_text(appeal_msg_processed: object(str)) -> object:
    ...


# MAKE KKD
# TODO: Эмилия
def make_kkd(full_data: List[object]) -> List[object]:
    ...
