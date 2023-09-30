# -*- encoding: utf-8 -*-
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from ._ml_models import process_msg_text


class AppealInitiator(models.Model):
    name = models.CharField(
        max_length=100,
        unique=False,
        verbose_name=_('ФИО инициатора')
    )
    tab_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Табельный номер')
    )
    date_register = models.DateField(
        auto_created=True,
        auto_now_add=True,
        verbose_name=_('Дата регистрации первого обращения')
    )
    ratio = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=1.0,
        verbose_name=_('Рейтинг пользователя')
    )

    class Meta:
        verbose_name = _('Инициатор обращения')
        verbose_name_plural = _('Инициаторы обращений')
        ordering = ('-date_register', 'tab_number')

    def __str__(self):
        return f'{self.tab_number} ({self.name})'


class Tag(models.Model):
    """Model for Tag instance."""

    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name=_('Название'),
    )
    color = models.CharField(
        max_length=7,
        validators=[RegexValidator(
            regex=r'^#[a-zA-Z0-9]{6}$',
            message=_('Недопустимые символы в коде'),
            code='invalid_hex_code'
        )],
        verbose_name=_('HEX код'),
        unique=False,
        default='#FF0000'
    )
    group = models.CharField(
        default=None,
        max_length=30,
        unique=False,
        verbose_name=_('Группа тэга'),
    )

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')
        ordering = ('name',)

    def __str__(self):
        return self.name


class TimeSeriesAnomaly(models.Model):

    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_DEFAULT,
        default='<Неизвестный>',
        related_name='anomaly',
        verbose_name=_('Заявитель')
    )
    date_update = models.DateField(
        auto_created=True,
        auto_now=True,
        verbose_name=_('Время расчета')
    )
    ratio = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Уровень аномалии')
    )

    class Meta:
        verbose_name = _('Аномалия по тэгам')
        verbose_name_plural = _('Аномалии по тэгам')
        ordering = ('tag', 'ratio')


class Appeal(models.Model):
    initiator = models.ForeignKey(
        AppealInitiator,
        null=True,
        # blank=True,
        on_delete=models.SET_NULL,
        related_name='appeals',
        verbose_name=_('Заявитель')
    )
    message = models.CharField(
        max_length=300,
        unique=False,
        verbose_name=_('Текст обращения'),
    )
    initial_theme = models.CharField(
        max_length=300,
        unique=False,
        verbose_name=_('Тема обращения'),
    )
    date_create = models.DateField(
        verbose_name=_('Дата создания обращения')
    )
    zno_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name=_('Номер ЗНО'),
    )
    attachment = models.BooleanField(
        verbose_name=_('Наличие вложения')
    )
    processed_message = models.CharField(
        blank=True,
        max_length=300,
        unique=False,
        verbose_name=_('АВТО: Текст обращения обработанный'),
    )
    tags = models.ManyToManyField(
        Tag,
        null=True,
        related_name='appeals',
        verbose_name=_('Теги')
    )
    mentioned = models.BooleanField(
        blank=True,
        verbose_name=_('Упоминание сотрудника или клиента'),
    )
    toxic = models.DecimalField(
        blank=True,
        max_digits=2,
        decimal_places=1,
        default=1.0,
        verbose_name=_('Токсичность сообщения')
    )
    constructive = models.DecimalField(
        blank=True,
        max_digits=2,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Конструктивность обращения')
    )

    class Meta:
        verbose_name = _('Обращение')
        verbose_name_plural = _('Обращения')
        ordering = ('zno_id', 'date_create')

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.processed_message:
            self.processed_message = process_msg_text(str(self.message))

        # if not self.tags:
        #     pass
            # self.tags = None

        if not self.mentioned:
            self.mentioned = False

        if not self.toxic:
            self.toxic = 0.0

        if not self.constructive:
            self.constructive = 0.0

        super(Appeal, self).save(*args, **kwargs)
