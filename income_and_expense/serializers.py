from rest_framework import serializers

from income_and_expense.models import Income, StateChoices


class IncomeSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    method_name = serializers.CharField(source='method.name', read_only=True)
    state_label = serializers.SerializerMethodField()
    formed_amount = serializers.CharField(read_only=True)

    class Meta:
        model = Income
        fields = [
            'id', 'name', 'pay_date', 'method', 'method_name',
            'account', 'amount', 'formed_amount',
            'state', 'state_label', 'memo',
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