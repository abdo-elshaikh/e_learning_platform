from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    LoginForm,
    RegisterForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    EditProfileForm,
)

# Login View


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('index')
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
                print(form.errors)
    else:
        form = LoginForm()

    return render(request, "users/login.html", {'form': form})


# Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# Logout View
def logout_view(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You are not logged in.')
        return redirect('login')
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')  # Password Reset View


def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Password reset email has been sent.')
            return redirect('login')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'users/password_reset.html', {'form': form})


# Set New Password View
def set_password_view(request, uidb64, token):
    form = CustomSetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request, 'Password has been reset. You can now log in.')
        return redirect('login')

    return render(request, 'users/set_password.html', {'form': form})


# Edit Profile View
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        # Update phone in profile model (if applicable)
        profile = user.profile  # Assuming a OneToOne relation with Profile
        profile.phone = request.POST.get('phone', profile.phone)
        profile.save()

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('index')
    return render(request, 'users/edit_profile.html')
