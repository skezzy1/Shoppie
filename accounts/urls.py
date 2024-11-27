from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterUser, LoginUser, UserProfile, edit_profile
from . import views

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
