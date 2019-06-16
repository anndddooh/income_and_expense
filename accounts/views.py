from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

# Create your views here.

class login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class logout(LogoutView):
    pass