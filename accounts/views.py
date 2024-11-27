from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Order 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

class RegisterUser(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome!")
            return redirect('home') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
        return render(request, 'accounts/register.html', {'form': form})


class LoginUser(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "Invalid username or password!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
        return render(request, 'accounts/login.html', {'form': form})

class UserProfile(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'accounts/profile/profile.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items').order_by('-created_at')
    
@login_required
def edit_profile(request):
    user_profile = None  
    try:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            user_profile = UserProfile.objects.create(user=request.user)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        user_profile = None  

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "There were errors in your form. Please correct them.")
    else:
        form = EditProfileForm(instance=user_profile)

    return render(request, 'accounts/profile/edit_profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        return render(request, 'login.html')