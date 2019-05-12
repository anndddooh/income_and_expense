from django import forms
from .models import Income, Expense, Account


class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('balance',)

IncomeFormSet = forms.modelformset_factory(
    Income, fields='__all__', can_delete=True, extra=1
)

ExpenseFormSet = forms.modelformset_factory(
    Expense, fields='__all__', can_delete=True, extra=1
)

AccountBalanceFormSet = forms.modelformset_factory(
    Account, form=AccountBalanceForm, extra=0
)