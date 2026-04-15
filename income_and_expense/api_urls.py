from django.urls import path

from income_and_expense import api_views

app_name = 'api'

urlpatterns = [
    path('incomes/', api_views.IncomeListAPIView.as_view(), name='income-list'),
]