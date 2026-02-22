import random  # <-- 1. NOWOŚĆ: Importujemy maszynę losującą!
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# 1. Nasz przyjazny formularz logowania
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Login lub e-mail"
        
    error_messages = {
        'invalid_login': "Ups! Nieprawidłowy login lub hasło. Jeśli nie masz jeszcze konta, kliknij przycisk rejestracji poniżej. ✨",
        'inactive': "To konto jest nieaktywne.",
    }

# 2. Formularz rejestracji z Generatorem Zabawnych Nicków
class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Imię")
    last_name = forms.CharField(required=True, label="Nazwisko")
    email = forms.EmailField(required=True, label="Adres e-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email") 

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ten adres e-mail jest już zajęty! Zaloguj się lub użyj innego.")
        return email

    # --- 2. NOWOŚĆ: Generator Puszystych Naleśników! ---
    def save(self, commit=True):
        user = super().save(commit=False)
        
        przymiotniki = ["Puszysty", "Wesoły", "Latający", "Magiczny", "Zaspany", 
            "Tańczący", "Uroczy", "Dzielny", "Mięciutki", "Kosmiczny", 
            "Gadatliwy", "Błyskotliwy", "Rozbrykany", "Uśmiechnięty", "Puchaty",
            "Skaczący", "Śpiący", "Kolorowy", "Błyszczący", "Szczęśliwy",
            "Miły", "Bystry", "Ciekawski"]
        rzeczowniki = ["Naleśnik", "Ziemniak", "Dinozaur", "Kapeć", "Słoik", 
            "Kosmita", "Pieróg", "Detektyw", "Pingwin", "Żółw", 
            "Smok", "Leniwiec", "Kameleon", "Borsuk", "Chmurka",
            "Wróbel", "Jeżyk", "Kotek", "Chomik", "Orzeł", 
            "Sowa", "Łoś", "Jednorożec"]
        
        # PĘTLA OCHRONNA: Losuj tak długo, aż znajdziesz unikalny nick
        while True:
            losowy_przymiotnik = random.choice(przymiotniki)
            losowy_rzeczownik = random.choice(rzeczowniki)
            # Zwiększyłam zakres liczb z 10-99 na 10-999, żeby było jeszcze mniej powtórek!
            losowy_numer = random.randint(10, 999) 
            
            zabawny_nick = f"{losowy_przymiotnik}{losowy_rzeczownik}{losowy_numer}"
            
            # Pytamy bazę: "Czy masz już kogoś takiego?"
            if not User.objects.filter(username=zabawny_nick).exists():
                # Jeśli NIE istnieje, przerywamy pętlę (break) - mamy to!
                break 
        
        # Zapisujemy nasz w 100% unikalny i wylosowany login
        user.username = zabawny_nick 
        
        if commit:
            user.save()
        return user