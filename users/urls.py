from django.urls import path
from .views import register, profile, edit_profile
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile.', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]