from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Lesson, Level, Category

# Rejestrujemy Lekcje z użyciem Summernote (Edytora)
class LessonAdmin(SummernoteModelAdmin):  # <--- Dziedziczymy po SummernoteModelAdmin
    summernote_fields = ('content',)      # <--- Wskazujemy, które pole ma być "Wordem"
    list_display = ('title', 'level', 'type') # To sprawi, że lista lekcji będzie ładniejsza
    list_filter = ('level', 'type')           # Dodajemy filtry z prawej strony panelu

# Rejestrujemy pozostałe modele normalnie
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Level)
admin.site.register(Category)