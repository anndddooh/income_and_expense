from django.urls import path

from . import views

app_name = 'income_and_expense'

urlpatterns = [
    # ex: /index_and_expense/
    path(
        '',
        views.index,
        name='index'
    ),
    # ex: /index_and_expense/2019/3/
    path(
        '<int:year>/<int:month>/',
        views.table,
        name='table'
    ),
    # ex: /income_and_expense/2019/3/modify_inc/
    path(
        '<int:year>/<int:month>/modify_inc',
        views.modify_income,
        name='modify_inc'
    ),
    # ex: /income_and_expense/2019/3/modify_exp/
    path(
        '<int:year>/<int:month>/modify_exp',
        views.modify_expense,
        name='modify_exp'
    ),
    # ex: /income_and_expense/2019/3/modify_blance/
    path(
        '<int:year>/<int:month>/modify_blance',
        views.modify_account_balance,
        name='modify_balance'
    )
]