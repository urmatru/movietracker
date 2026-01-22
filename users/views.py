from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from users.forms import COUNTRYCHOICES

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profiles/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            selected_country = form.cleaned_data['country']
            if selected_country:
                user.country = selected_country
                name_to_code = {name: code for code, name in COUNTRYCHOICES}
                user.country_code = name_to_code.get(selected_country, "")
            else:
                user.country_code = ""
                user.country = ""
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profiles/edit_profile.html', {'form': form})


