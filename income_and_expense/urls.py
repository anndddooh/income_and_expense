from django.urls import path

from . import views

app_name = 'income_and_expense'

urlpatterns = [
    # ex: /index_and_expense/
    path('', views.index, name='index'),
    # ex: /index_and_expense/2019/3/
    path('<int:year>/<int:month>/', views.table, name='table')
]