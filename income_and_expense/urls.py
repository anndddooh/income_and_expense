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
    # ex: /income_and_expense/move_another_page
    path(
        'move_another_page',
        views.move_another_page,
        name='move_another_page'
    ),
    # ex: /income_and_expense/login/
    path(
        'login',
        views.login.as_view(),
        name='login'
    ),
    # ex: /income_and_expense/logout/
    path(
        'logout',
        views.logout.as_view(),
        name='logout'
    ),
    # ex: /income_and_expense/income/2019/3/
    path(
        'income/<int:year>/<int:month>',
        views.income,
        name='income'
    ),
    # ex: /income_and_expense/create_inc/2019/3/
    path(
        'create_inc/<int:year>/<int:month>',
        views.IncomeCreateView.as_view(),
        name='create_inc'
    ),
    # ex: /income_and_expense/update_inc/2019/3/567/
    path(
        'update_inc/<int:year>/<int:month>/<int:pk>',
        views.IncomeUpdateView.as_view(),
        name='update_inc'
    ),
    # ex: /income_and_expense/delete_inc/2019/3/567/
    path(
        'delete_inc/<int:year>/<int:month>/<int:pk>',
        views.IncomeDeleteView.as_view(),
        name='delete_inc'
    ),
    # ex: /income_and_expense/add_default_incs/2019/3/
    path(
        'add_default_incs/<int:year>/<int:month>',
        views.add_default_incs,
        name='add_default_incs'
    ),
    # ex: /income_and_expense/expense/2019/3/
    path(
        'expense/<int:year>/<int:month>',
        views.expense,
        name='expense'
    ),
    # ex: /income_and_expense/create_exp/2019/3/
    path(
        'create_exp/<int:year>/<int:month>',
        views.ExpenseCreateView.as_view(),
        name='create_exp'
    ),
    # ex: /income_and_expense/update_exp/2019/3/567/
    path(
        'update_exp/<int:year>/<int:month>/<int:pk>',
        views.ExpenseUpdateView.as_view(),
        name='update_exp'
    ),
    # ex: /income_and_expense/delete_exp/2019/3/567/
    path(
        'delete_exp/<int:year>/<int:month>/<int:pk>',
        views.ExpenseDeleteView.as_view(),
        name='delete_exp'
    ),
    # ex: /income_and_expense/add_default_exps/2019/3/
    path(
        'add_default_exps/<int:year>/<int:month>',
        views.add_default_exps,
        name='add_default_exps'
    ),
    # ex: /income_and_expense/balance/2019/3/
    path(
        'balance/<int:year>/<int:month>',
        views.balance,
        name='balance'
    ),
    # ex: /income_and_expense/update_balance/2019/3/5/
    path(
        'update_balance/<int:year>/<int:month>/<int:pk>',
        views.BalanceUpdateView.as_view(),
        name='update_balance'
    ),
    # ex: /income_and_expense/account_require/2019/3/
    path(
        'account_require/<int:year>/<int:month>',
        views.account_require,
        name='account_require'
    ),
    # ex: /income_and_expense/method_require/2019/3/
    path(
        'method_require/<int:year>/<int:month>',
        views.method_require,
        name='method_require'
    ),
    # ex: /income_and_expense/method_done/2019/3/2/
    path(
        'method_done/<int:year>/<int:month>/<int:pk>',
        views.method_done,
        name='method_done'
    )
]