import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from income_and_expense.models import (
    Account, DefaultExpenseMonth, DefaultIncomeMonth, Expense, Income, Loan,
    Method, StateChoices,
)
from income_and_expense.serializers import (
    AccountSerializer, ExpenseSerializer, IncomeSerializer, LoanSerializer,
    MethodSerializer,
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


def _get_balance_done(year, month):
    """該当月末までの残高(完了分)。"""
    _, last_date = _month_range(year, month)
    inc = Income.objects.filter(
        pay_date__lte=last_date, state=StateChoices.DONE
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    exp = Expense.objects.filter(
        pay_date__lte=last_date, state=StateChoices.DONE
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    return inc - exp


class _InexViewSetBase(viewsets.ModelViewSet):
    model = None

    def get_queryset(self):
        qs = self.model.objects.select_related(
            'method__account__user', 'method__account__bank'
        )
        if self.action == 'list':
            year, month = _parse_year_month(self.request)
            first_date, last_date = _month_range(year, month)
            qs = qs.filter(pay_date__gte=first_date, pay_date__lte=last_date)
        return qs.order_by(
            'method__account__user__name', 'method__name',
            'method__account__bank__name', 'state', 'pay_date', 'name'
        )

    def _check_update_delete_allowed(self, instance):
        if not _can_update_or_delete(instance.pay_date.year, instance.pay_date.month):
            raise ValidationError("古いデータは更新・削除できません。")

    def update(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_update_delete_allowed(self.get_object())
        return super().destroy(request, *args, **kwargs)


class IncomeViewSet(_InexViewSetBase):
    serializer_class = IncomeSerializer
    model = Income
    queryset = Income.objects.all()

    @action(detail=False, methods=['post'], url_path='add_defaults')
    def add_defaults(self, request):
        year, month = _parse_year_month(request)
        if not _can_add_default(year, month):
            raise ValidationError("過去の月にはデフォルトを追加できません。")

        first_date, last_date = _month_range(year, month)
        def_inc_months = DefaultIncomeMonth.objects.filter(month=month)
        existing_names = set(
            Income.objects.filter(
                pay_date__gte=first_date, pay_date__lte=last_date
            ).values_list('name', flat=True)
        )

        add_num = 0
        for dim in def_inc_months:
            di = dim.def_inc
            if di.name in existing_names:
                continue
            Income(
                name=di.name,
                pay_date=datetime.date(year, month, di.pay_day),
                method=di.method, amount=di.amount, state=di.state,
            ).save()
            add_num += 1

        return Response({'added': add_num}, status=status.HTTP_201_CREATED)


class ExpenseViewSet(_InexViewSetBase):
    serializer_class = ExpenseSerializer
    model = Expense
    queryset = Expense.objects.all()

    @action(detail=False, methods=['post'], url_path='add_defaults')
    def add_defaults(self, request):
        year, month = _parse_year_month(request)
        if not _can_add_default(year, month):
            raise ValidationError("過去の月にはデフォルトを追加できません。")

        first_date, last_date = _month_range(year, month)
        existing_names = set(
            Expense.objects.filter(
                pay_date__gte=first_date, pay_date__lte=last_date
            ).values_list('name', flat=True)
        )

        add_num = 0
        for dem in DefaultExpenseMonth.objects.filter(month=month):
            de = dem.def_exp
            if de.name in existing_names:
                continue
            Expense(
                name=de.name,
                pay_date=datetime.date(year, month, de.pay_day),
                method=de.method, amount=de.amount, state=de.state,
            ).save()
            add_num += 1
            existing_names.add(de.name)

        loans = Loan.objects.filter(
            (Q(first_year__lt=year) | Q(first_year=year, first_month__lte=month)),
            (Q(last_year__gt=year) | Q(last_year=year, last_month__gte=month))
        )
        for loan in loans:
            if loan.name in existing_names:
                continue
            if year == loan.first_year and month == loan.first_month:
                amount = loan.amount_first
            else:
                amount = loan.amount_from_second
            Expense(
                name=loan.name,
                pay_date=datetime.date(year, month, loan.pay_day),
                method=loan.method, amount=amount, state=loan.state,
            ).save()
            add_num += 1
            existing_names.add(loan.name)

        return Response({'added': add_num}, status=status.HTTP_201_CREATED)


class MethodListAPIView(generics.ListAPIView):
    serializer_class = MethodSerializer

    def get_queryset(self):
        return Method.objects.select_related(
            'account__user', 'account__bank'
        ).order_by(
            'name', 'account__user__name', 'account__bank__name'
        )


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.select_related(
        'method__account__user', 'method__account__bank'
    ).order_by('first_year', 'first_month')


class AccountViewSet(viewsets.ModelViewSet):
    """口座一覧と残高更新用。"""
    serializer_class = AccountSerializer
    queryset = Account.objects.select_related('user', 'bank').order_by(
        'user__name', 'bank__name'
    )


class BalanceAPIView(views.APIView):
    """残高サマリ。口座一覧 + DB上残高(完了分) + 差額。"""

    def get(self, request):
        year, month = _parse_year_month(request)
        accounts = Account.objects.select_related('user', 'bank').order_by(
            'user__name', 'bank__name'
        )
        account_rows = []
        balance_sum = 0
        for a in accounts:
            account_rows.append({
                'id': a.id,
                'bank': a.bank.name,
                'user': a.user.name,
                'balance': a.balance,
                'formed_balance': a.formed_balance(),
            })
            balance_sum += a.balance

        balance_on_db = _get_balance_done(year, month)
        balance_diff = balance_sum - balance_on_db

        return Response({
            'year': year,
            'month': month,
            'accounts': account_rows,
            'balance_sum': balance_sum,
            'balance_on_db': balance_on_db,
            'balance_diff': balance_diff,
        })
