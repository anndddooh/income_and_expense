import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers

from income_and_expense.models import (
    Account, Expense, Income, Method, StateChoices,
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
