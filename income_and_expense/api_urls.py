from django.urls import include, path
from rest_framework.routers import DefaultRouter

from income_and_expense import api_views

app_name = 'api'

router = DefaultRouter()
router.register(r'incomes', api_views.IncomeViewSet, basename='income')
router.register(r'expenses', api_views.ExpenseViewSet, basename='expense')
router.register(r'accounts', api_views.AccountViewSet, basename='account')
router.register(r'loans', api_views.LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
    path('methods/', api_views.MethodListAPIView.as_view(), name='method-list'),
    path('balance/', api_views.BalanceAPIView.as_view(), name='balance'),
]
