from django.contrib import admin
from .models import Lesson, Category, Level, Exercise, ExerciseItem

# 1. Pozwala dopisywać pytania (Itemy) bezpośrednio w Zadaniu
class ExerciseItemInline(admin.TabularInline):
    model = ExerciseItem
    extra = 1 # Ile pustych pól na pytania ma się pojawić na starcie

# 2. Pozwala dopisywać Zadanie bezpośrednio wewnątrz Lekcji
class ExerciseInline(admin.StackedInline):
    model = Exercise
    extra = 1
    show_change_link = True

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # To sprawi, że w liście lekcji od razu widzisz co jest czym
    list_display = ('title', 'level', 'category', 'type')
    list_filter = ('level', 'type', 'category')
    search_fields = ('title',)
    
    # TA LINIA TO MAGIA: Wkłada formularz zadań do środka lekcji!
    inlines = [ExerciseInline]

# Rejestrujemy resztę, żeby były pod ręką
admin.site.register(Category)
admin.site.register(Level)
# Te poniższe są teraz opcjonalne, bo masz je wewnątrz Lesson:
admin.site.register(Exercise)
admin.site.register(ExerciseItem)