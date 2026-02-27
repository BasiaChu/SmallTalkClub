from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Lesson, ExerciseResult, Level, Category
from .forms import CustomLoginForm, CustomRegisterForm

def home(request):
    return render(request, 'index.html')

def grammar(request):
    lessons_from_db = Lesson.objects.filter(type='grammar')
    # Dodajmy szukanie ukończonych lekcji również tutaj dla spójności ptaszków ✔️
    completed_ids = []
    if request.user.is_authenticated:
        completed_ids = ExerciseResult.objects.filter(user=request.user).values_list('lesson_id', flat=True)
    
    return render(request, 'grammar.html', {
        'lessons': lessons_from_db,
        'completed_ids': completed_ids
    })

# --- GŁÓWNA STRONA ĆWICZEŃ (DUŻE KAFELKI) ---
def exercises(request):
    # Ta funkcja teraz tylko wyświetla nasze piękne drzewka i kafelki poziomów
    return render(request, 'exercises.html')

# --- WIDOK KONKRETNEGO POZIOMU (MAŁE KAFELKI) ---
def exercise_level(request, level_name):
    # Strażnik błędu 404
    level = get_object_or_404(Level, name__iexact=level_name)

    categories = Category.objects.filter(lesson__level=level).distinct()

    titles = {
        'a1': 'Poziom A1 🌱', 'a2': 'Poziom A2 🌿', 'b1': 'Poziom B1 🌳',
        'b2': 'Poziom B2 🌲', 'osmoklasista': 'Egzamin Ósmoklasisty 8️⃣',
        'matura_podstawa': 'Matura Podstawowa 🎓', 'matura_rozszerzenie': 'Matura Rozszerzona 🚀',
    }
    display_name = titles.get(level_name.lower(), level.name)

    return render(request, 'exercise_level_detail.html', {
        'level': level,
        'level_display': display_name,
        'categories': categories, # Zamiast 'lessons', wysyłamy teraz kategorie (tematy)
    })

# NOWA FUNKCJA: Wyświetla listę kart pracy dla konkretnego tematu (np. A2 -> Present Simple)
def topic_exercises(request, level_name, category_slug):
    level = get_object_or_404(Level, name__iexact=level_name)
    category = get_object_or_404(Category, slug=category_slug)
    
    # Wyciągamy wszystkie karty pracy (Lessons) dla tego poziomu i tematu
    worksheets = Lesson.objects.filter(level=level, category=category, type='exercise')
    
    return render(request, 'topic_exercises.html', {
        'level': level,
        'category': category,
        'worksheets': worksheets
    })

def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)

    exercises = lesson.exercises.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            ExerciseResult.objects.create(
                user=request.user,
                lesson=lesson,
                score=10,
                max_score=10
            )
            messages.success(request, f"Brawo! Zapisano wynik z lekcji: {lesson.title} 🎉")
            return redirect('student_zone')
        else:
            messages.warning(request, "Zaloguj się, aby zapisywać swoje postępy!")
            return redirect('login')
            
    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'exercises': exercises
        })

def private_lessons(request):
    return render(request, 'private_lessons.html')

def readings(request):
    all_readings = Lesson.objects.filter(type='reading').order_by('level')
    return render(request, 'readings.html', {'readings': all_readings})

# --- STREFA UCZNIA I LOGOWANIE ---

def register_user(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Hura! Twoje konto zostało pomyślnie założone. Witamy w klubie! 🌸")
            return redirect("student_zone") 
    else:
        form = CustomRegisterForm()
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("student_zone")
    else:
        form = CustomLoginForm() 
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("home")

@login_required(login_url='login')
def student_zone(request):
    user_results = ExerciseResult.objects.filter(user=request.user).order_by('-date_completed')
    return render(request, "student_zone.html", {"results": user_results})