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
        ('grammar', '🌸 Gramatyka'),
        ('reading', '☕ Czytanka'),
        ('writing', '✍️ Pisanie'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(blank=True) # Treść lekcji/czytanki
    
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self): return f"[{self.get_type_display()}] {self.title}"

# 4. ZADANIA
class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self): return self.question

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