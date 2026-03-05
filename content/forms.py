import random
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError # <-- Dodaj to, żeby błędy działały!

letters_only = RegexValidator(
    regex=r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ ]+$',
    message='Imię i nazwisko mogą zawierać tylko litery.'
)

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
    first_name = forms.CharField(
        required=True, 
        label="Imię",
        validators=[letters_only],
        widget=forms.TextInput(attrs={'placeholder': 'np. Anna'})
    )
    last_name = forms.CharField(
        required=True,
         label="Nazwisko",
         validators=[letters_only],
         widget=forms.TextInput(attrs={'placeholder':'np. Kowalska'})
    )
    email = forms.EmailField(
        required=True, 
        label="Adres e-mail",
        widget=forms.EmailInput(attrs={
            'placeholder': 'np. kowalski@poczta.pl',
            'autocomplete': 'email',
            'class': 'form-control' })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email") 

    # POŁĄCZONA WALIDACJA EMAIL
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ten adres e-mail jest już zajęty! Zaloguj się lub użyj innego.")
        return email

    # --- Generator Puszystych Naleśników ---
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
        
        while True:
            zabawny_nick = f"{random.choice(przymiotniki)}{random.choice(rzeczowniki)}{random.randint(10, 999)}"
            if not User.objects.filter(username=zabawny_nick).exists():
                break 
        
        user.username = zabawny_nick 
        
        if commit:
            user.save()
        return user