# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from .models import Tag, Appeal, TimeSeriesAnomaly, AppealInitiator


@admin.register(AppealInitiator)
class InitiatorAdmin(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
    search_fields = ('name', 'tab_number')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
    search_fields = ('name', )


class TagInlineAdmin(admin.TabularInline):
    model = Appeal.tags.through


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
    search_fields = ('author', 'name', 'tags', 'pub_date', )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('initiator', 'message', 'initial_theme', 'zno_id',
                       'mentioned', 'constructive')}
         ),
        # ('Advanced Options', {
        #     'fields': ('image',)}
        #  ),
    )
    inlines = (TagInlineAdmin,)


@admin.register(TimeSeriesAnomaly)
class TimeSeriesAnomalyAdmin(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
    search_fields = ('tag', )
