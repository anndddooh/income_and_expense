from django.urls import path

from . import views

app_name = 'income_and_expense'

urlpatterns = [
    # ex: /income_and_expense/
    path(
        '',
        views.index,
        name='index'
    ),
    # ex: /income_and_expense/2019/3/income
    path(
        '<int:year>/<int:month>/income',
        views.income,
        name='income'
    ),
    # ex: /income_and_expense/2019/3/create_inc/
    path(
        '<int:year>/<int:month>/create_inc',
        views.IncomeCreateView.as_view(),
        name='create_inc'
    ),
    # ex: /income_and_expense/2019/3/567/update_inc/
    path(
        '<int:year>/<int:month>/<int:pk>/update_inc',
        views.IncomeUpdateView.as_view(),
        name='update_inc'
    ),
    # ex: /income_and_expense/2019/3/567/delete_inc/
    path(
        '<int:year>/<int:month>/<int:pk>/delete_inc',
        views.IncomeDeleteView.as_view(),
        name='delete_inc'
    ),
    # ex: /income_and_expense/2019/3/expense
    path(
        '<int:year>/<int:month>/expense',
        views.expense,
        name='expense'
    ),
    # ex: /income_and_expense/2019/3/create_exp/
    path(
        '<int:year>/<int:month>/create_exp',
        views.ExpenseCreateView.as_view(),
        name='create_exp'
    ),
    # ex: /income_and_expense/2019/3/567/update_exp/
    path(
        '<int:year>/<int:month>/<int:pk>/update_exp',
        views.ExpenseUpdateView.as_view(),
        name='update_exp'
    ),
    # ex: /income_and_expense/2019/3/567/delete_exp/
    path(
        '<int:year>/<int:month>/<int:pk>/delete_exp',
        views.ExpenseDeleteView.as_view(),
        name='delete_exp'
    ),
    # ex: /income_and_expense/2019/3/balance/
    path(
        '<int:year>/<int:month>/balance',
        views.balance,
        name='balance'
    ),
    # ex: /income_and_expense/2019/3/5/update_balance/
    path(
        '<int:year>/<int:month>/<int:pk>/update_balance',
        views.BalanceUpdateView.as_view(),
        name='update_balance'
    ),
    # ex: /income_and_expense/2019/3/account_require/
    path(
        '<int:year>/<int:month>/account_require',
        views.account_require,
        name='account_require'
    ),
    # ex: /income_and_expense/2019/3/method_require/
    path(
        '<int:year>/<int:month>/method_require',
        views.method_require,
        name='method_require'
    ),
    # ex: /income_and_expense/2019/3/2/method_done/
    path(
        '<int:year>/<int:month>/<int:pk>/method_done',
        views.method_done,
        name='method_done'
    )
]