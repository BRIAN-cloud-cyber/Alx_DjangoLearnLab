from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # use Django's built-in User

# -----------------------------
# Registration View
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})

# -----------------------------
# Login View
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login')
        else:
            auth_login(request, user)
            return redirect('home')  # redirect to your home page

    return render(request, 'blog/login.html')  # template path matches blog folder

# -----------------------------
# Profile View (editable)
# -----------------------------
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'blog/profile.html', {'form': form})
