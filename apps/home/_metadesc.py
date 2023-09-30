from dataclasses import dataclass, asdict


@dataclass
class ConstructiveCriteriaWeights:
    tag: float = 0.3
    attach: float = 0.3
    mention: float = 0.2
    initiator_ratio: float = 0.1
    toxic: float = 0.1

    def __post_init__(self):
        assert sum((self.tag, self.attach, self.mention, self.initiator_ratio, self.toxic)) == 1.0


weights = ConstructiveCriteriaWeights()


@dataclass
class ConstructiveCriterion:
    tag: bool
    attach: bool
    mention: bool
    initiator_ratio: float
    toxic: float

    @property
    def criteria(self):
        product = dict(zip(
                self.__dict__,
                (self.__dict__[key] * weights.__dict__[key] for key in self.__dict__)
            ))
        return sum(product.values())


REPLACEMENTS_TEXT = {
    r'[0-9\.]+': '',
    r'[\*]+': '',
    r'\[]\(.*\)': '',
    r'\[.*\]\(.*\)': '',
    r'http|ftp|https):[^\s]+': 'url',
    '**.**.****': '<ДАТА>',
    '**.**': '<ДАТА>',
    '** ** ******': '<ДАТА>',
    r'[\.]+': '.',
    '*': ''
}
