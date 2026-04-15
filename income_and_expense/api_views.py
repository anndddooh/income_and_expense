import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from income_and_expense.models import (
    DefaultIncomeMonth, Income, Method,
)
from income_and_expense.serializers import (
    IncomeSerializer, MethodSerializer,
)


def _month_range(year, month):
    first_date = datetime.date(year, month, 1)
    last_date = first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    return first_date, last_date


def _parse_year_month(request):
    year = request.query_params.get('year')
    month = request.query_params.get('month')
    if not year or not month:
        raise ValidationError('year と month は必須です')
    try:
        return int(year), int(month)
    except (TypeError, ValueError):
        raise ValidationError('year, month は整数で指定してください')


def _can_update_or_delete(year, month):
    current_time = timezone.now()
    current_first = datetime.date(current_time.year, current_time.month, 1)
    last_month_first = current_first - relativedelta(months=1)
    return datetime.date(year, month, 1) >= last_month_first


def _can_add_default(year, month):
    current_time = timezone.now()
    current_first = datetime.date(current_time.year, current_time.month, 1)
    return datetime.date(year, month, 1) >= current_first


class IncomeViewSet(viewsets.ModelViewSet):
    """収入のCRUD。一覧は ?year=&month= で絞り込み。"""
    serializer_class = IncomeSerializer
    queryset = Income.objects.select_related(
        'method__account__user', 'method__account__bank'
    )

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            year, month = _parse_year_month(self.request)
            first_date, last_date = _month_range(year, month)
            qs = qs.filter(pay_date__gte=first_date, pay_date__lte=last_date)
        return qs.order_by(
            'method__account__user__name', 'method__name',
            'method__account__bank__name', 'state', 'pay_date', 'name'
        )

    def _check_update_delete_allowed(self, instance):
        year = instance.pay_date.year
        month = instance.pay_date.month
        if not _can_update_or_delete(year, month):
            raise ValidationError("古い収入は更新・削除できません。")

    def update(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='add_defaults')
    def add_defaults(self, request):
        """デフォルト収入から今月分を追加。"""
        year, month = _parse_year_month(request)
        if not _can_add_default(year, month):
            raise ValidationError("過去の月にはデフォルトを追加できません。")

        first_date, last_date = _month_range(year, month)
        def_inc_months = DefaultIncomeMonth.objects.filter(month=month)
        existing = Income.objects.filter(
            pay_date__gte=first_date, pay_date__lte=last_date
        )
        existing_names = {i.name for i in existing}

        add_num = 0
        for def_inc_month in def_inc_months:
            def_inc = def_inc_month.def_inc
            if def_inc.name in existing_names:
                continue
            Income(
                name=def_inc.name,
                pay_date=datetime.date(year, month, def_inc.pay_day),
                method=def_inc.method,
                amount=def_inc.amount,
                state=def_inc.state,
            ).save()
            add_num += 1

        return Response({'added': add_num}, status=status.HTTP_201_CREATED)


class MethodListAPIView(generics.ListAPIView):
    """支払方法(Method)一覧。フォームのプルダウン用。"""
    serializer_class = MethodSerializer

    def get_queryset(self):
        return Method.objects.select_related(
            'account__user', 'account__bank'
        ).order_by(
            'name', 'account__user__name', 'account__bank__name'
        )


# 既存の互換用(古いURL /api/incomes/?year=&month= を維持)
class IncomeListAPIView(generics.ListAPIView):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        year, month = _parse_year_month(self.request)
        first_date, last_date = _month_range(year, month)
        return Income.objects.select_related(
            'method__account__user', 'method__account__bank'
        ).order_by(
            'method__account__user__name', 'method__name',
            'method__account__bank__name', 'state', 'pay_date', 'name'
        ).filter(pay_date__gte=first_date, pay_date__lte=last_date)
