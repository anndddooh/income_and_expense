from django.forms import modelformset_factory
from .models import Income

IncomeFormSet = modelformset_factory(Income, fields=("name", "amount"))