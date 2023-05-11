from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# from .models import CustomUser

# @login_required
# def follow_user(request, user_id):
#     user_to_follow = get_object_or_404(CustomUser, id=user_id)
#     request.user.following.add(user_to_follow)
#     return redirect('user_profile', user_id=user_id)

class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)
        return to_return
    
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    
