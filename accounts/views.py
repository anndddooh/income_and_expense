from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import LoginForm

# Create your views here.

class login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class logout(LogoutView):
    template_name = "accounts/logout.html"