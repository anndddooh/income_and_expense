import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers

from income_and_expense.models import (
    Account, Expense, Income, Loan, Method, StateChoices, TemplateExpense,
)


def is_valid_pay_date(pay_date):
    """1か月前以降の日付か。"""
    current_time = timezone.now()
    current_date = datetime.date(
        current_time.year, current_time.month, current_time.day
    )
    one_month_ago_date = current_date - relativedelta(months=1)
    return pay_date >= one_month_ago_date


class MethodSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Method
        fields = ['id', 'name', 'display_name']

    def get_display_name(self, obj):
        return str(obj)


class _InexSerializerBase(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    method_name = serializers.CharField(source='method.name', read_only=True)
    state_label = serializers.SerializerMethodField()
    formed_amount = serializers.CharField(read_only=True)

    def get_account(self, obj):
        acc = obj.method.account
        return {
            'id': acc.id,
            'user': acc.user.name,
            'bank': acc.bank.name,
        }

    def get_state_label(self, obj):
        return StateChoices(obj.state).label

    def validate_pay_date(self, value):
        if self.instance is not None and self.instance.pay_date == value:
            return value
        if not is_valid_pay_date(value):
            raise serializers.ValidationError(
                "1か月前より前の日付は指定できません。"
            )
        return value


class IncomeSerializer(_InexSerializerBase):
    class Meta:
        model = Income
        fields = [
            'id', 'name', 'pay_date', 'method', 'method_name',
            'account', 'amount', 'formed_amount',
            'state', 'state_label', 'memo',
        ]


class ExpenseSerializer(_InexSerializerBase):
    class Meta:
        model = Expense
        fields = [
            'id', 'name', 'pay_date', 'method', 'method_name',
            'account', 'amount', 'formed_amount',
            'state', 'state_label', 'memo',
        ]


class LoanSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(source='method.name', read_only=True)
    account = serializers.SerializerMethodField()
    state_label = serializers.SerializerMethodField()
    formed_amount_first = serializers.CharField(read_only=True)
    formed_amount_from_second = serializers.CharField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'name', 'pay_day',
            'first_year', 'first_month', 'last_year', 'last_month',
            'method', 'method_name', 'account',
            'amount_first', 'amount_from_second',
            'formed_amount_first', 'formed_amount_from_second',
            'state', 'state_label',
        ]

    def get_account(self, obj):
        acc = obj.method.account
        return {
            'id': acc.id,
            'user': acc.user.name,
            'bank': acc.bank.name,
        }

    def get_state_label(self, obj):
        return StateChoices(obj.state).label


class AccountSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    formed_balance = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id', 'bank', 'user', 'bank_name', 'user_name',
            'balance', 'formed_balance',
        ]


class TemplateExpenseSerializer(serializers.ModelSerializer):
    method_name = serializers.SerializerMethodField()
    pay_date = serializers.SerializerMethodField()

    class Meta:
        model = TemplateExpense
        fields = [
            'id', 'template_name', 'name',
            'date_type', 'pay_day', 'limit_day_of_this_month',
            'method', 'method_name', 'state', 'pay_date',
        ]

    def get_method_name(self, obj):
        return str(obj.method)

    def get_pay_date(self, obj):
        today = datetime.date.today()
        if obj.date_type == 'today':
            pay_date = today
        else:
            if today.day <= obj.limit_day_of_this_month:
                pay_date = datetime.date(
                    today.year, today.month, obj.pay_day
                )
            else:
                pay_date = datetime.date(
                    today.year, today.month, obj.pay_day
                ) + relativedelta(months=1)
            if obj.pay_day < obj.limit_day_of_this_month:
                pay_date += relativedelta(months=1)
        return pay_date.strftime('%Y-%m-%d')
