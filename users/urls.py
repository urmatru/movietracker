from django.urls import path
from .views import register, profile, edit_profile
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pages:home'), name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name="registration/change_password.html", 
        success_url="/users/password_change/done/"
        ),
        name="password_change"
    ),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(
        template_name="registration/change_password_done.html"
        ),
        name="password_change_done"
    ),
]

