from django.contrib import admin

from .models import Lesson, PhrasePair


class PhrasePairInline(admin.TabularInline):
    model = PhrasePair
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    inlines = [PhrasePairInline]


@admin.register(PhrasePair)
class PhrasePairAdmin(admin.ModelAdmin):
    list_display = ("lesson", "phrase_one", "phrase_two")
    list_filter = ("lesson",)
    search_fields = ("phrase_one", "phrase_two")
