from django import forms
from .models import Income, Expense, Account
from bootstrap_modal_forms.forms import BSModalForm


class ExpenseForm(BSModalForm):
    class Meta:
        model = Expense
        fields = ['name', 'pay_date', 'method', 'amount', 'undecided', 'done']


class IncomeForm(BSModalForm):
    class Meta:
        model = Income
        fields = ['name', 'pay_date', 'method', 'amount', 'undecided', 'done']


class BalanceForm(BSModalForm):
    class Meta:
        model = Account
        fields = ['bank', 'balance']