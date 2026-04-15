import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from income_and_expense.models import Income
from income_and_expense.serializers import IncomeSerializer


class IncomeListAPIView(generics.ListAPIView):
    """指定した年月の収入一覧を返す。 ?year=YYYY&month=M"""
    serializer_class = IncomeSerializer

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if not year or not month:
            raise ValidationError('year と month は必須です')
        try:
            year, month = int(year), int(month)
            first_date = datetime.date(year, month, 1)
        except (ValueError, TypeError):
            raise ValidationError('year, month は整数で指定してください')

        last_date = first_date + relativedelta(months=1) - datetime.timedelta(days=1)

        return Income.objects.select_related(
            'method__account__user', 'method__account__bank'
        ).order_by(
            'method__account__user__name', 'method__name',
            'method__account__bank__name', 'state', 'pay_date', 'name'
        ).filter(pay_date__gte=first_date, pay_date__lte=last_date)
