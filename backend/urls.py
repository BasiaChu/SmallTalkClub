from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings         
from django.conf.urls.static import static
from content.views import home, grammar, exercises, lesson_detail, private_lessons, readings, register_user, login_user, logout_user, student_zone, exercise_level, topic_exercises


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', home, name='home'),             # Strona główna
    path('grammar/', grammar, name='grammar'),
    path('exercises/', exercises, name='exercises'),
    path('readings/', readings, name='readings'), # Opcjonalnie
    path('private-lessons/', private_lessons, name='private_lessons'),
    path('lesson/<slug:slug>/', lesson_detail, name='lesson_detail'),
    path('rejestracja/', register_user, name='register'),
    path('logowanie/', login_user, name='login'),
    path('wyloguj/', logout_user, name='logout'),
    path('strefa-ucznia/', student_zone, name='student_zone'),
    path('reset_hasla/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name='password_reset'),
    path('reset_hasla/wyslano/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_hasla/gotowe/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    path('exercises/<str:level_name>/', exercise_level, name='exercise_level'),
    path('exercises/<str:level_name>/<slug:category_slug>/', topic_exercises, name='topic_exercises')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)