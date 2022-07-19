import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth import forms as auth_forms
from django import forms
from .models import Income, Expense, Account, Loan
from bootstrap_modal_forms.forms import BSModalModelForm
from income_and_expense.const import const_data


def is_valid_pay_date(pay_date):
    """有効な支払日かどうかをチェック

    Parameters
    ----------
    pay_date : DateField
        支払日

    Returns
    -------
    bool
        有効な支払日かどうか
    """

    # 1か月前の日付を取得
    current_time = timezone.now()
    current_date = datetime.date(
        current_time.year, current_time.month, current_time.day
    )
    one_month_ago_date = current_date - relativedelta(months=1)

    # 1か月前より前の日付は無効
    if pay_date < one_month_ago_date:
        return False

    return True


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class ExpenseForm(BSModalModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'pay_date', 'method', 'amount', 'state']
        labels = {
            'name': const_data.const.SHOWN_NAME_NAME,
            'pay_date': const_data.const.SHOWN_NAME_PAY_DATE,
            'method': const_data.const.SHOWN_NAME_METHOD,
            'amount': const_data.const.SHOWN_NAME_AMOUNT,
            'state': const_data.const.SHOWN_NAME_STATE
        }

    def clean_pay_date(self):
        pay_date = self.cleaned_data.get('pay_date')
        if not is_valid_pay_date(pay_date):
            raise forms.ValidationError("1か月前より前の日付は指定できません。")
        return pay_date


class IncomeForm(BSModalModelForm):
    class Meta:
        model = Income
        fields = ['name', 'pay_date', 'method', 'amount', 'state']
        labels = {
            'name': const_data.const.SHOWN_NAME_NAME,
            'pay_date': const_data.const.SHOWN_NAME_PAY_DATE,
            'method': const_data.const.SHOWN_NAME_METHOD,
            'amount': const_data.const.SHOWN_NAME_AMOUNT,
            'state': const_data.const.SHOWN_NAME_STATE
        }

    def clean_pay_date(self):
        pay_date = self.cleaned_data.get('pay_date')
        if not is_valid_pay_date(pay_date):
            raise forms.ValidationError("1か月前より前の日付は指定できません。")
        return pay_date


class BalanceForm(BSModalModelForm):
    class Meta:
        model = Account
        fields = ['bank', 'user', 'balance']
        labels = {
            'bank': const_data.const.SHOWN_NAME_ACCOUNT,
            'user': const_data.const.SHOWN_NAME_USER,
            'balance': const_data.const.SHOWN_NAME_BALANCE
        }


class LoanForm(BSModalModelForm):
    class Meta:
        model = Loan
        fields = ['name', 'pay_day', 'first_year', 'first_month',
            'last_year', 'last_month', 'method', 'amount_first',
            'amount_from_second', 'state']
        labels = {
            'name': const_data.const.SHOWN_NAME_NAME,
            'pay_day': const_data.const.SHOWN_NAME_PAY_DATE,
            'first_year': const_data.const.SHOWN_NAME_FIRST_YEAR,
            'first_month': const_data.const.SHOWN_NAME_FIRST_MONTH,
            'last_year': const_data.const.SHOWN_NAME_LAST_YEAR,
            'last_month': const_data.const.SHOWN_NAME_LAST_MONTH,
            'method': const_data.const.SHOWN_NAME_METHOD,
            'amount_first': (
                const_data.const.SHOWN_NAME_AMOUNT
                + const_data.const.SHOWN_NAME_FIRST
            ),
            'amount_from_second': (
                const_data.const.SHOWN_NAME_AMOUNT
                + const_data.const.SHOWN_NAME_FROM_SECOND
            ),
            'state': const_data.const.SHOWN_NAME_STATE
        }