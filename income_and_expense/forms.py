from django import forms
from .models import Income, Expense, Account
from bootstrap_modal_forms.forms import BSModalForm
from income_and_expense.const import const_data


class ExpenseForm(BSModalForm):
    class Meta:
        model = Expense
        fields = ['name', 'pay_date', 'method', 'amount', 'undecided', 'done']
        labels = {
            'name': const_data.const.SHOWN_NAME_NAME,
            'pay_date': const_data.const.SHOWN_NAME_PAY_DATE,
            'method': const_data.const.SHOWN_NAME_METHOD,
            'amount': const_data.const.SHOWN_NAME_AMOUNT,
            'undecided': const_data.const.SHOWN_NAME_UNDECIDED,
            'done': const_data.const.SHOWN_NAME_DONE
        }


class IncomeForm(BSModalForm):
    class Meta:
        model = Income
        fields = ['name', 'pay_date', 'method', 'amount', 'undecided', 'done']
        labels = {
            'name': const_data.const.SHOWN_NAME_NAME,
            'pay_date': const_data.const.SHOWN_NAME_PAY_DATE,
            'method': const_data.const.SHOWN_NAME_METHOD,
            'amount': const_data.const.SHOWN_NAME_AMOUNT,
            'undecided': const_data.const.SHOWN_NAME_UNDECIDED,
            'done': const_data.const.SHOWN_NAME_DONE
        }


class BalanceForm(BSModalForm):
    class Meta:
        model = Account
        fields = ['bank', 'balance']
        labels = {
            'bank': const_data.const.SHOWN_NAME_ACCOUNT,
            'balance': const_data.const.SHOWN_NAME_BALANCE
        }