from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login.as_view(), name="login"),
    path('logout/', views.logout.as_view(), name="logout"),
]