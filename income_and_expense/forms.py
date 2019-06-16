from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Income, Expense, Account


class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('balance',)


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = {
            'pay_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'pay_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
            'period_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
        }

IncomeFormSet = forms.modelformset_factory(
    Income, form=IncomeForm, can_delete=True, extra=1
)

ExpenseFormSet = forms.modelformset_factory(
    Expense, form=ExpenseForm, can_delete=True, extra=3
)

AccountBalanceFormSet = forms.modelformset_factory(
    Account, form=AccountBalanceForm, extra=0
)