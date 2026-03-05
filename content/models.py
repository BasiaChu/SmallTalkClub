from django.db import models
from django.contrib.auth.models import User

# 1. POZIOMY (np. A1, A2)
class Level(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

# 2. KATEGORIE (np. Czasy, Słówka)
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

# 3. LEKCJA (Gramatyka, Czytanka - wszystko w jednym)
class Lesson(models.Model):
    TYPE_CHOICES = [
        ('grammar', 'baza wiedzy - teoria'),
        ('exercise', 'ćwiczenia'),
        ('reading', 'czytanie'),
        ('writing', 'pisanie'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(blank=True) # Treść lekcji/czytanki
    
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Plik PDF")

    def __str__(self): return f"[{self.get_type_display()}] {self.title}"

# 5. WYNIKI
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField()

class ExerciseResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0) # Ile punktów zdobył
    max_score = models.IntegerField(default=0) # Na ile możliwych punktów
    date_completed = models.DateTimeField(auto_now_add=True) # Kiedy to zrobił

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.score}/{self.max_score})"

class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tasks', verbose_name="Do jakiego tematu to należy?")
    title = models.CharField(max_length=200, verbose_name="Nazwa zadania")
    url_link = models.URLField(verbose_name="Link do zadania")

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    # Klucz obcy - łączy to pytanie z konkretną lekcją
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions', verbose_name="Lekcja")
    
    # Treść pytania
    question_text = models.CharField(max_length=500, verbose_name="Treść pytania (np. I ___ a cat.)")
    
    # Opcje do wyboru dla ucznia
    option_a = models.CharField(max_length=200, verbose_name="Odpowiedź A")
    option_b = models.CharField(max_length=200, verbose_name="Odpowiedź B")
    option_c = models.CharField(max_length=200, verbose_name="Odpowiedź C")
    
    # Wskazanie dla systemu, która odpowiedź jest prawidłowa (żeby mógł ocenić ucznia)
    CORRECT_CHOICES = (
        ('A', 'Odpowiedź A'),
        ('B', 'Odpowiedź B'),
        ('C', 'Odpowiedź C'),
    )
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES, verbose_name="Poprawna odpowiedź")

    def __str__(self):
        return self.question_text

class Exercise(models.Model):
    # RODZIC (Zadanie na karcie pracy)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises', verbose_name="Lekcja")
    instruction = models.CharField(max_length=200, verbose_name="Polecenie do zadania (np. Uzupełnij luki w zdaniach twierdzących)")

    def __str__(self):
        return f"{self.lesson.title} - {self.instruction}"


class ExerciseItem(models.Model):
    # DZIECKO (Pojedynczy przykład/zdanie wewnątrz tego zadania)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='items', verbose_name="Do jakiego zadania to należy?")
    
    question_text = models.CharField(max_length=500, verbose_name="Zdanie z luką (np. 'She ___ (go) to school.')")
    correct_answer = models.CharField(max_length=200, verbose_name="Poprawna odpowiedź (np. 'goes')")

    def __str__(self):
        return self.question_text