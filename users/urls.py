from django.urls import path
from .views import (
    login_view,
    register_view,
    logout_view,
    password_reset_view,
    set_password_view,
    edit_profile_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('set-password/<uidb64>/<token>/', set_password_view, name='set_password'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
]
